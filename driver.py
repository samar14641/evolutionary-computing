import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from evo import Environment
from mpl_toolkits.mplot3d import Axes3D
from order import Order
from pprint import pprint
from random import randrange, shuffle


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

    return sum([L[i].oquant() for i in range(len(L) - 1) if L[i].oid() > L[i + 1].oid()])

def random_swapper(solns: list) -> list:
    """Randomly swap two orders
    Parameters:
        solns (list): list of solns
    Returns:
        list: new list of orders"""

    L = solns[0]

    i, j = randrange(0, len(L)), randrange(0, len(L)) 
    L[i], L[j] = L[j], L[i]

    return L

def priority_swapper(solns: list) -> list:  # try to minimise low_priority
    """Swap orders based on priority
    Parameters:
        solns (list): list of solns
    Returns:
        list: new list of orders"""

    L = solns[0]

    high_priority = [o for o in L if o.oprior() == Order.PRIOR_MAP['HIGH']]
    low_priority = [o for o in L if o.oprior() == Order.PRIOR_MAP['LOW']]

    return high_priority + low_priority

def product_swapper(solns: list) -> list:  # try to minimise setups
    """Swap orders based on product
    Parameters:
        solns (list): list of solns
    Returns:
        list: new list of orders"""

    L = solns[0]
    soln = []

    _ = [soln.extend(s) for s in [[o for o in L if o.oprod() == prod] for prod in Order.PRODUCTS]]

    return soln

def id_swapper(solns: list) -> list:  # try to minimise delays:
    """Swap orders based on ID
    Parameters:
        solns (list): list of solns
    Returns:
        list: new list of orders"""

    L = solns[0]

    return [Order(i, pri, pro, q) for i, pri, pro, q in sorted([o.get_props() for o in L], key = lambda x: x[0])]

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

    # shuffle(L)

    E = Environment()

    E.add_fitness('setups', setups)
    E.add_fitness('low_priority', low_priority)
    E.add_fitness('delays', delays)

    E.add_agent('random_swapper', random_swapper, 1)
    E.add_agent('priority_swapper', priority_swapper, 1)
    E.add_agent('product_swapper', product_swapper, 1)
    E.add_agent('id_swapper', id_swapper, 1)

    E.add_solution(L)

    E.evolve(100000)
    
    df = pd.DataFrame(E.get_scores())
    for i in range(df.shape[1]):
        df[i] = df[i].apply(lambda x: x[1])

    df.rename(columns = {0: 'Setups', 1: 'High-LastIndex', 2: 'Delays'}, inplace = True)

    pprint(df)

    # sns.pairplot(df, corner = True)
    # plt.show()
    # plt.close()

    # ax3d = Axes3D(plt.figure())
    # ax3d.scatter(df['Setups'], df['High-LastIndex'], df['Delays'], c = '#552583')
    # ax3d.set_title('Tradeoffs')
    # ax3d.set_xlabel('Setups')
    # ax3d.set_ylabel('High-LastIndex')
    # ax3d.set_zlabel('Delays')
    # plt.show()
    # plt.close()

    df['TeamName'] = 'Samar'

    df.to_csv('./summary.csv', index = False)


main()
