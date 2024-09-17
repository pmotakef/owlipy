import logging

import highspy
from highspy.highs import highs_var

from owlipy.types import ModelParams, ModelStatus, ObjSense, VarType
from owlipy.exceptions import SolverException
from owlipy.wrappers.highs.highs_mapper import (
    HIGHS_VAR, HIGHS_MODEL_STATUS, HIGHS_PARAMS
)
from owlipy.owl_interface import OwlInterface
import numpy


class OptHighsWrapper(OwlInterface):
    def __init__(self):
        super(OptHighsWrapper).__init__()
        self.logger = logging.getLogger(__name__)
        self.model = highspy.Highs()
        # self.env = None
        self.partial_objective_fn = None
        self.model_sense = ObjSense.MIN
        self.solution = None

    # def set_env(self, **kwargs):
    #     self.env = None

    def reset_model(self):
        self.solution = None
        self.partial_objective_fn = None
        self.model_sense = ObjSense.MIN

    def create_model(self, name: str = None):
        self.reset_model()
        self.model = highspy.Highs()
        self.logger.info(f"created gurobi model {name}")

    def add_var(self, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = 0, ub: float = highspy.kHighsInf, start: float = None):
        if var_type == VarType.BINARY:
            ub = 1
            lb = 0
        return self.model.addVariable(lb=lb, ub=ub, type=HIGHS_VAR[var_type], name=name)

    def add_vars(self, indices: list, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = 0, ub: float = highspy.kHighsInf, start: list[float] = None):
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
        self.model.addConstr(expr, name=name)

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
        self.model.run()
        model_status = self.model.getModelStatus()
        return HIGHS_MODEL_STATUS[model_status] if model_status in HIGHS_MODEL_STATUS else None

    # def compute_iis(self, file_path: str | None = None):
    #     try:
    #         self.model.computeIIS()
    #         self.model.write(file_path)
    #     except Exception as e:
    #         raise SolverException(f"{e}- Couldn't compute and save IIS.")
    #     return None

    def get_value(self, var_name: highs_var):
        if self.solution is None:
            self.solution = self.model.getSolution()
        return self.solution.col_value[var_name.index]

    def set_parameter(self, k: ModelParams, v):
        if k in HIGHS_PARAMS:
            self.model.setOptionValue(HIGHS_PARAMS[k], v)
        else:
            self.model.setParam(k, v)

    def get_sum(self, variables: list | dict):
        if isinstance(variables, dict):
            return sum(list(variables.values()))
        return sum(variables)

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
