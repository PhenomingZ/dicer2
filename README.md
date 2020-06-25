<p align="center">
      <img src="./static/logo.png" width="200">
</p>

<p align="center">基于ElasticSearch的高效中文文档查重服务</p>

<p align="center">
   <a href="#introduction">Introduction</a> •
   <a href="#change-log">Change Log</a> •
   <a href="#setup-dicer2">Setup DICER2</a> •
   <a href="#getting-start">Getting Start</a> •
   <a href="#api">API</a> •
   <a href="#tutorials">Tutorials</a> •
   <a href="#faq">FAQ</a>
</p>


<h6 align="center">Made by Charles Zhang • <a href="http://phenoming.gitee.io/charlesblog/">http://phenoming.gitee.io/charlesblog/</a></h6>



<h2 id="introduction" align="center">Introduction</h2>

**DICER2**（读作`/daisə tuː/`）是一个基于**ElasticSearch**的高效中文文档查重服务。它致力于帮助用户搭建有自建文档库需求的中文文档查重服务，并且支持集群部署与横向扩展。**DICER2**使用**Gunicorn + Flask App**提供多进程的web服务用于接收RESTful请求，使用**Elasticsearch**作为文档索引和存储数据库，可满足大并发的生产环境的使用。

<h2 id="change-log" align="center">Change Log</h2>

**v0.1.3 Change Log (2020.06.24)**
1. 对于index、task和document的接口中的POST请求增加了不能以下划线开头的限制，所有的以下划线开头的路由均作为保留字
2. 修改了单文档查重的路由，由`single/_search`改为`_single/_search`
3. 优化了默认配置项中Jaccard距离的阈值为0.4（从0.5下调）

**v0.1.2 Change Log (2020.06.24)**  
1. 解决了DICER2在ElasticSearch集群未启动的情况下无法启动的问题
2. 添加了异常处理钩子，解决了运行过程中ElasticSearch集群无法连接的情况下无法返回有效的错误信息的问题
3. 添加了自定义的JSON格式化类DateEncoder，用于处理返回数据中的datetime格式的字段
4. 添加了新路由_summary，可以接收GET请求，用于获取整个DICER2存储的数据目录

**v0.1.1 Change Log (2020.06.23)**  
1. 完善了DICER2的部署流程
2. 添加了适用于各个版本的Dockerfile和docker-compose.yaml

点击链接查看完整的更新日志：[点击查看](CHANGELOG.md)

<h2 id="setup-dicer2" align="center">Setup DICER2</h2>

当前版本（v0.1.3）推荐使用**Docker-Compose**环境部署和使用**DICER2**。由于**DICER2**依赖于**ElasticSearch**集群环境，提供了相关镜像和**YAML**文件用于一键部署完整的应用环境，具体步骤如下：

### 1. 安装Docker-Compose

安装**Docker-Compose**的方法本文不再赘述，可以参考如下内容：

*   官方文档：[Docker-Compose Github](https://github.com/docker/compose)
*   中文教程：[Docker-Compose 菜鸟教程](https://www.runoob.com/docker/docker-compose.html)

### 2. 下载YAML文件

本文提供的YAML文件由如下三部分组成：

*   DICER2服务
*   ElasticSearch集群
*   Cerebro管理工具

下载地址：[点击下载](build/Docker/v0.1.3/docker-compose.yaml)

### 3. 启动服务

>    **DICER2**默认监听`9605`端口，**ElasticSearch**默认监听`9200`端口，**Cerebro**默认监听`9000`端口
>
>   启动服务前请确保这些端口没有冲突。

首先在终端中切换至**YAML**文件所在的目录，并确保该目录中有且仅有刚刚下载的一个名为`docker-compose.yaml`的文件，之后执行如下命令启动服务：

```bash
docker-compose up
```

>   通过该命令启动之后，Docker会自动拉取所需的镜像。

如果因网络原因，无法顺利拉取镜像，也可预先下载好所需镜像并导入本机后再启动服务，所需镜像拉取命令如下：

```bash
docker pull phenoming/dicer2:v0.1.3
docker pull phenoming/elasticsearch:v0.1.1
docker pull phenoming/cerebro:v0.1.1
```

启动后终端中会输出大量日志，当发现停止输出日志时即为启动完成。

### 4. 检查服务

使用`docker ps`检查启动的容器，应当能找到如下几个正在运行的容器：

```bash
$ docker ps
IMAGE                            STATUS          NAMES
phenoming/dicer2:v0.1.3          Up 2 seconds    dicer2
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
        "dicer2_version": "v0.1.3",
        "elastic_search_version": "7.6.2"
    },
    "msg": "Check your documents cooler!"
}
```

恭喜，**DICER2**服务启动完成！

<h2 id="getting-start" align="center">Getting Start</h2>

现在是时候通过一个简单案例体验一下**DICER2**的强大功能！假设一位高校教师提出了如下需求：

>   我是一位**机器学习**课程的教师，目前**2020**年上学期接近尾声，本学期的考核方式是完成一篇**结课论文**。我希望能检查出我的学生是否有**抄袭**往届学生作业的现象，谢谢。

分析这位教师的需求，首先她需要根据不同的年级存储学生提交的作业，之后她需要检查出不同年级的作业之间是否存在抄袭。下面我们使用**DICER2**实现这个需求：

### 1. 创建课程

>   注意：本章节所有的操作均使用curl命令在终端中向DICER2服务发送请求，也可以使用如POSTMAN等可视化工具完成。

根据需求，这位教师负责的课程是**机器学习**，首先为她在**DICER2**中创建这门课程，命令如下：

```bash
curl --location --request POST 'localhost:9605/machine-learning/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "机器学习"
}'
```

在该命令中，我们使用POST请求创建了一个名为`machine-learning`的课程，还为该课程指定了一个中文全称。

获得返回值如下即表明创建成功：

```json
{
    "meta": {
        "took": 208,
        "msg": "CREATED",
        "status": 201
    },
    "data": {
        "index": "machine-learning",
        "title": "机器学习"
    }
}
```

某些终端可能会将中文字符以Unicode转义的形式返回，并不影响中文字符的存储，如下所示：

```json
{
    "meta": {
        "took": 247, 
        "msg": "CREATED", 
        "status": 201
    }, 
    "data": {
        "index": "machine-learning", 
        "title": "\u673a\u5668\u5b66\u4e60"
    }
}
```

### 2. 创建年级

根据需求，我们希望不同年级的学生提交的作业可以分类保存，下面就在刚刚创建的课程中添加两个年级：

```bash
curl --location --request POST 'localhost:9605/machine-learning/2019-spring/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "2019年机器学习春季班"
}'

curl --location --request POST 'localhost:9605/machine-learning/2020-spring/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "2020年机器学习春季班"
}'
```

上面两条命令中，我们为`machine-learning`课程创建了两个年级`2019-spring`和`2020-spring`，并且分别为它们指定了中文全称。

获得返回值如下：

```json
{
    "meta": {
        "took": 24,
        "msg": "CREATED",
        "status": 201
    },
    "data": {
        "index": "machine-learning",
        "task": "2019-spring",
        "title": "2019年机器学习春季班"
    }
}

{
    "meta": {
        "took": 22,
        "msg": "CREATED",
        "status": 201
    },
    "data": {
        "index": "machine-learning",
        "task": "2020-spring",
        "title": "2020年机器学习春季班"
    }
}
```

### 3. 上传作业文档

接下来要做的就是把学生的作业文档上传到服务器上，我们现在拿到了两篇2019年级的作业和一篇2020年级的作业，它们的内容如下：

>   2019年级第一篇作业：[点击下载](example/QuickStart/docs/SY1906001.docx)

```
机器学习(Machine Learning, ML)是一门多领域交叉学科，涉及概率论、统计学、逼近论、凸分析、算法复杂度理论等多门学科。专门研究计算机怎样模拟或实现人类的学习行为，以获取新的知识或技能，重新组织已有的知识结构使之不断改善自身的性能。它是人工智能的核心，是使计算机具有智能的根本途径，其应用遍及人工智能的各个领域，它主要使用归纳、综合而不是演绎。
```

>    2019年级第二篇作业：[点击下载](example/QuickStart/docs/SY1906002.docx)

```
机器的能力是否能超过人的，很多持否定意见的人的一个主要论据是：机器是人造的，其性能和动作完全是由设计者规定的，因此无论如何其能力也不会超过设计者本人。这种意见对不具备学习能力的机器来说的确是对的，可是对具备学习能力的机器就值得考虑了，因为这种机器的能力在应用中不断地提高，过一段时间之后，设计者本人也不知它的能力到了何种水平。
```

>   2020年级第一篇作业：[点击下载](example/QuickStart/docs/SY2006000.docx)

```
说到人工智能必然要了解机器学习，从信息化软件，到电子商务，然后到高速发展互联网时代，到至今的云计算、大数据等，渗透到我们的生活、工作之中，在互联网的驱动下，人们更清晰的认识和使用数据，不仅仅是数据统计、分析，我们还强调数据挖掘、预测。
机器学习是一门研究计算机是如何模拟或实现人类行为，获取新知识并将其重新整理为现有的知识体系以此来提升自身能力和性能。
有些人认为，机器是由人生产的，其动作也是完全根据人类的设计决定的，人类完全不必担心机器会超过人类。
```

