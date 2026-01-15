import highspy
from owlipy.types import VarType, ModelStatus, ModelParams


HIGHS_VAR = {
    VarType.CONTINUOUS: highspy.HighsVarType.kContinuous,
    VarType.BINARY: highspy.HighsVarType.kInteger,
    VarType.INTEGER: highspy.HighsVarType.kInteger,
}

HIGHS_MODEL_STATUS = {
    highspy.HighsModelStatus.kOptimal: ModelStatus.OPTIMAL,
    highspy.HighsModelStatus.kInfeasible: ModelStatus.INFEASIBLE,
    highspy.HighsModelStatus.kUnbounded: ModelStatus.UNBOUNDED,
    highspy.HighsModelStatus.kUnknown: ModelStatus.UNKNOWN,
}

HIGHS_PARAMS = {
    ModelParams.MIPGAP: "mip_rel_gap",
    ModelParams.VERBOSE: "output_flag",
    ModelParams.MIPGAPABS: "mip_abs_gap",
    ModelParams.TIMELIMIT: "time_limit",
}
