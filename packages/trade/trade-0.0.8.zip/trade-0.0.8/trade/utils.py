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


def daytrade_condition(operation_a, operation_b):
    """Checks if the operations are day trades."""
    return (
        operation_a.asset == operation_b.asset and
        not same_sign(operation_a.quantity, operation_b.quantity) and
        operation_a.quantity != 0 and
        operation_b.quantity != 0
    )


def average_price(quantity_1, price_1, quantity_2, price_2):
    """Calculates the average price between two positions.

    A position is the quantity of an asset and its average price.
    """
    return (quantity_1 * price_1 + quantity_2 * price_2) / \
            (quantity_1 + quantity_2)


def same_sign(x, y):
    """Checks if two numbers have the same sign."""
    try:
        return (int(x) >= 0) ^ (int(y) < 0)
    except:
        return None


# TODO document this better
def find_purchase_and_sale(operation_a, operation_b):
    """Find which is a purchase and which is a sale."""
    if same_sign(operation_a.quantity, operation_b.quantity):
        return None
    if operation_a.quantity > operation_b.quantity:
        return operation_a, operation_b
    return operation_b, operation_a
