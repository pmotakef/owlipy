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
    ModelParams.MIPGAP: highspy.HighsOptions.mip_rel_gap,
    ModelParams.VERBOSE: highspy.HighsOptions.output_flag,
    ModelParams.MIPGAPABS: highspy.HighsOptions.mip_abs_gap,
    ModelParams.TIMELIMIT: highspy.HighsOptions.time_limit,
}
