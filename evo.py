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

    @staticmethod
    def _dominates(p, q) -> bool:
        """Check if solution q dominates p
        Parameters:
            p (tuple): evaluation of soln p i.e. ((objective1, score1), (objective2, score2), ...)
            q (tuple): evaluation of soln q
        Returns:
            bool: whether q dominates p or not"""

        p_scores = [score for _, score in p]
        q_scores = [score for _, score in q]

        score_diff = list(map(lambda x, y: y - x, p_scores, q_scores))
        
        min_diff, max_diff = min(score_diff), max(score_diff)

        return min_diff >= 0.0 and max_diff > 0

    @staticmethod
    def _reduce_non_dom(S, p) -> set:
        """Create the non-dominated set of solutions
        Parameters:
            S (set): evaluation of all solutions for pairwise comparison with p
            p (set): evaluation of all solutions for pairwise comparison with each solution q in S
        Returns:
            set: the set of non-dominated solutions"""

        return S - {q for q in S if Environment._dominates(p, q)}

    def remove_dominated(self) -> None:
        """Remove dominated solutions from the population
        Returns:
            None"""

        non_dom_set = reduce(Environment._reduce_non_dom, self.pop.keys(), self.pop.keys())

        self.pop = {k: self.pop[k] for k in non_dom_set}

    def evolve(self, iters, dom = 100, status = 1000) -> None:
        """Simulate the environment
        Parameters:
            iters (int): number of iterations
            dom (int): interval to remove solutions
            status (int): interval to print stats"""

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

    def get_population(self) -> dict:
        """Retrieve the population
        Returns:
            dict: the population"""

        return self.pop