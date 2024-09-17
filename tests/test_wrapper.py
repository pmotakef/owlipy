import pytest

from owlipy.types import (
    ModelParams,
    ModelStatus,
    ObjSense,
    Solvers,
    VarType,
)
from owlipy.owl import get_solver_model


class TestWrapper:
    @pytest.mark.gurobi
    def test_gurobi_wrapper(self):
        model = get_solver_model(Solvers.GUROBI)
        model.create_model(name="test")
        x = model.add_var(name="x", var_type=VarType.CONTINUOUS, lb=0, ub=1)
        y = model.add_var(name="y", var_type=VarType.CONTINUOUS, lb=0, ub=10)

        model.set_objective(x + (2 * y), ObjSense.MAX)
        status = model.solve()

        if status == ModelStatus.OPTIMAL:
            xv = model.get_value(x)
            yv = model.get_value(y)

            assert xv > 0
            assert yv > 0

    def test_highs_wrapper(self):
        model = get_solver_model(Solvers.HIGHS)
        model.create_model(name="test")
        x = model.add_var(name="x", var_type=VarType.CONTINUOUS, lb=0, ub=1)
        y = model.add_var(name="y", var_type=VarType.CONTINUOUS, lb=0, ub=10)

        model.set_objective(x + (2 * y), ObjSense.MAX)
        status = model.solve()

        if status == ModelStatus.OPTIMAL:
            xv = model.get_value(x)
            yv = model.get_value(y)

            assert xv > 0
            assert yv > 0

    @pytest.mark.cplex
    def test_cplex_wrapper(self):
        model = get_solver_model(Solvers.CPLEX)
        model.create_model(name="test")
        x = model.add_var(name="x", var_type=VarType.CONTINUOUS, lb=0, ub=1)
        y = model.add_var(name="y", var_type=VarType.CONTINUOUS, lb=0, ub=10)

        model.set_objective(x + (2 * y), ObjSense.MAX)
        status = model.solve()

        if status == ModelStatus.OPTIMAL:
            xv = model.get_value(x)
            yv = model.get_value(y)

            assert xv > 0
            assert yv > 0

    @pytest.mark.cplex
    def test_cplex_iis(self):
        model = get_solver_model(Solvers.CPLEX)
        model.create_model(name="test")
        x = model.add_var(name="x", var_type=VarType.CONTINUOUS, lb=0, ub=1)
        y = model.add_var(name="y", var_type=VarType.CONTINUOUS, lb=0, ub=10)

        model.add_constraint(x >= 3, name="const1")
        model.add_constraint(x <= 2, name="const1")

        model.set_objective(x + (2 * y), ObjSense.MAX)
        status = model.solve()

        assert status == ModelStatus.INFEASIBLE
        iis = model.compute_iis(output_file_path=None)
        assert iis is not None

    @pytest.mark.cplex
    def test_cplex_sum(self):
        model = get_solver_model(Solvers.CPLEX)
        model.create_model(name="test")
        time_slots = [i for i in range(10)]
        x = model.add_vars(time_slots, name="x", var_type=VarType.CONTINUOUS, lb=0, ub=1)
        y = model.add_vars(time_slots, name="y", var_type=VarType.CONTINUOUS, lb=0, ub=10)

        y2 = [y[t] for t in time_slots]

        model.set_objective(model.get_sum(x) + (2 * model.get_sum(y2)), ObjSense.MAX)
        status = model.solve()

        assert status == ModelStatus.OPTIMAL
        assert model.get_value(x[0]) > 0
        assert model.get_value(y[0]) > 0

    @pytest.mark.cplex
    def test_cplex_inner_op(self):
        model = get_solver_model(Solvers.CPLEX)
        model.create_model(name="test")
        time_slots = [i for i in range(10)]
        x = model.add_vars(time_slots, name="x", var_type=VarType.CONTINUOUS, lb=0, ub=1)
        y = model.add_vars(time_slots, name="y", var_type=VarType.CONTINUOUS, lb=0, ub=10)

        m = [1, 2, 4, 2, 2, 1, 2, 3, 5, 6]
        model.set_objective(model.get_sum(model.inner_op(x, model.inner_op(m, y, "*"), "+")), ObjSense.MAX)
        status = model.solve()

        assert status == ModelStatus.OPTIMAL
        assert model.get_value(x[0]) > 0
        assert model.get_value(y[0]) > 0

    @pytest.mark.gurobi
    def test_gurobi_sum(self):
        model = get_solver_model(Solvers.GUROBI)
        model.create_model(name="test")
        time_slots = [i for i in range(10)]
        x = model.add_vars(time_slots, name="x", var_type=VarType.CONTINUOUS, lb=0, ub=1)
        y = model.add_vars(time_slots, name="y", var_type=VarType.CONTINUOUS, lb=0, ub=10)

        y2 = [y[t] for t in time_slots]

        model.set_objective(model.get_sum(x) + (2 * model.get_sum(y2)), ObjSense.MAX)
        status = model.solve()

        assert status == ModelStatus.OPTIMAL
        assert model.get_value(x[0]) > 0
        assert model.get_value(y[0]) > 0

    @pytest.mark.gurobi
    def test_gurobi_inner_op(self):
        model = get_solver_model(Solvers.GUROBI)
        model.create_model(name="test")
        time_slots = [i for i in range(10)]
        x = model.add_vars(time_slots, name="x", var_type=VarType.CONTINUOUS, lb=0, ub=1)
        y = model.add_vars(time_slots, name="y", var_type=VarType.CONTINUOUS, lb=0, ub=10)

        m = [1, 2, 4, 2, 2, 1, 2, 3, 5, 6]
        model.set_objective(model.get_sum(model.inner_op(x, model.inner_op(m, y, "*"), "+")), ObjSense.MAX)
        status = model.solve()

        assert status == ModelStatus.OPTIMAL
        assert model.get_value(x[0]) > 0
        assert model.get_value(y[0]) > 0

    @pytest.mark.cplex
    def test_cplex_mip(self):
        # no mip gap is set, the default must be used which is 1e-4
        # problem can be found here: https://github.com/cswaroop/cplex-samples/blob/master/mipex1.py
        model = get_solver_model(Solvers.CPLEX)
        model.create_model(name="test")
        x1 = model.add_var(name="x1", var_type=VarType.INTEGER, lb=0, ub=40)
        x2 = model.add_var(name="x2", var_type=VarType.INTEGER, lb=0)
        x3 = model.add_var(name="x3", var_type=VarType.INTEGER, lb=0)
        x4 = model.add_var(name="x4", var_type=VarType.INTEGER, lb=2, ub=3)

        model.add_constraint(-x1 + x2 + x3 + 10 * x4 <= 20, name="const1")
        model.add_constraint(x1 - 3 * x2 + x3 <= 2, name="const2")
        model.add_constraint(x2 - 3.5 * x4 == 0, name="const3")

        model.set_objective(x1 + 2 * x2 + 3 * x3 + x4, sense=ObjSense.MAX)

        status1 = model.solve()

        assert status1 == ModelStatus.OPTIMAL
        assert model.model.cplex.parameters.mip.tolerances.mipgap.get() == 1e-4

        # now set a bigger mip gap
        model.set_parameter(ModelParams.MIPGAP, 1e-1)

        status2 = model.solve()
        assert status2 == ModelStatus.OPTIMAL
        assert model.model.cplex.parameters.mip.tolerances.mipgap.get() == 0.1

    @pytest.mark.gurobi
    def test_gurobi_mip(self):
        # no mip gap is set, the default must be used which is 1e-4
        # problem can be found here: https://github.com/cswaroop/cplex-samples/blob/master/mipex1.py
        model = get_solver_model(Solvers.GUROBI)
        model.create_model(name="test")
        x1 = model.add_var(name="x1", var_type=VarType.INTEGER, lb=0, ub=40)
        x2 = model.add_var(name="x2", var_type=VarType.INTEGER, lb=0)
        x3 = model.add_var(name="x3", var_type=VarType.INTEGER, lb=0)
        x4 = model.add_var(name="x4", var_type=VarType.INTEGER, lb=2, ub=3)

        model.add_constraint(-x1 + x2 + x3 + 10 * x4 <= 20, name="const1")
        model.add_constraint(x1 - 3 * x2 + x3 <= 2, name="const2")
        model.add_constraint(x2 - 3.5 * x4 == 0, name="const3")

        model.set_objective(x1 + 2 * x2 + 3 * x3 + x4, sense=ObjSense.MAX)

        status1 = model.solve()

        assert status1 == ModelStatus.OPTIMAL
        assert model.model.Params.MIPGap == 1e-4

        # now set a bigger mip gap
        model.set_parameter(ModelParams.MIPGAP, 1e-1)

        status2 = model.solve()
        assert status2 == ModelStatus.OPTIMAL
        assert model.model.Params.MIPGap == 0.1

    def test_debug(self):
        model = get_solver_model(Solvers.DEBUG)
        x1 = model.add_var(var_type=VarType.CONTINUOUS, name="x1", lb=0, ub=None)
        x2 = model.add_var(var_type=VarType.CONTINUOUS, name="x2", lb=0, ub=None)
        model.add_constraint(x1 - 2 * x2 + 2 >= 0, name="c1")
        model.add_constraint(-x1 - 2 * x2 >= -6, name="c2")
        model.add_constraint(x1 <= 2 * x2 + 2, name="c3")
        model.add_constraint(x1 == 2 * x2, name="c4")
        model.set_objective((x1 - 1) ** 2 + (x2 - 2.5) ** 2)

        assert model.model.constrs["c4"].replace({"x1": 2, "x2": 1}) == 0
        assert model.model.constrs_type["c4"] == "eq"
        assert model.model.constrs_type["c3"] == "ineq"
        assert model.model.bounds["x1"][0] == 0
        assert model.model.bounds["x1"][1] is None
