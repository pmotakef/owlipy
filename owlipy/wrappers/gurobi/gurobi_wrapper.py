import logging

import gurobipy

from owlipy.types import ModelParams, ModelStatus, ObjSense, VarType
from owlipy.exceptions import SolverException
from owlipy.wrappers.gurobi.gurobi_mapper import (
    PARAMS_MAPPINGS,
    SENSE_MAPPING,
    STATUS_MAPPING,
    VAL_INF,
    VAR_MAPPING,
)
from owlipy.owl_interface import OwlInterface


class OptGurobiWrapper(OwlInterface):
    def __init__(self):
        super(OptGurobiWrapper).__init__()
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.env = None
        self.partial_objective_fn = None

    def set_env(self, **kwargs):
        self.env = None

    def create_model(self, name: str = "gurobi opt"):
        if self.env:
            self.model = gurobipy.Model(name=name, env=self.env)
        else:
            self.model = gurobipy.Model(name=name)
        self.logger.info(f"created gurobi model {name}")

    def add_var(self, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = -VAL_INF, ub: float = VAL_INF, start: float = None):
        params = {"name": name, "vtype": VAR_MAPPING[var_type]}
        if var_type != VarType.BINARY:
            params.update({"lb": lb, "ub": ub})
        return self.model.addVar(**params)

    def add_vars(self, indices: list, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = None, ub: float = None, start: list[float] = None):
        params = {"name": name, "vtype": VAR_MAPPING[var_type]}
        if var_type != VarType.BINARY:
            params.update({"lb": lb, "ub": ub})
        return self.model.addVars(indices, **params)

    def add_constraint(self, expr, name: str):
        if isinstance(expr, (bool, int, float, str)):
            return
        self.model.addConstr(expr, name=name)

    def add_constraints(self, exprs: list | tuple, name: str):
        if not exprs or isinstance(exprs[0], (bool, int, float, str)):
            return
        self.model.addConstrs((exprs[i] for i in range(len(exprs))), name=name)

    def set_objective(self, expr=None, sense: ObjSense = ObjSense.MIN):
        self.model.ModelSense = SENSE_MAPPING[sense]
        obj_fn = 0
        if self.partial_objective_fn is not None:
            obj_fn += self.partial_objective_fn
        if expr is not None:
            obj_fn += expr
        self.model.setObjective(obj_fn)

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
        self.model.optimize()
        return STATUS_MAPPING[self.model.status] if self.model.status in STATUS_MAPPING else None

    def compute_iis(self, file_path: str | None = None):
        try:
            self.model.computeIIS()
            self.model.write(file_path)
        except Exception as e:
            raise SolverException(f"{e}- Couldn't compute and save IIS.")
        return None

    def get_value(self, var_name):
        if isinstance(var_name, gurobipy.LinExpr):
            return var_name.getValue()
        elif isinstance(var_name, (int, float)):
            return var_name
        return var_name.getAttr("x")

    def set_param(self, k: ModelParams, v):
        if k in PARAMS_MAPPINGS:
            self.model.setParam(PARAMS_MAPPINGS[k], v)
        else:
            self.model.setParam(k, v)

    def get_sum(self, variables: list | dict):
        if isinstance(variables, dict):
            return gurobipy.quicksum(list(variables.values()))
        return gurobipy.quicksum(variables)

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
