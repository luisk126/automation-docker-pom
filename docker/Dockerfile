# =========================
# Stage 1: Base runtime
# =========================
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# -------------------------
# System dependencies
# -------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    gnupg \
    ca-certificates \
    unzip \
    git \
    jq \
    firefox-esr \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libgbm1 \
    libdrm2 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Install Chrome
# -------------------------
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Install ChromeDriver
# -------------------------


# -------------------------
# Install GeckoDriver
# -------------------------
RUN GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r .tag_name) && \
    wget -q https://github.com/mozilla/geckodriver/releases/download/${GECKO_VERSION}/geckodriver-${GECKO_VERSION}-linux64.tar.gz && \
    tar -xzf geckodriver-${GECKO_VERSION}-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-${GECKO_VERSION}-linux64.tar.gz

# -------------------------
# Python test stack
# -------------------------
RUN pip install --no-cache-dir \
    selenium \
    pytest \
    pytest-cov \
    requests \
    allure-pytest \
    flake8

# -------------------------
# Non-root user
# -------------------------
RUN useradd -m -s /bin/bash qauser
USER qauser
WORKDIR /workspace

CMD ["bash"]
