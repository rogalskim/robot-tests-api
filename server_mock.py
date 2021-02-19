import re
import time
from typing import Any, Union
import urllib.parse

import requests
import requests_mock

from task import Task


class MockConstants:
    fail_key = "mock_fail"
    true = "True"
    false = "False"


class ServerMock:
    def __init__(self, server_address: str) -> None:
        self._adapter = requests_mock.Adapter()

        self._tasks = self._make_mock_tasks()
        self._robots = ["Molly", "Bosco", "Doretta", "Karl"]
        self._next_task_id = 1701

        self._make_mock_api(server_address)

    def get_mock_adapter(self) -> requests_mock.Adapter:
        return self._adapter

    @staticmethod
    def _should_response_fail(request: requests.Request) -> bool:
        if MockConstants.fail_key not in request.headers.keys():
            return False
        return request.headers[MockConstants.fail_key] == MockConstants.true

    def _get_modification_timestamp(self, request: requests.Request, context: Any) -> str:
        """
        Mock callback for Server modification time requests.

        :returns: modification timestamp as str.
        """
        if self._should_response_fail(request):
            context.status_code = requests.codes.server_error
            context.reason = "Internal server error."
        else:
            context.status_code = requests.codes.ok

        current_time = str(int(time.time()))
        return current_time

    def _create_task(self, request: requests.Request, context: Any) -> str:
        """
        Mock callback for Task creation requests.

        :returns: Task id as string.
        """
        requested_task_details = request.json()

        if self._should_response_fail(request):
            context.status_code = requests.codes.server_error
            context.reason = "Internal server error."
            return context.reason
        elif requested_task_details["robot_name"] not in self._robots:
            context.status_code = requests.codes.bad_request
            context.reason = "Invalid robot name requested."
            return context.reason
        else:
            context.status_code = requests.codes.ok

        new_task = Task(task_id=self._next_task_id,
                        creation_time=int(time.time()),
                        robot_id=self._robots.index(requested_task_details["robot_name"]),
                        branch=requested_task_details["branch"],
                        runs=requested_task_details["runs"])
        self._tasks[self._next_task_id] = new_task
        self._next_task_id += 1

        return str(new_task.task_id)

    def _get_robot_list(self, request: requests.Request, context: Any) -> str:
        """
        Mock callback for robot list requests.

        :returns: robot names separated by spaces.
        """
        if self._should_response_fail(request):
            context.status_code = requests.codes.im_a_teapot
            context.reason = "The robots have rebelled."
        else:
            context.status_code = requests.codes.ok
        return " ".join(self._robots)

    def _get_tasks(self, request: requests.Request, context: Any) -> Union[dict, list]:
        """
        Mock callback for Task requests. Handles requests both for single and multiple tasks,
        based on the url query element.
        :return: dict or list of dict representing the Task(s)
        """
        if self._should_response_fail(request):
            context.status_code = requests.codes.server_error
            context.reason = "Internal server error."
            return {}

        task_query = urllib.parse.urlsplit(request.url)[3]
        if task_query == "":
            context.status_code = requests.codes.bad_request
            context.reason = "No query specified."
            return {}

        query_type, query_value = task_query.split('=')
        if query_type == "id":
            task_id = int(query_value)
            if task_id not in self._tasks.keys():
                context.status_code = requests.codes.not_found
                context.reason = "Invalid Task Id."
                return {}
            context.status_code = requests.codes.ok
            return self._tasks[task_id].__dict__
        elif query_type == "q":
            if query_value != "all":
                context.status_code = requests.codes.bad_request
                context.reason = "Invalid query."
                return {}
            context.status_code = requests.codes.ok

            filtered_tasks = list(self._tasks.values())

            if "robot_name" in list(request.headers.keys()):
                robot_name = request.headers["robot_name"]
                if robot_name in self._robots:
                    robot_id = self._robots.index(robot_name)

                    def match_robot_id(task: Task) -> bool:
                        return task.robot_id == robot_id

                    filtered_tasks = filter(match_robot_id, filtered_tasks)

            if "status" in list(request.headers.keys()):
                status = request.headers["status"]

                def match_status(task: Task) -> bool:
                    return task.status == status

                filtered_tasks = filter(match_status, filtered_tasks)

            task_dicts = [task.__dict__ for task in filtered_tasks]
            return task_dicts
        else:
            context.status_code = requests.codes.bad_request
            context.reason = "Invalid query."
            return {}

    @staticmethod
    def _make_mock_tasks() -> dict:
        def set_task_result(task_dict: dict, task_id: int, attempts: int, successes: int) -> None:
            task = task_dict[task_id]
            task.status = "finished"
            task.attempts = attempts
            task.successes = successes

        mock_tasks = [Task(1, 1611010000, 0, 10, "configs_dev_0_0_1"),
                      Task(8, 1612017000, 0, 5, "configs_dev_0_2_0"),
                      Task(117, 161300000, 1, 5, "configs_dev_0_2_9"),
                      Task(213, 1613227000, 2, 20, "configs_dev_0_5_2"),
                      Task(503, 1613707000, 3, 1, "configs_dev_0_6_4"),
                      Task(789, 1613727105, 2, 100, "configs_dev_0_7_5"),
                      Task(1024, int(time.time()), 0, 50, "configs_dev_0_8_1")]

        mock_tasks[-2].status = "running"
        mock_tasks[-1].status = "running"

        task_dict = {task.task_id: task for task in mock_tasks}

        set_task_result(task_dict, task_id=1, attempts=23, successes=18)
        set_task_result(task_dict, task_id=8, attempts=16, successes=5)
        set_task_result(task_dict, task_id=213, attempts=75, successes=71)
        set_task_result(task_dict, task_id=503, attempts=6, successes=4)

        return task_dict

    def _make_mock_api(self, server_address: str) -> None:
        self._adapter.register_uri(method="GET",
                                   url=f"{server_address}/info?q=mod_time",
                                   text=self._get_modification_timestamp)

        self._adapter.register_uri(method="POST",
                                   url=f"{server_address}/tasks",
                                   text=self._create_task)

        self._adapter.register_uri(method="GET",
                                   url=f"{server_address}/robots",
                                   text=self._get_robot_list)

        task_matcher = re.compile(f"{server_address}/tasks")
        self._adapter.register_uri("GET", task_matcher, json=self._get_tasks)

