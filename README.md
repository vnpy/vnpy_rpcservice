# VeighNa框架的RPC服务应用

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-1.0.2-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-linux|windows|mac-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.7|3.8|3.9|3.10-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## 说明

基于pyzmq开发的RPC服务模块，允许将某一VeighNa进程启动为服务端，作为统一的行情和交易路由通道，允许多客户端同时连接，实现实现跨进程或者跨网络的分布式系统。

## 安装

安装环境推荐基于3.0.0版本以上的【[**VeighNa Studio**](https://www.vnpy.com)】。

直接使用pip命令：

```
pip install vnpy_rpcservice
```


或者下载源代码后，解压后在cmd中运行：

```
pip install .
```
