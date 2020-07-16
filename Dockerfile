FROM ubuntu:16.04

RUN DEBIAN_FRONTEND=noninteractive

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHON_VERSION 3.6.8
ENV HOME /root
ENV PYTHON_ROOT $HOME/local/python-$PYTHON_VERSION
ENV PATH $PYTHON_ROOT/bin:$PATH
ENV PYENV_ROOT $HOME/.pyenv

RUN apt-get update && apt-get upgrade -y \
 && apt-get install -y \
    git \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    chromium-chromedriver \
    vim \
 && git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT \
 && $PYENV_ROOT/plugins/python-build/install.sh \
 && /usr/local/bin/python-build -v $PYTHON_VERSION $PYTHON_ROOT \
 && rm -rf $PYENV_ROOT

# RUN cp /usr/lib/chromium-browser/chromedriver /usr/bin

# pipenv install
RUN pip install pipenv

WORKDIR /work
COPY Pipfile ./work
COPY config.yaml ./work
COPY race.py ./work
COPY endpoints.py ./work

RUN pipenv install --system --skip-lock

VOLUME ["/work"]