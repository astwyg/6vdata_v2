# 6vdata_v2
6vdata是一个面向A股市场的数据分析平台和工具.
请访问: http://6vdata.com

# 依赖

* python 3.6
* python依赖: 见requirments.txt
* mongodb 3.2.22
* mysql 5.7.26

# 目录结构

* env: 基于py3.6的运行环境, 希望控制项目大小, 所以不拆分环境
* webserver: 基于Django的web服务
* server: server端工具, 主要是数据采集
* data: 数据
* tools: 数据转移, 备份等工具

# 特别感谢

* [tushare](https://tushare.pro/)提供股票基础数据

# 坑

* 在linux下, 尤其是只有命令行的状态下, chrome driver很难跑起来, 常常报`chromedriver unexpectedly exited. Status code was: 127`, 可以用`sudo apt-get install -y chromium-browser`一把解决依赖问题.
* 在linux下, 尤其是只有命令行的状态下, chrome driver很难跑起来, 除了依赖, 而且没有屏幕, 此问题参考[这里](https://stackoverflow.com/questions/10399557/is-it-possible-to-run-selenium-firefox-web-driver-without-a-gui)
* 在linux, 记得安装`apt install python3.6-dev`, 否则mysql连接器各种奇奇怪怪报错.

# dev blog

## 2019-5-25 10:48:03
在6vdata申请之初, 本来只是希望练练手, 做点数据分析, 顺便吸点流量, 后来机缘巧合, 居然走到了VC(venture capital)岗位上, 居然真的要在工作中分析A股市场了, 因此推倒之前的第一版, 重新来做.

本周末计划先搭起来webserver架子, 设计好接口, 开始每天抓全部上市公司相关的公众号文章, 从数据积累开始.
接下来会搬上来年报查询工具.

TODO:

- [ ] log还没搞.

