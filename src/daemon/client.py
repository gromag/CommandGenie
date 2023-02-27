from multiprocessing.connection import Client


def call_daemon(data):
    address = ("localhost", 6000)
    conn = Client(address)
    conn.send(data)
    command, reasoning = conn.recv()
    conn.close()
    return command, reasoning
