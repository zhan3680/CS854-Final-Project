def main(input):
    n = input["n"]
    res = 0
    for i in range(n**2):
        res += i
    return {"n": n, "res": res}