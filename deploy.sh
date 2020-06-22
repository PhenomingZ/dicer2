#!/bin/bash

# docker run -it -p 9605:9605 --network 7x-docker-2-es-instances_es7net --link es7_01:elastic dicer2:v0.1.0

VERSION="v0.1.0"
BUILD_DIR=./build/Docker/${VERSION}
DOCKERFILE=./build/Docker/Dockerfile

mkdir ${BUILD_DIR}

tar -zcf ${BUILD_DIR}/dicer2_${VERSION}_src.tar.gz ./App/ ./manager.py ./requirements.txt ./LICENSE ./README.md

cp ${DOCKERFILE} ${BUILD_DIR}
sed -i "" "s/<version>/${VERSION}/" ${BUILD_DIR}/Dockerfile

cd ${BUILD_DIR}
docker build -t dicer2:${VERSION} .

#docker save dicer2:${VERSION} | gzip -c > dicer2_${VERSION}_img.tar.gz