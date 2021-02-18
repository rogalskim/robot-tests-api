import time

from typing import Any

import requests
import requests_mock


class MockConstants:
    fail_key = "mock_fail"
    true = "True"
    false = "False"


def should_response_fail(request: requests.Request) -> bool:
    if MockConstants.fail_key not in request.headers.keys():
        return False
    return request.headers[MockConstants.fail_key] == MockConstants.true


def get_modification_timestamp(request: requests.Request, context: Any) -> str:
    if should_response_fail(request):
        context.status_code = requests.codes.not_found
    else:
        context.status_code = requests.codes.ok

    current_time = str(int(time.time()))
    return current_time


def make_mock_server_adapter(address_scheme: str, server_address: str) -> requests_mock.Adapter:
    mock_adapter = requests_mock.Adapter()
    full_address = address_scheme + "://" + server_address

    mock_adapter.register_uri(method="GET",
                              url=full_address + "/info",
                              text=get_modification_timestamp)

    return mock_adapter
