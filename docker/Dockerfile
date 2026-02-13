# Imagen base: Debian 12 (bookworm) con soporte de seguridad a largo plazo
FROM python:3.10-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Instalación consolidada: herramientas temporales, Chrome, ChromeDriver y limpieza profunda
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    jq \
    gpg \
    ca-certificates \
    && \
    # Agregar repositorio de Google Chrome (método moderno sin apt-key)
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor | tee /usr/share/keyrings/google-chrome.gpg > /dev/null && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] https://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    # Actualizar lista de paquetes y aplicar todas las actualizaciones de seguridad disponibles
    apt-get update -y && apt-get upgrade -y && apt-get install -y --no-install-recommends google-chrome-stable && \
    # Instalar ChromeDriver compatible con la versión de Chrome instalada
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | tr -d '\r') && \
    CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1) && \
    CHROMEDRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_MAJOR_VERSION | tr -d '\r') && \
    wget -q -O /tmp/chromedriver_linux64.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver_linux64.zip /tmp/chromedriver-linux64 && \
    # Eliminar herramientas temporales y limpiar caché de apt (no quedarán en la imagen final)
    apt-get purge -y --auto-remove wget curl unzip jq gpg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalación de paquetes Python con versiones parcheadas
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

# Crear usuario no root para ejecutar las pruebas
RUN useradd -m -s /bin/bash -u 1000 qauser && \
    mkdir -p /workspace && \
    chown -R qauser:qauser /workspace

USER qauser
WORKDIR /workspace

# Healthcheck simple
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Comando por defecto (solo Chrome, sin GeckoDriver para reducir superficie)
CMD ["pytest", "--headless", "--browser", "chrome"]