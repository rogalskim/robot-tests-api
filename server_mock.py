import re
import time
from typing import Any, Union
import urllib.parse

import requests
import requests_mock

from api import Endpoints, RequestUrls, RequestUrl, Queries
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

        :return: modification timestamp as str.
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

        :return: Task id as string.
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

        :return: robot names separated by spaces.
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

        query_string = urllib.parse.urlsplit(request.url).query
        if query_string == "":
            context.status_code = requests.codes.bad_request
            context.reason = "No query specified."
            return {}

        return self._process_task_query(request, context, query_string)

    def _process_task_query(self, request: requests.Request, context: Any, query_string: str) -> \
            Union[dict, list]:
        """
        Interprets task request type based on the query string and calls proper processing method.

        :return: dict or list of dict representing the Task(s)
        """
        query_key, query_value = query_string.split('=')
        if query_key == Queries.single_task("").key():
            return self._get_single_task(context, query_value)
        elif query_string == Queries.all_tasks().text():
            return self._get_filtered_task_list(request, context, query_value)
        else:
            context.status_code = requests.codes.bad_request
            context.reason = "Invalid query."
            return {}

    def _get_single_task(self, response_context: Any, query_value: str) -> dict:
        """:return: dict representation of the Task"""
        task_id = int(query_value)
        if task_id not in self._tasks.keys():
            response_context.status_code = requests.codes.not_found
            response_context.reason = "Invalid Task Id."
            return {}
        response_context.status_code = requests.codes.ok
        return self._tasks[task_id].__dict__

    def _get_filtered_task_list(self, request: requests.Request, response_context: Any,
                                query_value: str) -> list:
        """:return: list of Tasks represented as dicts"""

        tasks = list(self._tasks.values())

        if "robot_name" in list(request.headers.keys()):
            robot_name = request.headers["robot_name"]
            tasks = self._filter_task_list_by_robot_name(tasks, robot_name)

        if "status" in list(request.headers.keys()):
            status = request.headers["status"]
            tasks = [task for task in tasks if task.status == status]

        response_context.status_code = requests.codes.ok
        task_dicts = [task.__dict__ for task in tasks]
        return task_dicts

    def _filter_task_list_by_robot_name(self, task_list: list, robot_name: str) -> list:
        if robot_name not in self._robots:
            return task_list
        robot_id = self._robots.index(robot_name)
        return [task for task in task_list if task.robot_id == robot_id]

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

        tasks_dict = {task.task_id: task for task in mock_tasks}

        set_task_result(tasks_dict, task_id=1, attempts=23, successes=18)
        set_task_result(tasks_dict, task_id=8, attempts=16, successes=5)
        set_task_result(tasks_dict, task_id=213, attempts=75, successes=71)
        set_task_result(tasks_dict, task_id=503, attempts=6, successes=4)

        return tasks_dict

    def _make_mock_api(self, server_address: str) -> None:
        self._adapter.register_uri(method="GET",
                                   url=RequestUrls.get_modification_time(server_address).text(),
                                   text=self._get_modification_timestamp)

        self._adapter.register_uri(method="POST",
                                   url=RequestUrls.create_task(server_address).text(),
                                   text=self._create_task)

        self._adapter.register_uri(method="GET",
                                   url=RequestUrls.get_robots(server_address).text(),
                                   text=self._get_robot_list)

        task_endpoint_url = RequestUrl(root=server_address, endpoint=Endpoints.tasks).text()
        match_all_task_get_requests = re.compile(task_endpoint_url)
        self._adapter.register_uri("GET", match_all_task_get_requests, json=self._get_tasks)
