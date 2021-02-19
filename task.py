class Task:
    def __init__(self,
                 task_id: int,
                 creation_time: int,
                 robot_id: int,
                 runs: int,
                 branch: str) -> None:

        self.task_id = task_id
        self.creation_time = creation_time
        self.robot_id = robot_id
        self.runs = runs
        self.branch = branch
        self.status = "waiting"
        self.attempts = None
        self.successes = None


def dict_to_task(input_dict: dict) -> Task:
    task = Task(input_dict["task_id"],
                input_dict["creation_time"],
                input_dict["robot_id"],
                input_dict["runs"],
                input_dict["branch"])
    task.status = input_dict["status"]
    task.attempts = input_dict["attempts"]
    task.successes = input_dict["successes"]
    return task


def dict_list_to_task_list(dict_list: list) -> list:
    task_list = []
    for task_dict in dict_list:
        task_list.append(dict_to_task(task_dict))
    return task_list
