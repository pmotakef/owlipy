from owlipy.types import VarType, ObjSense, ModelStatus, ModelParams


class OwlInterface:
    def __init__(self):
        self.model = None

    def create_model(self, name: str):
        raise NotImplementedError()

    def set_env(self):
        raise NotImplementedError()

    def add_var(self, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = None, ub: float = None, start: float = None):
        raise NotImplementedError()

    def add_vars(self, indices: list, name: str, var_type: VarType = VarType.CONTINUOUS, lb: float = None, ub: float = None, start: list[float] = None):
        raise NotImplementedError()

    def add_constraint(self, expr, name: str):
        raise NotImplementedError()

    def add_constraints(self, exprs: list, name: str):
        raise NotImplementedError()

    def set_objective(self, expr, sense: ObjSense = ObjSense.MIN):
        raise NotImplementedError()

    def add_to_objective(self, expr):
        raise NotImplementedError()

    def solve(self) -> ModelStatus:
        raise NotImplementedError()

    def set_parameter(self, k: ModelParams, v):
        raise NotImplementedError()

    def get_value(self, var_name):
        raise NotImplementedError()

    def get_values(self, var_names: list):
        raise NotImplementedError()

    def compute_iis(self, output_file_path: str | None = None):
        raise NotImplementedError()

    def get_sum(self, variables: list | dict):
        raise NotImplementedError()

    def inner_op(self, vars1: list | dict, vars2: list | dict, operation: str = "+") -> list:
        raise NotImplementedError()
