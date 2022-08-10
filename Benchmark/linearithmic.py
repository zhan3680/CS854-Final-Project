def main(input):
    n = input["n"]
    res = 0
    for i in range(n*log(n)):
        res += i
    return {"n": n, "res": res}


def log(n):
    for i in range(1, n):
        if 2**(i-1) < n and 2**i >= n:
            return i