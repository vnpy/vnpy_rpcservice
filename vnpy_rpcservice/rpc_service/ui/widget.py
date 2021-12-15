from vnpy.event import EventEngine, Event
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import QtWidgets, QtCore
from ..engine import APP_NAME, EVENT_RPC_LOG


class RpcManager(QtWidgets.QWidget):
    """"""
    signal_log = QtCore.pyqtSignal(Event)

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        """构造函数"""
        super().__init__()

        self.main_engine: MainEngine = main_engine
        self.event_engine: EventEngine = event_engine

        self.rpc_engine = main_engine.get_engine(APP_NAME)

        self.init_ui()
        self.register_event()

    def init_ui(self) -> None:
        """初始化界面"""
        self.setWindowTitle("RPC服务")
        self.setFixedWidth(900)
        self.setFixedHeight(500)

        self.start_button = QtWidgets.QPushButton("启动")
        self.start_button.clicked.connect(self.start_server)

        self.stop_button = QtWidgets.QPushButton("停止")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)

        for button in [self.start_button, self.stop_button]:
            hint = button.sizeHint()
            button.setFixedHeight(hint.height() * 2)
            button.setFixedWidth(hint.width() * 4)

        self.rep_line = QtWidgets.QLineEdit(self.rpc_engine.rep_address)
        self.rep_line.setFixedWidth(300)

        self.pub_line = QtWidgets.QLineEdit(self.rpc_engine.pub_address)
        self.pub_line.setFixedWidth(300)

        self.log_monitor = QtWidgets.QTextEdit()
        self.log_monitor.setReadOnly(True)

        form = QtWidgets.QFormLayout()
        form.addRow("请求响应地址", self.rep_line)
        form.addRow("事件广播地址", self.pub_line)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(form)
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addStretch()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.log_monitor)

        self.setLayout(vbox)

    def register_event(self) -> None:
        """注册事件"""
        self.signal_log.connect(self.process_log_event)

        self.event_engine.register(EVENT_RPC_LOG, self.signal_log.emit)

    def process_log_event(self, event: Event) -> None:
        """调用事件"""
        log = event.data
        msg: str = f"{log.time}\t{log.msg}"
        self.log_monitor.append(msg)

    def start_server(self) -> None:
        """启动服务"""
        rep_address: str = self.rep_line.text()
        pub_address: str = self.pub_line.text()

        result = self.rpc_engine.start(rep_address, pub_address)
        if result:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

    def stop_server(self) -> None:
        """停止服务"""
        result = self.rpc_engine.stop()
        if result:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
