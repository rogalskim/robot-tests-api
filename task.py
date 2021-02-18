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


def json_to_task(json: dict) -> Task:
    task = Task(json["task_id"],
                json["creation_time"],
                json["robot_id"],
                json["runs"],
                json["branch"])
    task.status = json["status"]
    task.attempts = json["attempts"]
    task.successes = json["successes"]
    return task
