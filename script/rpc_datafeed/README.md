# RPC数据服务

用于将某些限制只能单点登录（IP或者进程）的数据服务，共享给多个VeighNa Trader进程，仅建议在本机或者局域网内使用。

请将datafeed_server.py和run_trader.py两个启动脚本分别放置在不同的目录中，每个目录包含独立的.vntrader文件夹：

* datafeed_server.py
    * 所在目录的.vntrader\vt_setting.json中，请配置datafeed相关字段为实际要使用的数据服务（如rqdata）
* run_trader.py
    * 所在目录的.vntrader\vt_setting.json中，请参考run_trader.py文件中头部的SETTINGS内容修改datafeed相关字段

注意两边的端口号需要匹配。
