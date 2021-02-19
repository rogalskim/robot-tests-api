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
- Getting Task info
```
> get_task 1701
{'task_id': 1701, 'creation_time': 1613720393, 'robot_id': 0, 'runs': 100, 'branch': 'configs_dev_0_8_1'...
```
- Closing the program
```
> exit
Goodbye!
```

