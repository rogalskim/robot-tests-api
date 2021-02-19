import requests

from exceptions import ExecutionError
from task import Task, dict_to_task, dict_list_to_task_list
from server_mock import ServerMock, MockConstants


class ClientSession:
    def __init__(self, host: str, port: int, fail_request: bool) -> None:
        self._session = requests.session()

        address_scheme = "https-mock"
        self._server_address = f"{address_scheme}://{host}:{port}"

        self._server_mock = ServerMock(self._server_address)
        mock_adapter = self._server_mock.get_mock_adapter()
        self._session.mount(prefix=address_scheme, adapter=mock_adapter)

        self.get_server_modification_time(fail_request)

    def get_address(self) -> str:
        return self._server_address

    def get_server_modification_time(self, simulate_failure: bool = False) -> int:
        headers = self._add_fail_header(headers={}, should_fail=simulate_failure)
        response = self._session.get(f"{self._server_address}/info?q=mod_time", headers=headers)
        if response.ok:
            return int(response.text)
        else:
            raise ExecutionError(f"HTTP request failed: {response.status_code}\n{response.reason}")

    def request_task_creation(self, robot_name: str, git_branch: str, run_count: int,
                              simulate_failure: bool = False) -> int:
        """:return: Task id for the created Task"""
        request_headers = self._add_fail_header(headers={}, should_fail=simulate_failure)
        request_data = {"robot_name": robot_name,
                        "branch": git_branch,
                        "runs": run_count}

        response = self._session.post(url=f"{self._server_address}/tasks",
                                      headers=request_headers,
                                      json=request_data)
        if response.ok:
            return int(response.text)
        else:
            raise ExecutionError(f"HTTP request failed: {response.status_code}\n{response.reason}")

    def get_robot_dict(self, simulate_failure: bool) -> dict:
        request_headers = self._add_fail_header(headers={}, should_fail=simulate_failure)
        response = self._session.get(url=f"{self._server_address}/robots", headers=request_headers)

        if not response.ok:
            raise ExecutionError(f"HTTP request failed: {response.status_code}\n{response.reason}")

        robot_list = response.text.split()
        robot_dict = {index: robot_name for index, robot_name in enumerate(robot_list)}
        return robot_dict

    def get_task(self, task_id: int, simulate_failure: bool) -> Task:
        request_headers = self._add_fail_header(headers={}, should_fail=simulate_failure)
        request_url = f"{self._server_address}/tasks?id={task_id}"
        response = self._session.get(url=request_url, headers=request_headers)

        if not response.ok:
            raise ExecutionError(f"HTTP request failed: {response.status_code}\n{response.reason}")

        return dict_to_task(response.json())

    def get_many_tasks(self, robot_name: str, status: str, simulate_failure: bool) -> list:
        """
        :return: list of Tasks
        """
        request_headers = {"robot_name": robot_name, "status": status}
        request_headers = self._add_fail_header(request_headers, simulate_failure)
        request_url = f"{self._server_address}/tasks?q=all"
        response = self._session.get(url=request_url, headers=request_headers)

        if not response.ok:
            raise ExecutionError(f"HTTP request failed: {response.status_code}\n{response.reason}")

        return dict_list_to_task_list(response.json())

    @staticmethod
    def _add_fail_header(headers: dict, should_fail: bool) -> dict:
        """Signals mock Server to simulate request failure."""
        if should_fail:
            headers[MockConstants.fail_key] = MockConstants.true
        else:
            headers[MockConstants.fail_key] = MockConstants.false
        return headers

