# loadwordteam/SH2MSGConvert
FROM python:3.10-bullseye

RUN mkdir -p /opt/sh2msgconvert

ADD sh2msg /opt/sh2msgconvert/sh2msg
ADD sh2msg.spec /opt/sh2msgconvert
ADD setup.py /opt/sh2msgconvert

SHELL ["/bin/bash", "-c"]

RUN cd /opt/sh2msgconvert \
    && python3 -m venv venv \
    && apt-get update \
    && apt-get install tini -y \
    && source venv/bin/activate \
    && pip3 install pyinstaller -q \
    && pyinstaller sh2msg.spec \
    && cp dist/sh2msg /usr/local/bin \
    && chmod +x /usr/local/bin/sh2msg \
    && cd / && rm -rf /opt/sh2msgconvert

ENTRYPOINT ["tini", "--", "/usr/local/bin/sh2msg"]


