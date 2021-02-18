import requests
import requests_mock


def make_mock_server_adapter(address_scheme: str, server_address: str) -> requests_mock.Adapter:
    mock_adapter = requests_mock.Adapter()
    full_address = address_scheme + "://" + server_address

    mock_adapter.register_uri(method="GET",
                              url=full_address + "/info",
                              text="1613638253",
                              status_code=requests.codes.ok)
    return mock_adapter
