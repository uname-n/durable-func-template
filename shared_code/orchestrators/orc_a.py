from logging import getLogger

debugger = getLogger("orc_a")

from azure.durable_functions import DurableOrchestrationContext

from shared_code.context import Context
from shared_code.app import app


@app.orchestration_trigger(context_name="context")
def orc_a(context: DurableOrchestrationContext) -> dict:  # type: ignore
    request: Context = Context.parse_raw(context.get_input())  # type: ignore

    return dict(response="orc_a")
