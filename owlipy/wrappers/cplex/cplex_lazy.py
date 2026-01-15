import cplex
from cplex.callbacks import LazyConstraintCallback, BranchCallback, HeuristicCallback, MIPInfoCallback
from docplex.mp.callbacks.cb_mixin import ConstraintCallbackMixin, ModelCallbackMixin
from owlipy.types import BranchSearchOutput


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


class DOBranchSearchCallback(ModelCallbackMixin, BranchCallback):
    def __init__(self, env):
        BranchCallback.__init__(self, env)
        ModelCallbackMixin.__init__(self)
        self.callback_fn: callable = lambda x, y, z: [BranchSearchOutput()]
        self.model_vars = {}
        self.heuristic_pruning = False

    def __call__(self):
        # Fetch variable values into a solution object
        if self.is_integer_feasible():
            return

        node_data = self.get_node_data()
        if node_data:
            branches: list[BranchSearchOutput] = node_data.pop(0)
            if node_data:
                branches[-1].node_data = node_data
        else:
            sol = self.make_solution()
            branch_vars = []
            if self.get_branch_type() == self.branch_type.variable:
                for i in range(self.get_num_branches()):
                    b = self.get_branch(i)
                    for v_idx, _, _ in b[1]:
                        v = self.index_to_var(v_idx)
                        v_name = v.name
                        if v_name not in branch_vars:
                            branch_vars.append(v_name)
            branches: list[BranchSearchOutput] = self.callback_fn(sol, self.model_vars, branch_vars)

        if branches is None:
            self.prune()
            return

        for bso in branches:
            bso_vars = [(v.var_name, v.dir.value, v.bound) for v in bso.variables] if bso.variables is not None else None
            bso_const = [(cplex.SparsePair(ind=c.var_name, val=c.var_val), c.sense, c.rhs) for c in bso.constraints] if bso.constraints is not None else None
            self.make_branch(
                objective_estimate=self.get_objective_value(),
                variables=bso_vars, constraints=bso_const, node_data=bso.node_data,
            )
        if self.heuristic_pruning:
            self.prune()


class DOHeuristicCallback(ModelCallbackMixin, HeuristicCallback):
    def __init__(self, env):
        HeuristicCallback.__init__(self, env)
        ModelCallbackMixin.__init__(self)
        self.callback_fn: callable = lambda x, y: 0
        self.model_vars = {}

    def __call__(self):
        '''
        solution is either an instance of SparsePair or a sequence of
        length two.  If it is a sequence, the first entry is a
        sequence of variable indices or names whose values are to be
        changed and the second entry is a sequence of floats with the
        corresponding new solution values.  Variables whose indices
        are not specified remain unchanged.
        '''
        # Fetch variable values into a solution object
        feas = self.get_feasibilities()
        var_indices = [j for j, f in enumerate(feas) if f == self.feasibility_status.feasible]
        sol = self.make_solution()
        solution = self.callback_fn(sol, self.model_vars)
        if solution is not None:
            self.set_solution(solution)
