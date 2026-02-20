FROM ghcr.io/actions/actions-runner:2.330.0

USER root
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
ENV PYTHON_VERSION=3.13.7

# 1) Paquetes base + GitHub CLI + utilidades
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
        dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        gh \
        wget \
        jq \
        x11-apps \
        unzip \
        locales \
        lsb-release \
        apt-transport-https \
        tar \
        rsync \
        openssh-client \
        sshpass \
        telnet \
        xz-utils \
        netcat-openbsd \
        build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
        libsqlite3-dev libffi-dev liblzma-dev tk-dev \
        gzip && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8 && \
    update-ca-certificates

# 2) Instalar Python
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations --with-ensurepip=install && \
    make -j"$(nproc)" && \
    make altinstall && \
    cd .. && \
    rm -rf Python-${PYTHON_VERSION}*

# 3) Alias python/pip
RUN ln -s /usr/local/bin/python3.13 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3.13 /usr/local/bin/pip

# ✅ 4) FIX IMPORTANTE AQUÍ
RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir \
        selenium \
        pytest \
        pytest-cov \
        requests \
        allure-pytest \
        flake8 \
        jaraco-context==6.1.0 \
        wheel==0.46.2

# 5) Instalar Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | \
    gpg --dearmor | tee /usr/share/keyrings/google-chrome.gpg > /dev/null && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] https://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# 6) ChromeDriver dinámico
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | tr -d '\r') && \
    CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1) && \
    CHROMEDRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_MAJOR_VERSION | tr -d '\r') && \
    wget -q -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip -qq /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/*

# 7) GeckoDriver
RUN GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r .tag_name | tr -d '\r') && \
    wget -q https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-linux64.tar.gz && \
    tar -xzf geckodriver-${GECKO_VERSION}-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-${GECKO_VERSION}-linux64.tar.gz

# 8) Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# 9) Workspace
RUN mkdir -p /workspace && \
    chown -R runner:runner /workspace

# 10) Validación
RUN python --version && pip --version && google-chrome --version && chromedriver --version

USER runner
WORKDIR /workspace

HEALTHCHECK CMD python -c "exit(0)"

CMD ["pytest", "--headless", "--browser", "chrome"]