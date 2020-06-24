<p align="center">
      <img src="./static/logo.png" width="200">
</p>

<p align="center">基于ElasticSearch的高效中文文档查重服务</p>

<p align="center">
   <a href="#introduction">Introduction</a> •
   <a href="#install">Install</a> •
   <a href="#change-log">Change Log</a> •
   <a href="#getting-start">Getting Start</a> •
   <a href="#api">API</a> •
   <a href="#tutorials">Tutorials</a> •
   <a href="#faq">FAQ</a>
</p>



<h6 align="center">Made by Charles Zhang • <a href="http://phenoming.gitee.io/charlesblog/">http://phenoming.gitee.io/charlesblog/</a></h6>



<h2 id="introduction" align="center">Introduction</h2>

**DICER2**（读作`/daisə tuː/`）是一个基于**ElasticSearch**的高效中文文档查重服务。它致力于帮助用户搭建有自建文档库需求的中文文档查重服务，并且支持集群部署与横向扩展。**DICER2**使用**Gunicorn + Flask App**提供多进程的web服务用于接收RESTful请求，使用**Elasticsearch**作为文档索引和存储数据库，可满足大并发的生产环境的使用。

<h2 id="install" align="center">Install</h2>

当前版本（v0.1.2）推荐使用**Docker-Compose**环境部署和使用**DICER2**。由于**DICER2**依赖于**ElasticSearch**集群环境，我们提供了相关镜像和**YAML**文件用于一键部署完整的应用环境，具体步骤如下：

### 1. 安装Docker-Compose

安装**Docker-Compose**的方法本文不再赘述，可以参考如下内容：

*   官方文档：[Docker-Compose Github](https://github.com/docker/compose)
*   中文教程：[Docker-Compose 菜鸟教程](https://www.runoob.com/docker/docker-compose.html)

### 2. 下载YAML文件

本文提供的YAML文件由如下三部分组成：

*   DICER2服务
*   ElasticSearch集群
*   集群管理工具Cerebro

[yaml](./build/Docker/v0.1.2/dicer2-docker-compose.yaml)

