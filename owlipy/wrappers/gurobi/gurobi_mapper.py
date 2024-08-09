try:
    import gurobipy
except ImportError:
    raise ValueError("The package gurobipy not installed.")

from owlipy.types import ModelParams, ModelStatus, ObjSense, VarType

VAR_MAPPING = {
    VarType.CONTINUOUS: gurobipy.GRB.CONTINUOUS,
    VarType.INTEGER: gurobipy.GRB.INTEGER,
    VarType.BINARY: gurobipy.GRB.BINARY,
}

SENSE_MAPPING = {
    ObjSense.MIN: gurobipy.GRB.MINIMIZE,
    ObjSense.MAX: gurobipy.GRB.MAXIMIZE
}

STATUS_MAPPING = {
    gurobipy.GRB.Status.OPTIMAL: ModelStatus.OPTIMAL,
    gurobipy.GRB.Status.INFEASIBLE: ModelStatus.INFEASIBLE,
    gurobipy.GRB.status.INF_OR_UNBD: ModelStatus.UNKNOWN,
    gurobipy.GRB.status.UNBOUNDED: ModelStatus.UNBOUNDED,
}

PARAMS_MAPPINGS = {
    ModelParams.VERBOSE: "OutputFlag",
    ModelParams.TIMELIMIT: gurobipy.GRB.Param.TimeLimit,
    ModelParams.MIPGAP: gurobipy.GRB.Param.MIPGap,
    ModelParams.MIPGAPABS: gurobipy.GRB.Param.MIPGapAbs
}


VAL_INF = gurobipy.GRB.INFINITY
