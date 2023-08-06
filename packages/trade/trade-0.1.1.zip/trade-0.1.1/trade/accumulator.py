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

import math

from .utils import average_price, same_sign


class Accumulator:
    """An accumulator of quantity @ some average price.

    Attributes:
        asset: An asset instance, the asset whose data are being
            accumulated.
        date: A string 'YYYY-mm-dd' representing the date of the last
            status change of the accumulator.
        quantity: The asset's accumulated quantity.
        price: The asset's average price for the quantity accumulated.
        results: A dict with the total results from the operations
            accumulated.
        logging: A boolean indicating if the accumulator should log
            the calls to the accumulate() method.
        log: A dict with all the operations performed with the asset,
            provided that self.logging is True.

    if created with logging=True the accumulator will log the every
    operation it accumulates.

    Results are calculated by the accumulator according to the value
    of the operations informed and the current status of the
    accumulator (the current quantity and average price of the asset).
    """

    def __init__(self, asset=None, logging=False):
        """Creates a instance of the accumulator.

        Logging by default is set to False; the accumulator will not
        log any operation, just accumulate the quantity and calculate
        the average price and results related to the asset after each
        call to accumulate_operation(), accumulate_daytrade() and
        accumulate_event().

        If logging is set to True the accumulator will log the data
        passed on every call to accumulate_operation(),
        accumulate_daytrade() and accumulate_event().
        """
        self.asset = asset
        self.date = None
        self.quantity = 0
        self.price = 0
        self.results = {
            'trades': 0,
            'daytrades': 0
        }
        self.logging = logging
        self.log = {}

    def accumulate_operation(self, operation):
        """Accumulates operation data to the existing position."""

        # Operations may update the posions themselves,
        # or maybe its their underlying operations that
        # should update the position. This is determined
        # by the accumulate_underlying_operations
        # attribute on the Operation object.
        if operation.accumulate_underlying_operations:

            # If its the underlying operations that should
            # update the position, then we iterate through
            # all underlying operations and let each one
            # of them update the accumulator's position.
            for underlying_operation in operation.operations:
                self.update_position(underlying_operation)

        # If its not the underlying_operations that should
        # update the position, them we try to use the operation
        # itself to update the accumulator's position.
        else:
            self.update_position(operation)

        # add whatever result was informed with or generated
        # by this operation to the accumulator results dict
        for key, value in operation.results.items():
            if key not in self.results:
                self.results[key] = 0
            self.results[key] += value

        # log the operation, if logging
        if self.logging:
            self.log_occurrence(operation)

        return operation.results

    def update_position(self, operation):
        """Update the position of the accumulator with an Operation."""

        # Here we check if the operation asset is the same
        # asset of this Accumulator object; the accumulator
        # only accumulates operations that trade its asset.
        # We also check if the operation should update the
        # position; if all this conditions are met, then
        # the position is updated.
        update_position_condition = (
            operation.asset == self.asset and
            operation.update_position and
            operation.quantity
        )
        if update_position_condition:

            # Define the new accumualtor quantity
            new_quantity = self.quantity + operation.quantity

            # if the quantity of the operation has the same sign
            # of the accumulated quantity then we need to
            # find out the new average price of the asset
            if same_sign(self.quantity, operation.quantity):
                self.price = average_price(
                                self.quantity,
                                self.price,
                                operation.quantity,
                                operation.real_price
                            )

            # If the traded quantity has an opposite sign of the
            # asset's accumulated quantity and the accumulated
            # quantity is not zero, then there was a result.
            elif self.quantity != 0:

                # check if we are trading more than what
                # we have on our portfolio; if yes,
                # the result will be calculated based
                # only on what was traded (the rest create
                # a new position)
                if abs(operation.quantity) > abs(self.quantity):
                        result_quantity = self.quantity * -1

                # If we're not trading more than what we have,
                # then use the operation quantity to calculate
                # the result
                else:
                    result_quantity = operation.quantity

                # calculate the result of this operation and add
                # the new result to the accumulated results
                operation.results['trades'] += result_quantity * self.price - \
                                        result_quantity * operation.real_price

                # If the new accumulated quantity is of the same sign
                # of the old accumulated quantity, the average of price
                # will not change.
                if same_sign(self.quantity, new_quantity):
                    self.price = self.price

                # If the new accumulated quantity is of different
                # sign of the old accumulated quantity then the
                # average price is now the price of the operation
                else:
                    self.price = operation.real_price

            # If the accumulated quantity was zero then
            # there was no result and the new average price
            # is the price of the operation
            else:
                self.price = operation.real_price

            # update the accumulator quantity
            # with the new quantity
            self.quantity = new_quantity

            # If the accumulator is empty
            # the price is set back to zero
            if not self.quantity:
                self.price = 0


    def accumulate_event(self, event):
        """Receives a Event subclass instance and lets it do its work.

        An event can change the quantity, price and results stored in
        the accumulator.

        The way it changes this information is up to the event object;
        each Event subclass must implement a method like this:

            update_portfolio(quantity, price, results)
                # do stuff here...
                return quantity, price

        that have the logic for the change in the accumulator's
        quantity, price and results.
        """
        self.quantity, self.price = event.update_portfolio(
                                        self.quantity,
                                        self.price,
                                        self.results
                                    )
        if self.logging:
            self.log_occurrence(event)

    def log_occurrence(self, operation):
        """Log Operation, Daytrade and Event objects.

        If logging, this method is called behind the scenes every
        time the method accumulate() is called. The occurrences are
        logged like this:

            self.log = {
                '2017-09-19': {
                    'position': {
                        'quantity': float
                        'price': float
                    }
                    'occurrences': [Operation, ...],
                },
                ...
            }
        """

        # If the date is not present in the dict keys,
        # a new key created.
        if operation.date not in self.log:
            self.log[operation.date] = {'occurrences': []}

        # Log the accumulator status and operation data
        self.log[operation.date]['position'] = {
            'quantity': self.quantity,
            'price': self.price,
        }

        self.log[operation.date]['occurrences'].append(operation)
