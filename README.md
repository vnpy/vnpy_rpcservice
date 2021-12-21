# vn.py框架的RPC服务应用

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.0.0-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-linux|windows|mac-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.7-blue.svg" />
</p>

## 说明

基于pyzmq开发的RPC服务模块，允许将某一vn.py进程启动为服务端，作为统一的行情和交易路由通道，允许多客户端同时连接，实现实现跨进程或者跨网络的分布式系统。

## 安装

安装需要基于2.9.0版本以上的[VN Studio](https://www.vnpy.com)。

直接使用pip命令：

```
pip install vnpy_rpcservice
```

下载解压后在cmd中运行

```
python setup.py install
```
