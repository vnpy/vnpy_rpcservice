"""启动 RPC 数据服务的示例脚本。"""
from vnpy.event import EventEngine
from vnpy_rpcservice import DatafeedServer


REP_ADDRESS = "tcp://*:66001"
PUB_ADDRESS = "tcp://*:66002"


def main() -> None:
    """启动事件引擎和数据服务，按下回车后停止。"""
    event_engine = EventEngine()
    event_engine.start()

    server = DatafeedServer(event_engine)
    server.start(REP_ADDRESS, PUB_ADDRESS)

    input()

    event_engine.stop()
    server.stop()


if __name__ == "__main__":
    main()
