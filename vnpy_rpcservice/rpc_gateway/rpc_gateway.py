from vnpy.event import Event
from vnpy.rpc import RpcClient
from vnpy.trader.gateway import BaseGateway
from vnpy.trader.object import (
    SubscribeRequest,
    HistoryRequest,
    CancelRequest,
    OrderRequest
)
from vnpy.trader.constant import Exchange
from vnpy.trader.object import (
    BarData,
    ContractData,
    AccountData,
    PositionData,
    OrderData,
    TradeData
)


class RpcGateway(BaseGateway):
    """
    VeighNa用于连接rpc服务的接口。
    """

    default_name: str = "RPC"

    default_setting: dict[str, str] = {
        "主动请求地址": "tcp://127.0.0.1:2014",
        "推送订阅地址": "tcp://127.0.0.1:4102"
    }

    exchanges: list[Exchange] = list(Exchange)

    def __init__(self, event_engine, gateway_name: str) -> None:
        """构造函数"""
        super().__init__(event_engine, gateway_name)

        self.symbol_gateway_map: dict[str, str] = {}

        self.client: "RpcClient" = RpcClient()
        self.client.callback = self.client_callback

    def connect(self, setting: dict) -> None:
        """连接交易接口"""
        req_address: str = setting["主动请求地址"]
        pub_address: str = setting["推送订阅地址"]

        self.client.subscribe_topic("")
        self.client.start(req_address, pub_address)

        self.write_log("服务器连接成功，开始初始化查询")

        self.query_all()

    def subscribe(self, req: SubscribeRequest) -> None:
        """订阅行情"""
        gateway_name: str = self.symbol_gateway_map.get(req.vt_symbol, "")
        self.client.subscribe(req, gateway_name)

    def send_order(self, req: OrderRequest) -> str:
        """委托下单"""
        gateway_name: str = self.symbol_gateway_map.get(req.vt_symbol, "")
        gateway_orderid: str = self.client.send_order(req, gateway_name)

        if gateway_orderid:
            _, orderid = gateway_orderid.split(".")
            return f"{self.gateway_name}.{orderid}"
        else:
            return gateway_orderid

    def cancel_order(self, req: CancelRequest) -> None:
        """委托撤单"""
        gateway_name: str = self.symbol_gateway_map.get(req.vt_symbol, "")
        self.client.cancel_order(req, gateway_name)

    def query_account(self) -> None:
        """查询资金"""
        pass

    def query_position(self) -> None:
        """查询持仓"""
        pass

    def query_history(self, req: HistoryRequest) -> list[BarData]:
        """查询历史数据"""
        gateway_name: str = self.symbol_gateway_map.get(req.vt_symbol, "")
        return self.client.query_history(req, gateway_name)

    def query_all(self) -> None:
        """查询基础信息"""
        contracts: list[ContractData] = self.client.get_all_contracts()
        for contract in contracts:
            self.symbol_gateway_map[contract.vt_symbol] = contract.gateway_name
            contract.gateway_name = self.gateway_name
            self.on_contract(contract)
        self.write_log("合约信息查询成功")

        accounts: list[AccountData] = self.client.get_all_accounts()
        for account in accounts:
            account.gateway_name = self.gateway_name
            account.__post_init__()
            self.on_account(account)
        self.write_log("资金信息查询成功")

        positions: list[PositionData] = self.client.get_all_positions()
        for position in positions:
            position.gateway_name = self.gateway_name
            position.__post_init__()
            self.on_position(position)
        self.write_log("持仓信息查询成功")

        orders: list[OrderData] = self.client.get_all_orders()
        for order in orders:
            order.gateway_name = self.gateway_name
            order.__post_init__()
            self.on_order(order)
        self.write_log("委托信息查询成功")

        trades: list[TradeData] = self.client.get_all_trades()
        for trade in trades:
            trade.gateway_name = self.gateway_name
            trade.__post_init__()
            self.on_trade(trade)
        self.write_log("成交信息查询成功")

    def close(self) -> None:
        """关闭连接"""
        self.client.stop()
        self.client.join()

    def client_callback(self, topic: str, event: Event) -> None:
        """回调函数"""
        if event is None:
            print("none event", topic, event)
            return

        data: object = event.data

        if hasattr(data, "gateway_name"):
            data.gateway_name = self.gateway_name

        if isinstance(data, (PositionData, AccountData, OrderData, TradeData)):
            data.__post_init__()

        self.event_engine.put(event)
