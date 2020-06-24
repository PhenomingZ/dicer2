**v0.1.2 Change Log (2020.06.24)**  
1. 解决了DICER2在ElasticSearch集群未启动的情况下无法启动的问题
2. 添加了异常处理钩子，解决了运行过程中ElasticSearch集群无法连接的情况下无法返回有效的错误信息的问题
3. 添加了自定义的JSON格式化类DateEncoder，用于处理返回数据中的datetime格式的字段
4. 添加了新路由_summary，可以接收GET请求，用于获取整个DICER2存储的数据目录
5. 对于index、task和document的接口中的POST请求增加了不能以下划线开头的限制，所有的以下划线开头的路由均作为保留字

**v0.1.1 Change Log (2020.06.23)**  
1. 完善了DICER2的部署流程
2. 添加了适用于各个版本的Dockerfile和docker-compose.yaml