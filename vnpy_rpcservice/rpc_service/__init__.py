from pathlib import Path

from vnpy.trader.app import BaseApp

from .engine import RpcEngine, APP_NAME


class RpcServiceApp(BaseApp):
    """"""
    app_name: str = APP_NAME
    app_module: str = __module__
    app_path: Path = Path(__file__).parent
    display_name: str = "RPC服务"
    engine_class: RpcEngine = RpcEngine
    widget_name: str = "RpcManager"
    icon_name: str = str(app_path.joinpath("ui", "rpc.ico"))
