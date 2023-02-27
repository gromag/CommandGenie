import os
import sys


class OSProvider:
    """Helps determine the Operative System is running on"""

    @staticmethod
    def is_mac() -> bool:
        return sys.platform.lower().startswith("darwin")

    @staticmethod
    def is_linux() -> bool:
        return sys.platform.lower().startswith("linux")

    @staticmethod
    def is_linux_or_mac() -> bool:
        return os.name.lower() == "posix"

    @staticmethod
    def is_win() -> bool:
        return sys.platform.lower().startswith("win")
