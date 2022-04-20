import traceback
from typing import Dict, Optional

from vnpy.event import Event, EventEngine
from vnpy.rpc import RpcServer
from vnpy.trader.engine import BaseEngine, MainEngine
from vnpy.trader.utility import load_json, save_json
from vnpy.trader.object import LogData

APP_NAME = "RpcService"

EVENT_RPC_LOG = "eRpcLog"


class RpcEngine(BaseEngine):
    """
    VeighNa的rpc服务引擎。
    """
    setting_filename: str = "rpc_service_setting.json"

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        """构造函数"""
        super().__init__(main_engine, event_engine, APP_NAME)

        self.rep_address: str = "tcp://*:2014"
        self.pub_address: str = "tcp://*:4102"

        self.server: Optional[RpcServer] = None

        self.init_server()
        self.load_setting()
        self.register_event()

    def init_server(self) -> None:
        """初始化服务器"""
        self.server = RpcServer()

        self.server.register(self.main_engine.subscribe)
        self.server.register(self.main_engine.send_order)
        self.server.register(self.main_engine.cancel_order)
        self.server.register(self.main_engine.query_history)

        self.server.register(self.main_engine.get_tick)
        self.server.register(self.main_engine.get_order)
        self.server.register(self.main_engine.get_trade)
        self.server.register(self.main_engine.get_position)
        self.server.register(self.main_engine.get_account)
        self.server.register(self.main_engine.get_contract)
        self.server.register(self.main_engine.get_all_ticks)
        self.server.register(self.main_engine.get_all_orders)
        self.server.register(self.main_engine.get_all_trades)
        self.server.register(self.main_engine.get_all_positions)
        self.server.register(self.main_engine.get_all_accounts)
        self.server.register(self.main_engine.get_all_contracts)
        self.server.register(self.main_engine.get_all_active_orders)

    def load_setting(self) -> None:
        """读取配置文件"""
        setting: Dict[str, str] = load_json(self.setting_filename)
        self.rep_address = setting.get("rep_address", self.rep_address)
        self.pub_address = setting.get("pub_address", self.pub_address)

    def save_setting(self) -> None:
        """保存配置文件"""
        setting: Dict[str, str] = {
            "rep_address": self.rep_address,
            "pub_address": self.pub_address
        }
        save_json(self.setting_filename, setting)

    def start(self, rep_address: str, pub_address: str) -> bool:
        """启动rpc服务"""
        if self.server.is_active():
            self.write_log("RPC服务运行中")
            return False

        self.rep_address = rep_address
        self.pub_address = pub_address

        try:
            self.server.start(rep_address, pub_address)
        except:  # noqa
            msg: str = traceback.format_exc()
            self.write_log(f"RPC服务启动失败：{msg}")
            return False

        self.save_setting()
        self.write_log("RPC服务启动成功")
        return True

    def stop(self) -> bool:
        """停止rpc服务"""
        if not self.server.is_active():
            self.write_log("RPC服务未启动")
            return False

        self.server.stop()
        self.server.join()
        self.write_log("RPC服务已停止")
        return True

    def close(self) -> None:
        """关闭rpc服务"""
        self.stop()

    def register_event(self) -> None:
        """注册事件"""
        self.event_engine.register_general(self.process_event)

    def process_event(self, event: Event) -> None:
        """调用事件"""
        if self.server.is_active():
            self.server.publish("", event)

    def write_log(self, msg: str) -> None:
        """输出日志"""
        log: LogData = LogData(msg=msg, gateway_name=APP_NAME)
        event: Event = Event(EVENT_RPC_LOG, log)
        self.event_engine.put(event)
