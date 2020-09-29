# Trouble Shooting

## 1. ElasticSearch 启动报虚拟内存过低 - max virtual memory areas is too low
### 问题描述
max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
### 解决方案
```bash
sudo vi /etc/sysctl.conf

# 在最后一行添加 
vm.max_map_count=655360

# 保存退出后执行
sudo sysctl -p
```

再次启动 elasticsearch 即可。
