# import evo
import json

from order import Order
from random import randrange


def setups(L: list) -> int:  # minimise
    """Calculates the number of setups
    Parameters:
        L (list): list of orders
    Returns:
        int: number of setups"""

    return sum([L[i].oprod() != L[i + 1].oprod() for i in range(len(L) - 1)])

def low_priority(L: list) -> int:  # minimise
    """Calculates the number of low priority orders produced before the last high priority order
    Parameters:
        L (list): list of orders
    Returns:
        int: sum of quantities"""

    last_high_priority = max([idx for idx, o in enumerate(L) if o.oprior() == Order.PRIOR_MAP['HIGH']])
    return sum([o.oquant() for o in L[: last_high_priority] if o.oprior() == Order.PRIOR_MAP['LOW']])

def delays(L: list) -> int:  # minimise
    """Calculates the sum of delays
    Parameters:
        L (list): list of orders
    Returns:
        int: sum of delays"""

    return sum([(L[i].oid(), L[i].oquant()) for i in range(len(L) - 1) if L[i].oid() > L[i + 1].oid()])

def random_swapper(solns) -> list:
    """Randomly swap two orders
    Parameters:
        solns (list): list of solns
    Returns:
        list: new list of orders"""

    L = solns[0]

    i, j = randrange(0, len(L)), randrange(0, len(L)) 
    L[i], L[j] = L[j], L[i]

    return L

def read_json(filepath) -> dict:
    """Reads a JSON file
    Parameters:
        filepath (str): path to the JSON data file
    Returns:
        dict: file contents as a dict"""

    data = None

    with open(filepath, 'r') as f:
        data = json.load(f)

    return data

def main():
    orders = read_json('./Data/orders.json')

    L = []

    for o_id, o in orders.items():
        ord_obj = Order(int(o_id), o['priority'], o['product'], o['quantity'])
        L.append(ord_obj)


main()