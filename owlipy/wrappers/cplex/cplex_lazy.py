from cplex.callbacks import LazyConstraintCallback
from docplex.mp.callbacks.cb_mixin import ConstraintCallbackMixin


class DOLazyCallback(ConstraintCallbackMixin, LazyConstraintCallback):
    def __init__(self, env):
        LazyConstraintCallback.__init__(self, env)
        ConstraintCallbackMixin.__init__(self)
        self.callback_fn: callable = lambda x, y: 0
        self.model_vars = {}

    def __call__(self):
        # Fetch variable values into a solution object
        sol = self.make_solution()
        cst_list = self.callback_fn(sol, self.model_vars)
        unsats = self.get_cpx_unsatisfied_cts(cst_list, sol, tolerance=1e-6)
        for ct, cpx_lhs, sense, cpx_rhs in unsats:
            self.add(cpx_lhs, sense, cpx_rhs)
