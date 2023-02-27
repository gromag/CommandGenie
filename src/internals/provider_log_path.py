import os
import abstractions
from pathlib import Path
from internals.provider_os import OSProvider


class Consts:
    WIN_ROOT_PATH = "%LOCALAPPDATA%"
    MAC_ROOT_PATH = "$HOME"
    LINUX_ROOT_PATH = "/var/log"
    DEFAULT_ROOT_PATH = "./"
    RELATIVE_LOG_PATH = Path("CommandGenie")


class _BaseLogPathProvider(abstractions.LogPathProvider):
    """Internally used, provides base functionality to evaluate OS specific paths
    aliases.
    As an example %LOCALAPPDATA% on Windows and $HOME on Mac

    """

    def __init__(self, root_folder: str) -> None:
        self.root_folder = root_folder

    def get_path(self) -> Path:
        root = os.popen(f"echo {self.root_folder}").read().strip()
        return Path(root)


class _MacLogPathProvider(_BaseLogPathProvider):
    """Provides Mac specific log path

    Args:
        BaseLogPathProvider (_type_): _description_
    """

    def __init__(self) -> None:
        super().__init__(Consts.MAC_ROOT_PATH)

    def get_path(self) -> Path:
        root_path = super().get_path() / Path("Library", "Logs")

        return root_path / Consts.RELATIVE_LOG_PATH


class _LinuxPathProvider(_BaseLogPathProvider):
    """Provides Linux specific log path

    Args:
        BaseLogPathProvider (_type_): _description_
    """

    def __init__(self) -> None:
        super().__init__(Consts.LINUX_ROOT_PATH)

    def get_path(self) -> Path:
        return super().get_path() / Consts.RELATIVE_LOG_PATH.lower() / "logs"


class _WinLogPathProvider(_BaseLogPathProvider):
    """Provides Win specific log path

    Args:
        BaseLogPathProvider (_type_): _description_
    """

    def __init__(self) -> None:
        super().__init__(Consts.WIN_ROOT_PATH)

    def get_path(self) -> Path:

        return super().get_path() / Consts.RELATIVE_LOG_PATH / "Logs"


class LogProviderFactory:
    def get_log_provider() -> abstractions.LogPathProvider:

        if OSProvider.is_mac():
            return _MacLogPathProvider()

        if OSProvider.is_linux():
            return _LinuxPathProvider()

        if OSProvider.is_win():
            return _WinLogPathProvider()

        raise NotImplementedError("The current OS is not supported.")


class LogPathProvider(abstractions.LogPathProvider):
    """Provides the path to where write logs

    Args:
        lib_abstractions (_type_): _description_
    """

    def __init__(self, create_path=True) -> None:
        super().__init__()
        self.provider = LogProviderFactory.get_log_provider()
        self.create = create_path

    def get_path(self) -> Path:
        path = self.provider.get_path()
        if self.create:
            os.makedirs(path, exist_ok=True)
        return path
