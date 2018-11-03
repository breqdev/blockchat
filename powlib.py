import hashlib

def check(incrementer):
    sha256 = hashlib.sha256()
    sha256.update(str(incrementer).encode("utf-8"))
    return sha256.hexdigest().startswith("d3c0d3")

def compute(previous):
    incrementer = previous + 1
    while not check(incrementer):
        incrementer += 1
    return incrementer
