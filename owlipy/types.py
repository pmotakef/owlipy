from enum import Enum
from dataclasses import dataclass



class ModelStatus(Enum):
    OPTIMAL = 1
    INFEASIBLE = 2
    UNBOUNDED = 3
    UNKNOWN = 4


class VarType(Enum):
    CONTINUOUS = 1
    INTEGER = 2
    BINARY = 3


class ObjSense(Enum):
    MAX = 1
    MIN = 2


class Solvers(Enum):
    GUROBI = 1
    CPLEX = 2
    HIGHS = 3
    SCIPY = 4
    HEXALY = 5
    DEBUG = 100


class ModelParams(Enum):
    VERBOSE = "verbose"
    TIMELIMIT = "time_limit"
    MIPGAP = "mip_gap"
    MIPGAPABS = "mip_gap_abs"
    SCIPY_SOLVER_TYPE = "scipy_solver"
    MIP_EMPHASIS = "mip_emphasis"
    MIP_FEAS_PUMP = "mip_feas_pump"


class MIPEmphasisParams(Enum):
    BALANCED = 0
    FEASIBILITY = 1
    OPTIMALITY = 2
    BESTBOUND = 3
    HIDDENFEAS = 4


class MIPStrategyHeuristicPump(Enum):
    ALWAYS_OFF = -1
    AUTO = 0
    ALWAYS_ON = 1
    GOOD_FEAS = 2


class ScipyConstrType(Enum):
    INEQUAL = "ineq"
    EQUAL = "eq"


class ScipySolvers(Enum):
    NEDLER_MEAD = "Nelder-Mead"
    POWELL = "Powell"
    CG = "CG"
    BFGS = "BFGS"
    NEWTON_CG = "Newton-CG"
    L_BFGS_B = "L-BFGS-B"
    TNC = "TNC"
    COBYLA = "COBYLA"
    SLSQP = "SLSQP"
    TRUST_CONSTR = "trust-constr"
    DOGLEG = "dogleg"
    TRUST_NCG = "trust-ncg"
    TRUST_EXACT = "trust-exact"
    TRUST_KRYLOV = "trust-krylov"
    AUTO = "Auto"


class VarDirection(Enum):
    L = "L"
    U = "U"


class ConstSense(Enum):
    L = "L"
    G = "G"
    E = "E"


@dataclass
class BranchSearchVar:
    var_name: str | int
    dir: VarDirection
    bound: int


@dataclass
class BranchSearchConst:
    var_name: list[str | int]
    var_vals: list[int]
    sense: ConstSense
    rhs: float


@dataclass
class BranchSearchOutput:
    variables: list[BranchSearchVar] | None = None
    constraints: list[BranchSearchConst] | None = None
    node_data: list | None = None