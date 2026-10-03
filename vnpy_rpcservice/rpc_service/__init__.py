"""RPC 服务应用包。"""
from pathlib import Path

from vnpy.trader.app import BaseApp

from .engine import RpcEngine, APP_NAME


__all__ = [
    "RpcEngine",
    "APP_NAME",
    "RpcServiceApp",
]


class RpcServiceApp(BaseApp):
    """RPC 服务应用。"""
    app_name: str = APP_NAME
    app_module: str = __module__
    app_path: Path = Path(__file__).parent
    display_name: str = "RPC服务"
    engine_class: type[RpcEngine] = RpcEngine
    widget_name: str = "RpcManager"
    icon_name: str = str(app_path.joinpath("ui", "rpc.ico"))
