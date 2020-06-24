#!/bin/bash

# 创建一个课程
curl --location --request POST 'localhost:9605/machine-learning/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "机器学习"
}'

# 为刚创建的课程创建一个班级
curl --location --request POST 'localhost:9605/machine-learning/2020-spring/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title": "2020年机器学习春季班"
}'

# 上传学生的作业文档
curl --location --request POST 'localhost:9605/machine-learning/2020-spring/SY1806700/' \
--form 'file=@docs/SY1806700.docx' \
--form 'title=软件测试技术课程心得体会'

curl --location --request POST 'localhost:9605/machine-learning/2020-spring/SY1806701/' \
--form 'file=@docs/SY1806701.docx' \
--form 'title=软件测试技术课程心得体会'

curl --location --request POST 'localhost:9605/machine-learning/2020-spring/SY1806702/' \
--form 'file=@docs/SY1806702.docx' \
--form 'title=软件测试技术课程心得体会'