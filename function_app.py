from logging import getLogger

debugger = getLogger("azfn")

from azure.functions import HttpRequest, HttpResponse
from azure.durable_functions import (
    DurableOrchestrationClient,
    DurableOrchestrationContext,
)

from shared_code.orchestrators import orc_a, orc_b, orc_c

from shared_code.context import Context
from shared_code.app import app

from json import dumps, loads


def http_response(data: dict, status_code: int = 200, **kwargs):
    return HttpResponse(
        dumps({**data, **kwargs}, indent=4),
        mimetype="application/json",
        status_code=status_code,
    )


@app.route(route="endpoint")
@app.durable_client_input(client_name="client")
async def endpoint(req: HttpRequest, client: DurableOrchestrationClient) -> HttpResponse:
    req_data = Context(name="alice")

    instance_id = await client.start_new("main_orchestrator", client_input=req_data.json())
    status_response: HttpResponse = client.create_check_status_response(req, instance_id)
    debugger.info(dumps(loads(status_response.get_body()), indent=4))

    response: dict = await client.wait_for_completion_or_create_check_status_response(  # type: ignore
        req, instance_id, timeout_in_milliseconds=100_000
    )

    if type(response) == HttpResponse:
        return response

    return http_response(response, status_code=200)


@app.orchestration_trigger(context_name="context")
def main_orchestrator(context: DurableOrchestrationContext) -> str:  # type: ignore
    request: Context = Context.parse_raw(context.get_input())  # type: ignore

    # serial
    request.response["orc_a"] = yield context.call_sub_orchestrator("orc_a", request.json())  # type: ignore
    request.response["orc_b"] = yield context.call_sub_orchestrator("orc_b", request.json())  # type: ignore
    request.response["orc_c"] = yield context.call_sub_orchestrator("orc_c", request.json())  # type: ignore
    #

    # parallel
    tasks = [
        context.call_sub_orchestrator("orc_a", request.json()),  # type: ignore
        context.call_sub_orchestrator("orc_b", request.json()),  # type: ignore
        context.call_sub_orchestrator("orc_c", request.json()),  # type: ignore
    ]

    results = yield context.task_all(tasks)  # type: ignore

    request.response["orc_a_parallel"] = results[0]
    request.response["orc_b_parallel"] = results[1]
    request.response["orc_c_parallel"] = results[2]
    #

    return request.json()
