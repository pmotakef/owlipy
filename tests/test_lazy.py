import pytest

from owlipy.types import (
    ModelParams,
    ModelStatus,
    ObjSense,
    Solvers,
    VarType,
)
from owlipy.owl import get_solver_model
from owlipy.types import BranchSearchOutput, BranchSearchConst, BranchSearchVar, VarDirection, ConstSense


class TestCallbacks:
    @pytest.mark.cplex
    def test_cplex_lazy_constraint(self):

        def lazy_callback(solution, model_vars):
            cstr = []
            var_x = model_vars['x']
            var_y = model_vars['y']
            if solution[var_x] > 0:
                cstr.append(var_x <= 0)
            return cstr

        model = get_solver_model(Solvers.CPLEX)
        model.create_model(name="test")
        x = model.add_var(name="x", var_type=VarType.CONTINUOUS, lb=0, ub=1)
        y = model.add_var(name="y", var_type=VarType.INTEGER, lb=0, ub=10)

        model.set_objective(x + (2 * y), ObjSense.MAX)

        model.setup_lazy_cst_callback(callback_fn=lazy_callback)

        status = model.solve()

        if status == ModelStatus.OPTIMAL:
            xv = model.get_value(x)
            yv = model.get_value(y)

            assert xv == 0
            assert yv > 0

    @pytest.mark.cplex
    def test_cplex_branch_search(self):

        def branch_callback(solution, model_vars):
            print("branch_callback")
            # cstr = []
            var_x = model_vars['x']
            var_y = model_vars['y']
            return BranchSearchOutput(variables=[BranchSearchVar(var_name=var_y, dir=VarDirection.L, bound=1)])

        model = get_solver_model(Solvers.CPLEX)
        model.create_model(name="test")
        x = model.add_var(name="x", var_type=VarType.CONTINUOUS, lb=1, ub=4)
        y = model.add_var(name="y", var_type=VarType.BINARY, lb=0, ub=1)

        model.add_constraint(x <= 2 + 3 * y, name="c1")
        model.add_constraint(x >= 5 * y, name="c2")

        model.set_objective(x, ObjSense.MAX)
        model.set_parameter(ModelParams.VERBOSE, True)

        model.setup_branch_callback(callback_fn=branch_callback, heuristic_pruning=True)

        status = model.solve()

        if status == ModelStatus.OPTIMAL:
            xv = model.get_value(x)
            yv = model.get_value(y)

            assert xv > 0
            assert yv == 0

