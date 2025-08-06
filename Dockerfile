FROM python:3.10

# Установить системные зависимости для Chrome и GUI
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg2 \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Установить Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Проверить версию Chrome
RUN google-chrome --version

# Создать пользователя для безопасности
RUN useradd -m -s /bin/bash selenium && \
    mkdir -p /app && \
    chown selenium:selenium /app

# Установить рабочую директорию
WORKDIR /app

# Копировать requirements и установить Python-зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копировать все скрипты
COPY . /app
RUN chown -R selenium:selenium /app

# Переключиться на пользователя selenium
USER selenium

# Настроить переменные окружения для Chrome
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome

# По умолчанию запускать bash
ENTRYPOINT ["/bin/bash"]