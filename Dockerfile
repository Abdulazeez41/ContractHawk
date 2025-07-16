FROM python:3.11-bullseye as base

RUN apt-get update && apt-get install -y \
    curl wget git gnupg \
    build-essential libssl-dev zlib1g-dev libbz2-dev \
    ca-certificates

RUN curl -fsSL https://deb.nodesource.com/setup_18.x  | bash - && \
    apt-get install -y nodejs


RUN pip install solc-select

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

FROM base as dev

RUN pip install slither-analyzer==0.11.3

RUN pip install mythril

RUN npm install -g solhint

COPY solc-static-linux /usr/local/bin/solc
RUN chmod +x /usr/local/bin/solc && \
    /usr/local/bin/solc --version

COPY . .