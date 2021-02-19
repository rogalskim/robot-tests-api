import urllib.parse

import requests

from exceptions import ExecutionError
from task import Task, dict_to_task, dict_list_to_task_list
from server_mock import ServerMock, MockConstants


class ClientSession:
    def __init__(self, host: str, port: int, simulate_failure: bool) -> None:
        self._server_address = f"https-mock://{host}:{port}"
        self._session = self._create_mock_server_session(self._server_address)
        self._test_server_connection(simulate_failure)

    def get_address(self) -> str:
        return self._server_address

    def get_server_modification_time(self, simulate_failure: bool = False) -> int:
        headers = self._make_basic_request_header(simulate_failure)
        response = self._session.get(url=f"{self._server_address}/info?q=mod_time", headers=headers)
        self._abort_if_response_is_bad(response)
        return int(response.text)

    def request_task_creation(self, robot_name: str, git_branch: str, run_count: int,
                              simulate_failure: bool = False) -> int:
        """:return: Task id for the created Task"""
        request_data = {"robot_name": robot_name, "branch": git_branch, "runs": run_count}
        response = self._session.post(url=f"{self._server_address}/tasks",
                                      headers=self._make_basic_request_header(simulate_failure),
                                      json=request_data)

        self._abort_if_response_is_bad(response)
        return int(response.text)

    def get_robot_dict(self, simulate_failure: bool) -> dict:
        request_headers = self._make_basic_request_header(simulate_failure)
        response = self._session.get(url=f"{self._server_address}/robots", headers=request_headers)

        self._abort_if_response_is_bad(response)

        robot_list = response.text.split()
        robot_dict = {index: robot_name for index, robot_name in enumerate(robot_list)}
        return robot_dict

    def get_task(self, task_id: int, simulate_failure: bool) -> Task:
        request_headers = self._make_basic_request_header(simulate_failure)
        request_url = f"{self._server_address}/tasks?id={task_id}"
        response = self._session.get(url=request_url, headers=request_headers)

        self._abort_if_response_is_bad(response)

        return dict_to_task(response.json())

    def get_many_tasks(self, robot_name: str, status: str, simulate_failure: bool) -> list:
        """:return: list of Tasks"""
        request_headers = self._make_basic_request_header(simulate_failure)
        request_headers["robot_name"] = robot_name
        request_headers["status"] = status
        response = self._session.get(f"{self._server_address}/tasks?q=all", headers=request_headers)

        ClientSession._abort_if_response_is_bad(response)

        return dict_list_to_task_list(response.json())

    def _test_server_connection(self, simulate_failure: bool) -> None:
        self.get_server_modification_time(simulate_failure)

    @staticmethod
    def _create_mock_server_session(server_address: str) -> requests.Session:
        session = requests.session()
        mock_server = ServerMock(server_address)
        mock_adapter = mock_server.get_mock_adapter()
        address_scheme = urllib.parse.urlparse(server_address).scheme
        session.mount(prefix=address_scheme, adapter=mock_adapter)
        return session

    @staticmethod
    def _make_basic_request_header(should_fail: bool) -> dict:
        """Makes a request header that can Signal mock Server to simulate request failure."""
        return {MockConstants.fail_key: MockConstants.true if should_fail else MockConstants.false}

    @staticmethod
    def _abort_if_response_is_bad(response: requests.Response) -> None:
        if not response.ok:
            raise ExecutionError(f"HTTP request failed: {response.status_code}\n{response.reason}")
