from typing import Callable

from vnpy.rpc import RpcClient, RpcServer
from vnpy.event import Event
from vnpy.trader.setting import SETTINGS
from vnpy.trader.datafeed import BaseDatafeed
from vnpy.trader.engine import EventEngine
from vnpy.trader.event import EVENT_TIMER
from vnpy.trader.object import HistoryRequest, BarData, TickData
from vnpy.trader.datafeed import get_datafeed


class RpcDatafeed(BaseDatafeed):
    """RPC数据服务"""

    def __init__(self) -> None:
        """"""
        self.req_address: str = SETTINGS["datafeed.username"]
        self.sub_address: str = SETTINGS["datafeed.password"]

        self.inited: bool = False
        self.client: RpcClient = None

    def __del__(self) -> None:
        """对象析构"""
        if self.client and self.client._active:
            self.client.stop()
            self.client.join()

    def init(self, output: Callable = print) -> bool:
        """初始化"""
        if self.inited:
            return True

        if not self.req_address or not self.sub_address:
            output("RPC数据服务初始化失败，请检查连接地址！")
            return False

        self.client = RpcClient()
        self.client.callback = lambda topic, data: None
        self.client.subscribe_topic("")
        self.client.start(self.req_address, self.sub_address)

        return True

    def query_bar_history(self, req: HistoryRequest, output: Callable = print) -> list[BarData]:
        """查询K线数据"""
        if not self.inited:
            n: bool = self.init(output)
            if not n:
                return []

        data: list | str = self.client.query_bar_history(req)

        if isinstance(data, str):
            output(data)
            return []
        else:
            return data

    def query_tick_history(self, req: HistoryRequest, output: Callable = print) -> list[TickData]:
        """查询Tick数据"""
        if not self.inited:
            n: bool = self.init(output)
            if not n:
                return []

        data: list | str = self.client.query_tick_history(req)

        if isinstance(data, str):
            output(data)
            return []
        else:
            return data


class DatafeedServer(RpcServer):
    """RPC数据服务器"""

    def __init__(self, event_engine: EventEngine) -> None:
        """构造函数"""
        super().__init__()

        self.event_engine: EventEngine = event_engine

        self.datafeed: BaseDatafeed = get_datafeed()

        self.register(self.query_bar_history)
        self.register(self.query_tick_history)

        self.register_event()

    def register_event(self) -> None:
        """注册事件监听"""
        self.event_engine.register(EVENT_TIMER, self.send_heartbeat)

    def send_heartbeat(self, event: Event) -> None:
        """发送服务端心跳"""
        if self._active:
            self.publish(EVENT_TIMER, None)

    def query_bar_history(self, req: HistoryRequest, output: Callable = print) -> list[BarData] | str:
        """查询K线数据"""
        logs: list = []
        bars: list = self.datafeed.query_bar_history(req, logs.append)

        if logs:
            return " | ".join(logs)
        else:
            return bars

    def query_tick_history(self, req: HistoryRequest, output: Callable = print) -> list[TickData] | str:
        """查询Tick数据"""
        logs: list = []
        ticks: list = self.datafeed.query_tick_history(req, logs.append)

        if logs:
            return " | ".join(logs)
        else:
            return ticks
