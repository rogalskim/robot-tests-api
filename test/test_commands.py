import time
import unittest

from commands import Connect, CreateTask, GetTask
from exceptions import ExecutionError
from task import Task


class TestConnect(unittest.TestCase):
    def test_creates_session_with_given_server_address(self):
        mock_scheme = "https-mock"
        test_host = "server.ai"
        test_port = 6400
        expected_address = f"{mock_scheme}://{test_host}:{test_port}"
        arguments = f"--host {test_host} --port {test_port}"

        session = Connect().execute(arguments)

        self.assertEqual(session.get_address(), expected_address)

    def test_raises_execution_error_if_failure_requested(self):
        arguments = "--fail"

        self.assertRaises(ExecutionError, Connect().execute, arguments)


class WithClientSessionFixture(unittest.TestCase):
    def setUp(self):
        self.session = Connect().execute(arguments="")


class TestCreateTask(WithClientSessionFixture):
    def test_returns_task_id(self):
        arguments = "Karl git_branch 10"
        expected_task_id = 1701

        created_task_id = CreateTask().execute(arguments, self.session)

        self.assertEqual(created_task_id, expected_task_id)

    def test_raises_if_invalid_robot_name_given(self):
        arguments = "BadRobot git_branch 10"

        self.assertRaises(ExecutionError, CreateTask().execute, arguments, self.session)

    def test_creates_correct_task(self):
        expected_task = Task(task_id=1701, creation_time=0, robot_id=0, runs=8, branch="git_rocks")
        arguments = f"Molly {expected_task.branch} {expected_task.runs}"

        created_task_id = CreateTask().execute(arguments, self.session)
        created_task = GetTask().execute(str(created_task_id), self.session)

        current_timestamp = int(time.time())
        self.assertAlmostEqual(current_timestamp, created_task.creation_time)

        expected_task.creation_time = created_task.creation_time
        self.assertDictEqual(created_task.__dict__, expected_task.__dict__)


if __name__ == '__main__':
    unittest.main()
