<p align="center">
      <img src="./static/logo.png" width="200">
</p>

<p align="center">基于ElasticSearch的高效中文文档查重服务</p>

<p align="center">
   <a href="#introduction">Introduction</a> •
   <a href="#setup">Setup DICER2</a> •
   <a href="#change-log">Change Log</a> •
   <a href="#getting-start">Getting Start</a> •
   <a href="#api">API</a> •
   <a href="#tutorials">Tutorials</a> •
   <a href="#faq">FAQ</a>
</p>




<h6 align="center">Made by Charles Zhang • <a href="http://phenoming.gitee.io/charlesblog/">http://phenoming.gitee.io/charlesblog/</a></h6>



<h2 id="introduction" align="center">Introduction</h2>

**DICER2**（读作`/daisə tuː/`）是一个基于**ElasticSearch**的高效中文文档查重服务。它致力于帮助用户搭建有自建文档库需求的中文文档查重服务，并且支持集群部署与横向扩展。**DICER2**使用**Gunicorn + Flask App**提供多进程的web服务用于接收RESTful请求，使用**Elasticsearch**作为文档索引和存储数据库，可满足大并发的生产环境的使用。

<h2 id="Setup" align="center">Setup DICER2</h2>

当前版本（v0.1.2）推荐使用**Docker-Compose**环境部署和使用**DICER2**。由于**DICER2**依赖于**ElasticSearch**集群环境，我们提供了相关镜像和**YAML**文件用于一键部署完整的应用环境，具体步骤如下：

### 1. 安装Docker-Compose

安装**Docker-Compose**的方法本文不再赘述，可以参考如下内容：

*   官方文档：[Docker-Compose Github](https://github.com/docker/compose)
*   中文教程：[Docker-Compose 菜鸟教程](https://www.runoob.com/docker/docker-compose.html)

### 2. 下载YAML文件

本文提供的YAML文件由如下三部分组成：

*   DICER2服务
*   ElasticSearch集群
*   Cerebro管理工具

下载地址：[点击下载](./build/Docker/v0.1.2/dicer2-docker-compose.yaml)

### 3. 启动服务

>    **DICER2**默认监听`9605`端口，**ElasticSearch**默认监听`9200`端口，**Cerebro**默认监听`9000`端口，启动服务前请确保这些端口没有冲突。

首先在终端中切换至**YAML**文件所在的目录，并确保该目录中有且仅有刚刚下载的一个**YAML**文件，之后执行如下命令启动服务：

```bash
docker-compose up
```

>   通过该命令启动之后，Docker会自动拉取所需的镜像。

如果因网络原因，无法顺利拉取镜像，也可预先下载好所需镜像并导入本机后再启动服务，所需镜像拉取命令如下：

```bash
docker pull phenoming/dicer2:v0.1.2
docker pull phenoming/elasticsearch:v0.1.1
docker pull phenoming/cerebro:v0.1.1
```

启动后终端中会输出大量日志，当发现停止输出日志时即为启动完成。

### 4. 检查服务

使用`docker ps`检查启动的容器，应当能找到如下几个正在运行的容器：

```bash
$ docker ps
IMAGE                            STATUS          NAMES
phenoming/dicer2:v0.1.2          Up 2 seconds    dicer2
phenoming/cerebro:v0.1.1         Up 2 seconds    cerebro
phenoming/elasticsearch:v0.1.1   Up 2 seconds    es7_01
phenoming/elasticsearch:v0.1.1   Up 2 seconds    es7_02
```

使用如下命令检查**DICER2**是否启动成功：

```bash
curl --location --request GET 'http://localhost:9605/'
```

应当得到输出如下：

```json
{
    "name": "Dicer2",
    "version": {
        "dicer2_version": "v0.1.2",
        "elastic_search_version": "7.6.2"
    },
    "msg": "Check your documents cooler!"
}
```

恭喜，**DICER2**服务启动完成！

