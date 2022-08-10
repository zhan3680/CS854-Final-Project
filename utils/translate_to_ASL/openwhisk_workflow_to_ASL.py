import json
import sys
import random
import string
import os

class State:
    def __init__(self, action_name, index, type):
        self.name = generate_state_name(action_name, index)
        self.type = type
        self.end = None
        self.next = None
        self.branches = None
        self.resource = None
        if self.type == "Parallel":
            self.branches = []
        elif self.type == "Task":
            self.resource = action_name

    def update_branch(self, state_machine):
        if self.branches is not None:
            self.branches.append(state_machine)

    def to_ASL(self):
        res_ASL = {}
        res_ASL["Type"] = self.type

        if self.type == "Task":
            res_ASL["Resource"] = self.resource
        elif self.type == "Parallel":
            res_ASL["Branches"] = [s_m.to_ASL() for s_m in self.branches]

        if self.end:
            res_ASL["End"] = True
        else:
            res_ASL["Next"] = self.next

        return res_ASL


class StateMachine:
    def __init__(self):
        self.states = []
        self.start_at = None

    def append_state(self, state):
        self.states.append(state)

    def extend_states(self, states):
        self.states.extend(states)

    def to_ASL(self):
        res_ASL = {}
        res_ASL["States"] = {}

        self.start_at = self.states[0].name
        res_ASL["StartAt"] = self.start_at

        for i in range(len(self.states)-1):
            cur_state = self.states[i]
            next_state = self.states[i+1]
            cur_state.end = False
            cur_state.next = next_state.name
            res_ASL["States"][cur_state.name] = cur_state.to_ASL()

        self.states[-1].end = True
        res_ASL["States"][self.states[-1].name] = self.states[-1].to_ASL()

        return res_ASL



# take as input an ow workflow (dictionary), returns a state machine
def translate_ow_workflow_to_state_machine(ow_workflow, index):

    if ow_workflow["type"] == "action":
        action_name = retrieve_action_name(ow_workflow["name"])
        cur_state = State(action_name, index, "Task")
        cur_state_machine = StateMachine()
        cur_state_machine.append_state(cur_state)
        return cur_state_machine

    elif ow_workflow["type"] == "sequence":
        cur_state_machine = StateMachine()
        i = random.randint(1, 10000)
        for workflow in ow_workflow["components"]:
            tmp_state_machine = translate_ow_workflow_to_state_machine(workflow, index+i)
            cur_state_machine.extend_states(tmp_state_machine.states)
            i = random.randint(1, 10000)

        return cur_state_machine

    elif ow_workflow["type"] == "parallel":
        cur_state = State(generate_random_string(6), index, "Parallel")
        cur_state_machine = StateMachine()
        i = 1
        for workflow in ow_workflow["components"]:
            tmp_state_machine = translate_ow_workflow_to_state_machine(workflow, index+i)
            cur_state.update_branch(tmp_state_machine)
            i += 1

        cur_state_machine.append_state(cur_state)
        return cur_state_machine

    else:
        print("type not supported yet, sorry!")
        exit(854)


def retrieve_action_name(full_name):
    return full_name.split('/')[-1]

def generate_random_string(n):
    ran = ''.join(random.choices(string.ascii_uppercase, k=n))
    return ran

def generate_state_name(action_name, index):
    return "{}_{}".format(action_name, index)

if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    ow_workflow = json.load(f)
    f.close()
    state_machine = translate_ow_workflow_to_state_machine(ow_workflow, 0)
    if os.path.exists("{}_ASL.json".format(sys.argv[1].split('.')[0])):
        os.remove("{}_ASL.json".format(sys.argv[1].split('.')[0]))
    f2 = open("{}_ASL.json".format(sys.argv[1].split('.')[0]), "w+")
    json.dump(state_machine.to_ASL(), f2)
    f2.close()
