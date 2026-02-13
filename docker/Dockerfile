FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Instala dependencias del sistema necesarias
RUN apt-get update -y && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    jq \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instala Google Chrome (versión estable) desde el repositorio oficial
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor | tee /usr/share/keyrings/google-chrome.gpg > /dev/null && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] https://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Instala ChromeDriver compatible con la versión de Chrome instalada
# Se eliminan posibles retornos de carro y se extrae solo el número mayor de versión
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | tr -d '\r') && \
    CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1) && \
    CHROMEDRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_MAJOR_VERSION | tr -d '\r') && \
    wget -q -O /tmp/chromedriver_linux64.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver_linux64.zip /tmp/chromedriver-linux64

# Instala GeckoDriver (para Firefox)
RUN GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r .tag_name | tr -d '\r') && \
    wget -q https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-linux64.tar.gz && \
    tar -xzf geckodriver-${GECKO_VERSION}-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-${GECKO_VERSION}-linux64.tar.gz

# Instala paquetes Python (testing y seguridad)
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

# Crea usuario no root para ejecutar las pruebas
RUN useradd -m -s /bin/bash -u 1000 qauser && \
    mkdir -p /workspace && \
    chown -R qauser:qauser /workspace

USER qauser
WORKDIR /workspace

# Healthcheck simple
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Comando por defecto: ejecutar pytest en modo headless con Chrome
CMD ["pytest", "--headless", "--browser", "chrome"]