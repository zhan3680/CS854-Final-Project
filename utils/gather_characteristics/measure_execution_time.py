import os
import sys
import json
import random
import time

def get_execution_time(action, n):
    os.system("wsk -i action invoke {} --blocking --param n {} | tail -n +2 > {}.json".format(action, n, action))
    f = open("{}.json".format(action))
    log = json.load(f)
    execution_time = log["duration"]
    f.close()
    os.remove("{}.json".format(action))
    return execution_time

# run an end-to-end workflow with input value n, return a list containing execution time of all functions
# in the workflow given this input
def run():
    res = {}

    n = random.randint(101, 501)
    res["constant"] = get_execution_time("constant", n)
    res["logarithmic"] = get_execution_time("logarithmic", n)
    res["linear"] = get_execution_time("linear", n)
    res["linearithmic"] = get_execution_time("linearithmic", n)
    res["quadratic"] = get_execution_time("quadratic", n)
    res["cubic"] = get_execution_time("cubic", n)

    return res

def iteration(num_iterations):
    res = {"constant": [], "logarithmic": [], "linear": [], "linearithmic": [], "quadratic": [], "cubic": []}

    for i in range(num_iterations):
        action_durations = run()
        for action in action_durations.keys():
            res[action].append(action_durations[action])

    for action in res.keys():
        res[action] = sum(res[action])/len(res[action])

    return res

if __name__ == '__main__':
    num_iterations = int(sys.argv[1])
    action_avg_duration = iteration(num_iterations)
    f = open("action_avg_duration.json", 'w+')
    json.dump(action_avg_duration, f)
    f.close()