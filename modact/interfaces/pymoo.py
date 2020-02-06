import numpy as np
from pymoo.model.problem import Problem

import modact.problems as pb


class PymopProblem(Problem):

    def __init__(self, function, map_=map):
        
        if isinstance(function, pb.Problem):
            self.fct = function
        else:
            self.fct = pb.get_problem(function)
        lb, ub = self.fct.bounds()
        n_var = len(lb)
        n_obj = len(self.fct.weights)
        n_constr = len(self.fct.c_weights)
        xl = lb
        xu = ub

        self.weights = np.array(self.fct.weights)
        self.c_weights = np.array(self.fct.c_weights)

        self.map = map_

        super().__init__(n_var=n_var, n_obj=n_obj, n_constr=n_constr, xl=xl, xu=xu)

    def _evaluate(self, x, out, *args, **kwargs):
        f = np.zeros((x.shape[0], self.n_obj))
        g = np.zeros((x.shape[0], self.n_constr))
        res = self.map(self.fct, x)
        for i, fit in enumerate(res):
            f[i, :], g[i, :] = fit
        f *= -1*self.weights
        g *= self.c_weights
        out["F"] = f
        out["G"] = g
