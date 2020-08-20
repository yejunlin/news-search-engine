import sched
import time
from init import t,s
from bbc_init import bbc_target
from bbc_spider import bbc_start
def timed_task():
    # 初始化 sched 模块的 scheduler 类
    scheduler = sched.scheduler(time.time, time.sleep)
    # 增加调度任务
    scheduler.enter(t, s, task())
    # 运行任务
    scheduler.run()


# 定时任务
def task():
    bbc_start(bbc_target)


if __name__ == '__main__':
    timed_task()
