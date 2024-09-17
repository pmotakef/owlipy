import logging

import docplex.mp.conflict_refiner as cr
from docplex.mp.constr import AbstractConstraint
from docplex.mp.model import Model

from owlipy.types import ModelParams, ModelStatus, ObjSense, VarType
from owlipy.exceptions import SolverException
from owlipy.owl_interface import OwlInterface


class OptCplexWrapper(OwlInterface):
    def __init__(self):
        super(OptCplexWrapper).__init__()
        self.logger = logging.getLogger(__name__)
        self.model = Model()
        self.env = None
        self.solution = None
        self.objective_fn = 0
        self.verbose = False
        self.quality_metrics = True

    def set_env(self, **kwargs):
        self.env = None

    def create_model(self, name: str = "cplex opt"):
        self.model = Model(name=name)
        self.model.quality_metrics = self.quality_metrics
        self.logger.info(f"created cplex model {name}")

    def add_var(self, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = None, ub: float = None, start: float = None):
        if ub is None:
            ub = self.model.infinity if var_type != VarType.BINARY else 1
        if lb is None:
            lb = 0
        v = None
        if var_type == VarType.BINARY:
            v = self.model.binary_var(name=name)
        elif var_type == VarType.INTEGER:
            v = self.model.integer_var(lb=lb, ub=ub, name=name)
        elif var_type == VarType.CONTINUOUS:
            v = self.model.continuous_var(lb=lb, ub=ub, name=name)
        return v

    def add_vars(self, indices: list, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = None, ub: float = None, start: list[float] = None):
        if ub is None:
            ub = self.model.infinity if var_type != VarType.BINARY else 1
        if lb is None:
            lb = 0
        v = None
        if var_type == VarType.BINARY:
            v = self.model.binary_var_dict(keys=indices, name=name)
        elif var_type == VarType.INTEGER:
            v = self.model.integer_var_dict(keys=indices, lb=lb, ub=ub, name=name)
        elif var_type == VarType.CONTINUOUS:
            v = self.model.continuous_var_dict(keys=indices, lb=lb, ub=ub, name=name)
        return v

    def add_constraint(self, expr, name: str):
        if not isinstance(expr, AbstractConstraint):
            return
        self.model.add_constraint(expr, ctname=name)

    def add_constraints(self, exprs: list | tuple, name: str):
        if not exprs:
            return
        if not isinstance(exprs[0], AbstractConstraint):
            return
        exprs_list = list(exprs)
        names = name
        if not isinstance(name, list):
            names = [f"{name}_{i}" for i in range(len(exprs_list))]
        self.model.add_constraints(exprs_list, names=names)

    def set_objective(self, expr=None, sense: ObjSense = ObjSense.MIN):
        total_obj = self.objective_fn
        if expr is not None:
            total_obj += expr
        if sense == ObjSense.MAX:
            self.model.maximize(total_obj)
        else:
            self.model.minimize(total_obj)

    def solve(self) -> ModelStatus:
        self.solution = self.model.solve(log_output=self.verbose, clean_before_solve=True)
        if self.solution is None:
            status = self.model.solve_details.status_code
            if status == 2:
                return ModelStatus.UNBOUNDED
            elif status == 4:
                return ModelStatus.INFEASIBLE
            # elif status == 3:
            #     return ModelStatus.INFEASIBLE
            return ModelStatus.INFEASIBLE
        return ModelStatus.OPTIMAL

    def compute_iis(self, output_file_path: str | None = None):
        cref = cr.ConflictRefiner()
        if output_file_path is not None:
            cobj = cref.refine_conflict(self.model, display=False)
            cobj.as_output_table(use_df=True).to_csv(output_file_path)
        else:
            return cref.refine_conflict(self.model, display=True)

    def get_value(self, var_name):
        if isinstance(var_name, (int, float)):
            return var_name
        return self.solution.get_value(var_name)

    def get_values(self, variables: list | dict) -> list | dict:
        if isinstance(variables, dict):
            return {k: self.get_value(variables[k]) for k in variables}
        return [self.get_value(v) for v in variables]

    def set_parameter(self, k: ModelParams, v):
        if k == ModelParams.VERBOSE:
            self.model.verbose = v
        if k == ModelParams.TIMELIMIT:
            self.model.set_time_limit(v)
        if k == ModelParams.MIPGAP:
            self.model.parameters.mip.tolerances.mipgap = v
        if k == ModelParams.MIPGAPABS:
            self.model.parameters.mip.tolerances.absmipgap = v

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
