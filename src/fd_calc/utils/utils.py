from sys import stderr

def error(message:str):
    print(message, file=stderr)