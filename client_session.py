import requests

from server_mock import make_mock_server_adapter


class ConnectionFailed(RuntimeError):
    pass


class ClientSession:
    def __init__(self, host: str, port: int) -> None:
        self._session = requests.session()
        self._address_scheme = "https-mock"
        self._server_address = f"{host}:{port}"
        mock_adapter = make_mock_server_adapter(self._address_scheme, self._server_address)
        self._session.mount(prefix=self._address_scheme, adapter=mock_adapter)

        response = self._session.get(f"{self._address_scheme}://{self._server_address}/info")
        if response.ok:
            self._last_server_modification = int(response.text)
        else:
            raise ConnectionFailed

    def get_address(self) -> str:
        return f"{self._address_scheme}://{self._server_address}"
