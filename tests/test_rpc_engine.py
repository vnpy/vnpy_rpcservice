from vnpy.event import EventEngine
from vnpy.rpc.server import RpcServer
from vnpy.trader.constant import Direction, Exchange, Offset, OrderType, Status
from vnpy.trader.object import OrderData, PositionData

from vnpy_rpcservice.rpc_service.engine import RpcEngine


class FakeMainEngine:
    def __init__(self, order: OrderData, position: PositionData) -> None:
        self.order: OrderData = order
        self.position: PositionData = position

    def subscribe(self, *args: object) -> None:
        return None

    def send_order(self, *args: object) -> str:
        return ""

    def cancel_order(self, *args: object) -> None:
        return None

    def query_history(self, *args: object) -> list[object]:
        return []

    def get_tick(self, *args: object) -> None:
        return None

    def get_order(self, vt_orderid: str) -> OrderData | None:
        if vt_orderid == self.order.vt_orderid:
            return self.order
        return None

    def get_trade(self, *args: object) -> None:
        return None

    def get_position(self, vt_positionid: str) -> PositionData | None:
        if vt_positionid == self.position.vt_positionid:
            return self.position
        return None

    def get_account(self, *args: object) -> None:
        return None

    def get_contract(self, *args: object) -> None:
        return None

    def get_all_ticks(self) -> list[object]:
        return []

    def get_all_orders(self) -> list[OrderData]:
        return [self.order]

    def get_all_trades(self) -> list[object]:
        return []

    def get_all_positions(self) -> list[PositionData]:
        return [self.position]

    def get_all_accounts(self) -> list[object]:
        return []

    def get_all_contracts(self) -> list[object]:
        return []

    def get_all_active_orders(self) -> list[object]:
        return []


def close_server(server: RpcServer) -> None:
    server._context.destroy(linger=0)


def make_engine() -> tuple[RpcEngine, OrderData, PositionData]:
    order: OrderData = OrderData(
        gateway_name="TEST",
        symbol="rb2510",
        exchange=Exchange.SHFE,
        orderid="1001",
        type=OrderType.LIMIT,
        direction=Direction.LONG,
        offset=Offset.OPEN,
        price=3510,
        volume=2,
        traded=0,
        status=Status.NOTTRADED,
    )
    position: PositionData = PositionData(
        gateway_name="TEST",
        symbol="ag2506",
        exchange=Exchange.SHFE,
        direction=Direction.SHORT,
        volume=5,
        frozen=1,
        price=7800,
        pnl=12.5,
        yd_volume=4,
    )
    engine: RpcEngine = RpcEngine(FakeMainEngine(order, position), EventEngine())
    return engine, order, position


def test_registered_get_order_returns_local_order() -> None:
    engine, order, _position = make_engine()
    try:
        assert engine.server.is_active() is False
        found: OrderData | None = engine.server._functions["get_order"](order.vt_orderid)
        assert found is order
        assert found.symbol == "rb2510"
        assert found.exchange == Exchange.SHFE
        assert found.orderid == "1001"
        assert found.vt_orderid == "TEST.1001"
        assert found.direction == Direction.LONG
        assert found.offset == Offset.OPEN
        assert found.type == OrderType.LIMIT
        assert found.price == 3510
        assert found.volume == 2
        assert found.status == Status.NOTTRADED
    finally:
        close_server(engine.server)


def test_registered_get_position_returns_local_position() -> None:
    engine, _order, position = make_engine()
    try:
        assert engine.server.is_active() is False
        found: PositionData | None = engine.server._functions["get_position"](position.vt_positionid)
        assert found is position
        assert found.symbol == "ag2506"
        assert found.exchange == Exchange.SHFE
        assert found.direction == Direction.SHORT
        assert found.volume == 5
        assert found.frozen == 1
        assert found.price == 7800
        assert found.pnl == 12.5
        assert found.yd_volume == 4
        assert found.vt_symbol == "ag2506.SHFE"
        assert found.vt_positionid == "TEST.ag2506.SHFE." + Direction.SHORT.value
    finally:
        close_server(engine.server)
