from docplex.util.status import JobSolveStatus
from owlipy.types import ModelStatus

STATUS_MAPPING = {
    JobSolveStatus.UNKNOWN.name: ModelStatus.UNKNOWN,
    # JobSolveStatus.FEASIBLE_SOLUTION.name: ModelStatus.FEASIBLE,
    JobSolveStatus.OPTIMAL_SOLUTION.name: ModelStatus.OPTIMAL,
    JobSolveStatus.INFEASIBLE_SOLUTION.name: ModelStatus.INFEASIBLE,
    JobSolveStatus.UNBOUNDED_SOLUTION.name: ModelStatus.UNBOUNDED,
    JobSolveStatus.INFEASIBLE_OR_UNBOUNDED_SOLUTION.name: ModelStatus.INFEASIBLE,
}
