import requests

from exceptions import ExecutionError
from server_mock import make_mock_server_adapter
from server_mock import MockConstants


class ClientSession:
    def __init__(self, host: str, port: int, fail_request: bool) -> None:
        self._session = requests.session()
        self._address_scheme = "https-mock"
        self._server_address = f"{host}:{port}"
        mock_adapter = make_mock_server_adapter(self._address_scheme, self._server_address)
        self._session.mount(prefix=self._address_scheme, adapter=mock_adapter)

        if fail_request:
            header = {MockConstants.fail_key: MockConstants.true}
        else:
            header = {MockConstants.fail_key: MockConstants.false}

        response = self._session.get(f"{self._address_scheme}://{self._server_address}/info",
                                     headers=header)
        if response.ok:
            self._last_server_modification = int(response.text)
        else:
            raise ExecutionError(f"HTTP request failed: {response.status_code}")

    def get_address(self) -> str:
        return f"{self._address_scheme}://{self._server_address}"

    def get_server_modification_time(self) -> int:
        return 5
