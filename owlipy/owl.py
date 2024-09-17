from owlipy.types import Solvers
from owlipy.owl_interface import OwlInterface


def get_solver_model(solver_name: Solvers) -> OwlInterface:
    if solver_name == Solvers.GUROBI:
        from owlipy.wrappers.gurobi.gurobi_wrapper import OptGurobiWrapper

        return OptGurobiWrapper()
    elif solver_name == Solvers.CPLEX:
        from owlipy.wrappers.cplex.cplex_wrapper import OptCplexWrapper

        return OptCplexWrapper()

    elif solver_name == Solvers.DEBUG:
        from owlipy.wrappers.debug.debug_wrapper import OptDebugWrapper

        return OptDebugWrapper()

    elif solver_name == Solvers.HIGHS:
        from owlipy.wrappers.highs.highs_wrapper import OptHighsWrapper

        return OptHighsWrapper()
