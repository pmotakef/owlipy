import logging
from hexaly.optimizer import HexalyOptimizer, HxExpression
from owlipy.types import ModelParams, ModelStatus, ObjSense, VarType
from owlipy.exceptions import SolverException
from owlipy.owl_interface import OwlInterface
from owlipy.wrappers.hexaly.hexaly_mapper import HEXALY_MODEL_STATUS
INF = 10000


class OptHexalyWrapper(OwlInterface):
    def __init__(self):
        super(OptHexalyWrapper).__init__()
        self.logger = logging.getLogger(__name__)
        self.optimizer = HexalyOptimizer()
        self.model = self.optimizer.model
        self.partial_objective_fn = None
        self.model_sense = ObjSense.MIN
        self.vars = {}

    def reset_model(self):
        self.partial_objective_fn = None
        self.model_sense = ObjSense.MIN

    def create_model(self, name: str = None):
        self.reset_model()
        self.optimizer = HexalyOptimizer()
        self.model = self.optimizer.model
        self.logger.info(f"created gurobi model {name}")

    def add_var(self, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = 0, ub: float = INF, start: float = None):
        if var_type == VarType.BINARY:
            v = self.model.bool()
        elif var_type == VarType.INTEGER:
            v = self.model.int(lb, ub)
        else:
            v = self.model.float(lb, ub)
        self.vars[name] = v
        return v

    def add_vars(self, indices: list, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = 0, ub: float = INF, start: list[float] = None):
        added_vars = {}
        for i, idx in enumerate(indices):
            h_start = None
            if start is not None:
                h_start = start[i]
            added_vars[idx] = self.add_var(name=f"{name}_{str(idx)}", var_type=var_type, lb=lb, ub=ub, start=h_start)
        return added_vars

    def add_constraint(self, expr, name: str):
        if isinstance(expr, (bool, int, float, str)):
            return
        self.model.constraint(expr)

    def add_constraints(self, exprs: list | tuple, name: str):
        for i, expr in enumerate(exprs):
            if not isinstance(expr, (bool, int, float, str)):
                self.add_constraint(expr, name=f"{name}_{i}")

    def set_objective(self, expr=None, sense: ObjSense = ObjSense.MIN):
        if self.partial_objective_fn is None:
            self.partial_objective_fn = expr
        else:
            self.partial_objective_fn = self.partial_objective_fn + expr
        self.model_sense = sense

    def add_to_objective(self, expr):
        """
        Adds Partial objective to the model ensemble

        :param expr: Expression
        """
        if self.partial_objective_fn is None:
            self.partial_objective_fn = expr
        else:
            self.partial_objective_fn += expr

    def solve(self) -> ModelStatus:
        if self.model_sense == ObjSense.MIN:
            self.model.minimize(self.partial_objective_fn)
        else:
            self.model.maximize(self.partial_objective_fn)
        self.model.close()
        self.optimizer.solve()
        model_status = self.optimizer.solution.status
        return HEXALY_MODEL_STATUS[model_status]

    def get_value(self, var_name: str | HxExpression):
        if isinstance(var_name, str):
            return self.vars[var_name].value
        return var_name.value

    def set_parameter(self, k: ModelParams, v):
        if k == ModelParams.TIMELIMIT:
            self.optimizer.param.time_limit = v

    def get_sum(self, variables: list | dict):
        if isinstance(variables, dict):
            return self.model.sum(list(variables.values()))
        return self.model.sum(variables)

    def inner_op(self, vars1: list | dict, vars2: list | dict, operation: str = "+") -> list:
        vars1_ls = vars1 if isinstance(vars1, list) else list(vars1.values())
        vars2_ls = vars2 if isinstance(vars2, list) else list(vars2.values())

        if len(vars1_ls) != len(vars2_ls):
            raise SolverException("Length mismatch between vars1 and vars2.")

        res = []
        for i in range(len(vars2_ls)):
            if operation == "+":
                res.append(vars1_ls[i] + vars2_ls[i])
            elif operation == "-":
                res.append(vars1_ls[i] - vars2_ls[i])
            elif operation == "*":
                res.append(vars1_ls[i] * vars2_ls[i])
            elif operation == "/":
                res.append(vars1_ls[i] / vars2_ls[i])
        return res
