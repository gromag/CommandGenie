
import timeit
import os
from dotenv import load_dotenv
from multiprocessing.connection import Listener
from internals.logger import genie_logger

genie_logger.info(f"Daemon starting")

load_dotenv()


def start_daemon():
    # import only if triggered
    from genie.genie import GenieServer
    from genie.models.openai_model import OpenAILanguageModel

    model = OpenAILanguageModel(os.getenv("OPENAI_API_KEY"))
    genie = GenieServer(model)

    genie_logger.info("Daemon started")

    address = ("localhost", 6000)
    listener = Listener(address)
    while True:
        conn = listener.accept()
        data = conn.recv()
        genie_logger.info(f"Daemon received {data}")
        command, reasoning = genie.get_command(data)
        genie_logger.info(f"Daemon generate result {command}")
        conn.send((command, reasoning))
        conn.close()
