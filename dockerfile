FROM ubuntu:20.04
USER root
WORKDIR /app

# RUN apt update \
#     && apt install -y --no-install-recommends wget build-essential \
#     libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev \
#     libgdbm-dev libbz2-dev liblzma-dev zlib1g-dev uuid-dev \
#     libffi-dev libdb-dev \
#     && apt install -y git \
#     && apt upgrade
RUN apt update -y
RUN apt install -y git
RUN apt upgrade -y

# RUN wget --no-check-certificate https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz \
#     && tar -xf Python-3.9.5.tgz \
#     && cd Python-3.9.5 \
#     && ./configure --enable-optimizations \
#     && make \
#     && make install
RUN apt install python3 -y -qq --no-install-recommends
RUN apt install python3-pip -y -qq --no-install-recommends

RUN apt autoremove -y

RUN git clone https://github.com/Hashobrin/skill_sheet_app.git .

COPY requirements.txt /root/

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt