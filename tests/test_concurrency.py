import logging
import time
from datetime import datetime

import requests

from mb_std import ParallelTasks, hrequest
from mb_std.concurrency import Scheduler, synchronized_parameter


def task1() -> str:
    res = hrequest("https://httpbin.org/user-agent", user_agent="agent007")
    return res.json["user-agent"]


def task2(name: str, value: str) -> str:
    res = requests.get(f"https://httpbin.org/get?{name}={value}")
    return res.json()["args"][name]


def task3(*, p1: str, p2: str) -> str:
    res = requests.get(f"https://httpbin.org/get?p1={p1}&p2={p2}")
    return res.json()["args"]


def task4():
    raise Exception("moo")


def task5(seconds: int):
    time.sleep(seconds)


def task6():
    pass


def test_ok():
    tasks = ParallelTasks()
    tasks.add_task("task1", task1)
    tasks.add_task("task2", task2, ("aaa", "bbb"))
    tasks.add_task("task3", task3, kwargs={"p1": "aaa", "p2": "bbb"})
    tasks.execute()

    assert not tasks.error
    assert not tasks.timeout_error
    assert tasks.exceptions == {}
    assert tasks.result == {"task1": "agent007", "task2": "bbb", "task3": {"p1": "aaa", "p2": "bbb"}}


def test_exceptions():
    tasks = ParallelTasks()
    tasks.add_task("task1", task1)
    tasks.add_task("task4", task4)
    tasks.execute()

    assert tasks.error
    assert not tasks.timeout_error
    assert len(tasks.exceptions) == 1
    assert tasks.result == {"task1": "agent007"}


def test_timeout():
    tasks = ParallelTasks(timeout=3)
    tasks.add_task("task1", task1)
    tasks.add_task("task5", task5, (5,))
    tasks.execute()

    assert tasks.error
    assert tasks.timeout_error
    assert tasks.result == {"task1": "agent007"}


def test_synchronized_parameters():
    counter = 0

    @synchronized_parameter()
    def task(_param, _second_param=None):
        nonlocal counter
        time.sleep(1)
        counter += 1

    start_time = datetime.now()
    tasks = ParallelTasks()
    tasks.add_task("task1", task, args=(1,))
    tasks.add_task("task2", task, args=(1, 4))
    tasks.add_task("task3", task, args=(2,))
    tasks.add_task("task4", task, args=(3,))
    tasks.execute()
    end_time = datetime.now()

    assert counter == 4
    assert (end_time - start_time).seconds == 2


def test_synchronized_parameters_skip_if_locked():
    counter = 0

    @synchronized_parameter(skip_if_locked=True)
    def task(_param, _second_param=None):
        nonlocal counter
        time.sleep(1)
        counter += 1

    tasks = ParallelTasks()
    tasks.add_task("task1", task, args=(1,))
    tasks.add_task("task2", task, args=(1, 4))
    tasks.add_task("task3", task, args=(2,))
    tasks.add_task("task4", task, args=(3,))
    tasks.execute()

    assert counter == 3


def test_scheduler():
    logger = logging.getLogger()
    scheduler = Scheduler(logger)
    scheduler.add_job(lambda x: x, 5)
    scheduler.start()
    scheduler.stop()
