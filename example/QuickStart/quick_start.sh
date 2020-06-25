#!/bin/bash

# 创建一个课程
curl --location --request POST 'localhost:9605/machine-learning/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "机器学习"
}'

# 为刚创建的课程创建两个年级
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

# 上传学生的作业文档
curl --location --request POST 'localhost:9605/machine-learning/2019-spring/SY1906000/' \
--form 'file=@docs/SY1906000.docx' \
--form 'title=李四的机器学习结课论文'

curl --location --request POST 'localhost:9605/machine-learning/2019-spring/SY1906001/' \
--form 'file=@docs/SY1906001.docx' \
--form 'title=王五的机器学习结课论文'

curl --location --request POST 'localhost:9605/machine-learning/2020-spring/SY2006000/' \
--form 'file=@docs/SY2006000.docx' \
--form 'title=张三的机器学习结课论文'

# 进行查重
curl --location --request GET 'localhost:9605/_single/_search/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "index": "machine-learning",
    "task": "2020-spring",
    "document": "SY2006000",
    "search_range": {
        "machine-learning": ["2019-spring", "2020-spring"]
    }
}'
