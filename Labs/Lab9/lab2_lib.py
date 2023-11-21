# Copyright **`(c)`** 2023 Antonio Ferrigno `<s316467@polito.it>`  
# [`https://github.com/s316467/Computational-Intelligence-23-24/tree/main`](https://github.com/s316467/Computational-Intelligence-23-24/tree/main)  
# Free for personal or classroom use; see [`LICENSE.md`](https://github.com/s316467/Computational-Intelligence-23-24/tree/main/LICENSE.md) for details.  

from abc import abstractmethod

class AbstractProblem:
    def __init__(self):
        self._calls = 0

    @property
    @abstractmethod
    def x(self):
        pass

    @property
    def calls(self):
        return self._calls

    @staticmethod
    def onemax(genome):
        return sum(bool(g) for g in genome)

    def __call__(self, genome):
        self._calls += 1
        fitnesses = sorted((AbstractProblem.onemax(genome[s::self.x]) for s in range(self.x)), reverse=True)
        val = fitnesses[0] - sum(f*(.1 ** (k+1)) for k, f in enumerate(fitnesses[1:]))
        return val / len(genome) * self.x

def make_problem(a):
    class Problem(AbstractProblem):
        @property
        @abstractmethod
        def x(self):
            return a

    return Problem()

