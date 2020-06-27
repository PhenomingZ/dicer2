FROM phenoming/dicer2-base:v0.1.0

ENV PIP_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"

LABEL version=${VERSION} author="Charles Zhang" email="694556046@qq.com"

COPY requirements.txt ./

RUN pip install -r requirements.txt -i ${PIP_MIRROR}
