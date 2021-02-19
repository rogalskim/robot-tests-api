# robot-tests-api
Demo of an interactive command-line application for scheduling and reviewing robot evaluation tasks, operating on a mock REST API.

# Dependencies

- Python 3 (tested on version 3.9.1)
- requests 2.25.1
```
$ pip install requests
```
- requests-mock 1.8.0
```
$ pip install requests-mock
```

# Usage
- Running the program
```
$ python run.py
```
- Connecting to mock server
```
> connect
Established connection to https-mock://192.168.1.2:5000
```
- Getting command help
```
> help
```
```
> <command> --help
```
- Getting the list of Robots
```
> get_robots
{0: 'Molly', 1: 'Bosco', 2: 'Doretta', 3: 'Karl'}
```
- Adding a new Task
```
> create_task Molly configs_dev_0_8_1 100
Created new Task with id: 1701
```
- Getting a single Task by its task_id
```
> get_task 1701
{'task_id': 1701, 'creation_time': 1613720393, 'robot_id': 0, 'runs': 100, 'branch': 'configs_dev_0_8_1'...
```
- Making a filtered Task query
```
> get_many_tasks -r Molly -s finished
{'task_id': 1, 'creation_time': 1611010000, 'robot_id': 0, 'runs': 10, 'branch': 'configs_dev_0_0_1', 'status': 'finished', ...
{'task_id': 8, 'creation_time': 1612017000, 'robot_id': 0, 'runs': 5, 'branch': 'configs_dev_0_2_0', 'status': 'finished', ...
```
- Closing the program
```
> exit
Goodbye!
```

