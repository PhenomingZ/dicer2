#!/bin/bash

#  docker run -it -p 9605:9605 --network docker_es7net --rm --link es7_01:elasticsearch dicer2:v0.1.1

VERSION="v0.1.8"
BUILD_DIR=./build/Docker/${VERSION}
DOCKERFILE=./build/Docker/Dockerfile

mkdir ${BUILD_DIR}

pip freeze > requirements.txt

tar -zcf ${BUILD_DIR}/dicer2_${VERSION}_src.tar.gz ./App/ ./manager.py ./requirements.txt ./LICENSE ./README.md

cp ${DOCKERFILE} ${BUILD_DIR}
sed -i "" "s/<version>/${VERSION}/" ${BUILD_DIR}/Dockerfile

cd ${BUILD_DIR}
docker build -t phenoming/dicer2:${VERSION} .

#docker save phenoming/dicer2:${VERSION} | gzip -c > dicer2_${VERSION}_img.tar.gz
#docker push phenoming/dicer2:${VERSION}