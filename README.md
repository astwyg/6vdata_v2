# 6vdata_v2
6vdata是一个面向A股市场的数据分析平台和工具.

# 依赖

* python 3.6
* python依赖: 见requirments.txt
* mongodb 3.2.22
* mysql 尚未决定

# 目录结构

* env: 基于py3.6的运行环境, 希望控制项目大小, 所以不拆分环境
* webserver: 基于Django的web服务
* server: server端工具, 主要是数据采集
* data: 数据
* tools: 数据转移, 备份等工具


# dev blog

## 2019-5-25 10:48:03
在6vdata申请之初, 本来只是希望练练手, 做点数据分析, 顺便吸点流量, 后来机缘巧合, 居然走到了VC(venture capital)岗位上, 居然真的要在工作中分析A股市场了, 因此推倒之前的第一版, 重新来做.

本周末计划先搭起来webserver架子, 设计好接口, 开始每天抓全部上市公司相关的公众号文章, 从数据积累开始.
接下来会搬上来年报查询工具.

TODO:

- [] log还没搞.