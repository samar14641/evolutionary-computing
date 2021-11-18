import copy

from functools import reduce
from random import choice


class Environment():
    def __init__(self) -> None:
        """Constructor"""

        self.pop = {}  # solutions
        self.fitness = {}  # objective functions
        self.agent = {}  # mutators

    def size(self) -> int:
        """Get population size
        Returns:
            int: number of solutions in population"""

        return len(self.pop)

    def add_fitness(self, name, func) -> None:
        """Add an objective to the environment
        Parameters:
            name (str): function name
            func (method): the objective function
        Returns:
            None"""

        self.fitness[name] = func

    def add_agent(self, name, func, n = 1) -> None:
        """Add an agent to the environment
        Parameters:
            name (str): function name
            func (method): the agent function
            n (int): number of solutions for the agent (default: 1)
        Returns:
            None"""

        self.agent[name] = (func, n)

    def add_solution(self, soln) -> None:
        """Add a solution to the population
        Parameters:
            soln (list): a solution
        Returns:
            None"""

        eval = tuple([(name, func(soln)) for name, func in self.fitness.items()])  # score solution
        self.pop[eval] = soln

    def get_solutions_random(self, n) -> list:
        """Pick n random solutions from the population and return their copies
        Parameters:
            n (int): number of solutions required
        Returns
            list: list of selected solutions"""

        if self.size() == 0:
            return []
        else:
            return [copy.deepcopy(choice(tuple(self.pop.values()))) for _ in range(n)]

    def run_agent(self, name) -> None:
        """Run a selected agent
        Parameters:
            name (str): agent name
        Returns:
            None"""

        func, n = self.agent[name]

        solns = self.get_solutions_random(n)

        self.add_solution(func(solns))

    def remove_dominated(self) -> None:
        """"""

    def evolve(self, iters, dom = 100, status = 1000) -> None:
        """"""

        agents = list(self.agent.keys())

        for i in range(iters):
            agent = choice(agents)
            self.run_agent(agent)

            if i % dom == 0:
                self.remove_dominated()
            if i % status == 0:
                print('Iteration', i)
                print('Population:', self.size())

        self.remove_dominated()