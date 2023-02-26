import os
from dotenv import load_dotenv
from multiprocessing.connection import Listener


load_dotenv()


def start_daemon():
    # import only in triggered
    from genie.genie import GenieServer
    from genie.models.openai_model import OpenAILanguageModel
    from internals.logger import genie_logger

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
