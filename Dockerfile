FROM python:3.7-alpine

# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
#     && cat /etc/apk/repositories \
#     && echo -e "[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted-host=mirrors.aliyun.com">>/etc/pip.conf 
RUN apk add --update build-base python-dev python && pip install --upgrade pip \
    && pip install cython numpy gunicorn  && pip install pandas
# RUN apk add --update build-base python python-dev py-pip && pip install --upgrade pip

# https://github.com/9fevrier/docker-python-ta-lib/blob/master/Dockerfile
COPY deps/ta-lib-0.4.0-src.tar.gz .
RUN tar xvf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib \
    && sed -i 's/^#define TA_IS_ZERO(v).*$/#define TA_IS_ZERO(v) (((-0.000000000000000001)<v)\&\&(v<0.000000000000000001))/' src/ta_func/ta_utility.h \
    && sed -i 's/^#define TA_IS_ZERO_OR_NEG(v).*$/#define TA_IS_ZERO_OR_NEG(v) (v<0.000000000000000001)/' src/ta_func/ta_utility.h \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && cd .. \
    && rm -rf ta-lib \
    && rm ta-lib-0.4.0-src.tar.gz