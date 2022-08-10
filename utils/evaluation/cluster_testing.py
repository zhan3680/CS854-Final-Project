import os
import sys
import json
import random
from multiprocessing import Pool
from functools import partial

def gen_number(n = 1):
    return random.randint(0, n)

def gen_string(length = 10):
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(length))

TEST_ACTION = "time_complexity"

# generate a parameter for the TEST_ACTION
# change this for different actions
def gen_param():
    return "n " + str(random.randint(50, 100))

def get_execution_time(i):
    action = TEST_ACTION
    param = gen_param()
    print("Running test " + str(i) + " with param: " + param)
    cmd = "wsk -i action invoke {} --blocking --param {} | tail -n +2".format(action, param)

    try:
        out = os.popen(cmd).read()
        log = json.loads(out)
        if log["response"]["success"]:
            execution_time = log["duration"]
            print("Finish test {} in {} ms".format(i, execution_time))
            return execution_time
        else:
            print("Test {} fails".format(i))
            return -1
    except:
        print("Test {} fails with exception".format(i))
        return -1

def run_test():
    num_test = 20
    with Pool(2) as p:
        times = p.map(get_execution_time, range(num_test))
        times = list(filter(lambda t: t > 0, times))
        return sum(times) / len(times)
        # return times.value

if __name__ == '__main__':
    print(run_test())
