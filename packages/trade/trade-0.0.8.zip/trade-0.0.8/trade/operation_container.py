"""trade: Tools For Stock Trading Applications.

Copyright (c) 2015 Rafael da Silva Rocha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import absolute_import
from __future__ import division

import math
import copy

from .operation import Daytrade, Operation
from .tax_manager import TaxManager
from .utils import (
    average_price, daytrade_condition, find_purchase_and_sale
)


class OperationContainer:
    """A container for operations.

    An OperationContainer is used to group operations, like operations
    that occurred on the same date, and then perform tasks on them.

    The main task task that the OperationContainer can perform is to
    identify the resulting positions from a group of operations. The
    resulting positions are all operations separated as daytrades and
    common operations, with all common operations and daytrades with
    the same asset grouped into a single operation or a single
    daytrade.

    The resulting common operations and daytrades contains the
    OperationContiner commissions prorated by their volumes, and also
    any fees the OperationContainer TaxManager finds for them.

    This is achieved by calling this method:

        fetch_positions()

    Every time fetch_positions() is called the OperationContainer
    execute this tasks behind the scenes:

    - Separate the daytrades and the common operations of a group of
      operations that occurred on the same date by using the method:

        identify_daytrades_and_common_operations()

    - Prorate a group of taxes proportionally for all daytrades and
      common operations, if any, by using the method:

        prorate_commissions_by_daytrades_and_common_operations()

    - Find the appliable fees for the resulting positions by calling
      this method:

        find_fees_for_positions()

    Attributes:
        date: A string 'YYYY-mm-dd' representing the date of the
            operations on the container.
        operations: A list of Operation instances.
        commissions: A dict with discount names and values to be
            deducted from the operations.
        daytrades: a dict of Daytrade objects, indexed by the daytrade
            asset.
        common_operations: a dict of Operation objects, indexed by the
            operation asset.
    """

    def __init__(self,
                date=None,
                operations=None,
                exercises=None,
                fixed_commissions=None,
                tax_manager=TaxManager()
            ):
        self.date = date
        if operations is None: operations=[]
        if exercises is None: exercises=[]
        if fixed_commissions is None: fixed_commissions = {}
        self.operations = operations
        self.exercises = exercises
        self.fixed_commissions = fixed_commissions
        self.daytrades = {}
        self.common_operations = {}
        self.exercise_operations = {}
        self.tax_manager = tax_manager

    @property
    def total_commission_value(self):
        """Returns the sum of values of all commissions."""
        return sum(self.fixed_commissions.values())

    @property
    def volume(self):
        """Returns the total volume of the operations in the container."""
        return sum(operation.volume for operation in self.operations)

    def fetch_positions(self):
        """Fetch the positions resulting from the operations.

        Fetch the position is a complex process that needs to be
        better documented. What happens is as follows:

        - Separate all daytrades and common operations;
        - Group all common operations with one asset into a single
            Operation, so in the end you only have one operation
            per asset (on self.common_operations);
        - Group all daytrades with one asset into a single Daytrade,
            so in the end you only have one daytrade per asset;
        - put all common operations in self.common_operations, a dict
            indexed by the operation's asset name;
        - put all daytrades in self.daytrades, a dict indexed by the
            daytrade's asset name;
        - Prorate all commissions of the container for the common
            operations and the purchase and sale operation of every
            daytrade;
        - Find the taxes to be applied to every common operation and to
            every purchase and sale operation of every daytrade.

        After this method:

        - the raw operations list of the container remains untouched;
        - the container common_operations list is filled with all
            common operations of the container, with all information
            about commissions and taxes to be applied to each operation;
        - the container daytrades list is filled with all daytrades
            of the container, with all information about commissions
            and taxes to be applied to every purchase and sale
            operation of every daytrade.
        """
        self.get_operations_from_exercises()
        self.identify_daytrades_and_common_operations()
        self.prorate_fixed_commissions()
        self.find_fees_for_positions()

    def get_operations_from_exercises(self):
        for exercise in self.exercises:
            for operation in exercise.get_operations():
                if operation.asset in self.exercise_operations.keys():
                    self.merge_operations(
                        self.exercise_operations[operation.asset],
                        operation
                    )
                else:
                    self.exercise_operations[operation.asset] = operation

    def prorate_fixed_commissions(self):
        """Prorates the container's commissions by its operations.

        This method sum the discounts in the commissions dict of the
        container. The total discount value is then prorated by the
        daytrades and common operations based on their volume.
        """
        for operation in self.common_operations.values():
            self.prorate_commissions_by_operation(operation)
        for daytrade in self.daytrades.values():
            self.prorate_commissions_by_operation(daytrade.purchase)
            self.prorate_commissions_by_operation(daytrade.sale)

    def prorate_commissions_by_operation(self, operation):
        """Prorates the commissions of the container for one operation.

        The ratio is based on the container volume and the volume of
        the operation.
        """
        percent = operation.volume / self.volume * 100
        for key, value in self.fixed_commissions.items():
            operation.fixed_commissions[key] = value * percent / 100

    def identify_daytrades_and_common_operations(self):
        """Separates operations into daytrades and common operations.

        After this process, the attributes 'daytrades' and
        'common_operations'  will be filled with the daytrades
        and common operations found in the container operations list,
        if any. The original operations list remains untouched.
        """
        operations = copy.deepcopy(self.operations)

        for i, operation_a in enumerate(operations):
            for operation_b in \
                    [
                        op for op in operations[i:] if daytrade_condition(
                                                            op, operation_a
                                                        )
                    ]:
                if operation_b.quantity != 0 and operation_a.quantity != 0:
                    self.extract_daytrade(operation_a, operation_b)

            if operation_a.quantity != 0:
                self.add_to_common_operations(operation_a)

    def extract_daytrade(self, operation_a, operation_b):
        """Extracts the daytrade part of two operations."""

        # Find what is the purchase and what is the sale
        purchase, sale = find_purchase_and_sale(operation_a, operation_b)

        # Find the daytraded quantity; the daytraded
        # quantity is always the smallest absolute quantity
        daytrade_quantity = min([abs(purchase.quantity), abs(sale.quantity)])

        # Update the operations that originated the
        # daytrade with the new quantity after the
        # daytraded part has been extracted; One of
        # the operations will always have zero
        # quantity after this, being fully consumed
        # by the daytrade. The other operation may or
        # may not end with zero quantity.
        purchase.quantity -= daytrade_quantity
        sale.quantity += daytrade_quantity

        # Now that we know everything we need to know
        # about the daytrade, we create the Daytrade object
        daytrade = Daytrade(
            self.date,
            purchase.asset,
            daytrade_quantity,
            purchase.price,
            sale.price
        )

        # If this container already have a Daytrade
        # with this asset, we merge this daytrade
        # with the daytrade in self.daytrades -
        # in the end, there is only one daytrade per
        # asset per OperationContainer.
        if daytrade.asset in self.daytrades:
            self.merge_operations(
                self.daytrades[daytrade.asset].purchase,
                daytrade.purchase
            )
            self.merge_operations(
                self.daytrades[daytrade.asset].sale,
                daytrade.sale
            )
            self.daytrades[daytrade.asset].quantity += daytrade.quantity
        else:
            self.daytrades[daytrade.asset] = daytrade

    def add_to_common_operations(self, operation):
        """Adds an operation to the common operations list."""
        if operation.asset in self.common_operations:
            self.merge_operations(
                self.common_operations[operation.asset],
                operation
            )
        else:
            self.common_operations[operation.asset] = operation

    def merge_operations(self, existing_operation, operation):
        """Merges one operation with another operation."""
        existing_operation.price = average_price(
                                        existing_operation.quantity,
                                        existing_operation.price,
                                        operation.quantity,
                                        operation.price
                                    )
        existing_operation.quantity += operation.quantity

    def find_fees_for_positions(self):
        """Finds the taxess for all daytrades and common operations."""
        for asset, daytrade in self.daytrades.items():
            daytrade.purchase.commission_rates = \
                self.tax_manager.get_fees_for_daytrade(daytrade.purchase)
            daytrade.sale.commission_rates = \
                self.tax_manager.get_fees_for_daytrade(daytrade.sale)
        for asset, operation in self.common_operations.items():
            operation.commission_rates = \
                self.tax_manager.get_fees_for_operation(operation)
