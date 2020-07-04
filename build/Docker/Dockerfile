FROM phenoming/dicer2-base:v0.1.5

ENV VERSION="<version>"
ENV DICER2_HOME="/usr/local/dicer2"
ENV PIP_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"
ENV DICER2_CONFIG_PATH="settings/dicer2_docker_config.py"
ENV GUNICORN_CONFIG_PATH="App/settings/gunicorn_config.py"

LABEL version=${VERSION} author="Charles Zhang" email="694556046@qq.com"

RUN mkdir -p ${DICER2_HOME}

WORKDIR ${DICER2_HOME}

ADD dicer2_${VERSION}_src.tar.gz ./

RUN pip install -r requirements.txt -i ${PIP_MIRROR}

EXPOSE 9605 9605

CMD gunicorn -c ${GUNICORN_CONFIG_PATH} manager:app