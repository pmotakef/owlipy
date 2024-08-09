import logging

import symbolipy.symbol_interface

from owlipy.types import (
    ModelStatus,
    ObjSense,
    ScipyConstrType,
    ScipySolvers,
    VarType,
)
from owlipy.exceptions import SolverException
from owlipy.owl_interface import OwlInterface
from symbolipy import Symbol


class ScipyModel:
    def __init__(self, name: str | None = None):
        self.name = name
        self.vars = {}
        self.constrs = {}
        self.constrs_type = {}
        self.bounds = {}
        self.start = {}
        self.obj_fn = 0
        self.solver_type = ScipySolvers.AUTO


class OptDebugWrapper(OwlInterface):
    def __init__(self):
        super(OptDebugWrapper, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.model = ScipyModel()
        self.solution = None

    def create_model(self, name: str = "debug"):
        self.model.name = name

    def add_var(self, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = None, ub: float = None, start: float = None):
        if name in self.model.vars:
            raise SolverException(f"Variable: {name} already defined.")
        var_symbol = Symbol(name.replace(",", "_").replace(" ", ""))

        self.model.bounds[name] = (lb, ub)
        self.model.vars[name] = var_symbol
        self.model.start[name] = 0 if start is None else start
        return var_symbol

    def add_vars(self, indices: list, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = None, ub: float = None, start: list[float] = None):
        all_vars = {}
        for i in indices:
            all_vars[i] = self.add_var(var_type=var_type, name=f"{name}_{i}", lb=lb, ub=ub, start=start[i] if start is not None else None)
        return all_vars

    def add_constraint(self, expr, name: str):
        if name in self.model.constrs:
            raise SolverException(f"Constraint: {name} already defined.")

        cleaned_expr = expr
        constr_type = ScipyConstrType.INEQUAL
        if isinstance(expr, symbolipy.symbol_interface.Eq):
            cleaned_expr = expr.lhs - expr.rhs
            constr_type = ScipyConstrType.EQUAL
        elif isinstance(expr, (symbolipy.symbol_interface.Gr | symbolipy.symbol_interface.GrEq | symbolipy.symbol_interface.Ls | symbolipy.symbol_interface.LsEq)):
            if ">" in expr.op:
                cleaned_expr = expr.lhs - expr.rhs
            else:
                cleaned_expr = expr.rhs - expr.lhs

        self.model.constrs[name] = cleaned_expr
        self.model.constrs_type[name] = constr_type.value

    def add_constraints(self, exprs: list | tuple, name: str):
        for i in range(len(exprs)):
            self.add_constraint(exprs[i], name=f"{name}_{i}")

    def set_objective(self, expr, sense: ObjSense = ObjSense.MIN):
        if expr is None:
            if self == ObjSense.MAX:
                self.model.obj_fn *= -1
        else:
            self.model.obj_fn = expr if sense == ObjSense.MIN else -expr

    def add_partial_objective(self, expr):
        self.model.obj_fn += expr

    def solve(self) -> ModelStatus:
        return ModelStatus.OPTIMAL

    def get_value(self, var_name):
        return None

    def get_values(self, variables: list) -> list:
        return []

    def get_sum(self, variables: list | dict):
        if isinstance(variables, list):
            return sum(variables)
        return sum(variables.values())
