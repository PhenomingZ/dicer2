# docker run -it -p 9605:9605 --network 7x-docker-2-es-instances_es7net --link es7_01:elastic dicer2:v0.1.0

FROM python:3.7.3

ENV VERSION="v0.1.0"
ENV DICER2_HOME="/usr/local/dicer2"
ENV PIP_MIRROR="https://pypi.mirrors.ustc.edu.cn/simple/"
ENV DICER2_CONFIG_PATH="settings/dicer2.docker.config.py"

LABEL version=${VERSION} author="Charles Zhang" email="694556046@qq.com"

RUN mkdir ${DICER2_HOME}

WORKDIR ${DICER2_HOME}

ADD dicer2_${VERSION}.tar.gz ./

RUN pip install -r requirements.txt -i ${PIP_MIRROR}

EXPOSE 9605 9605

ENTRYPOINT gunicorn manager:app -b 0.0.0.0:9605
