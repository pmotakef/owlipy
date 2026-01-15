from owlipy.types import ModelStatus, ModelParams
from hexaly.optimizer import HxSolutionStatus


HEXALY_MODEL_STATUS = {
    HxSolutionStatus.OPTIMAL: ModelStatus.OPTIMAL,
    HxSolutionStatus.INFEASIBLE: ModelStatus.INFEASIBLE,
    HxSolutionStatus.INCONSISTENT: ModelStatus.UNBOUNDED,
}
