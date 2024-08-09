from enum import Enum


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
    DEBUG = 100


class ModelParams(Enum):
    VERBOSE = "verbose"
    TIMELIMIT = "time_limit"
    MIPGAP = "mip_gap"
    MIPGAPABS = "mip_gap_abs"
    SCIPY_SOLVER_TYPE = "scipy_solver"


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
