FROM python:3.10

# Установить системные зависимости для Chrome и GUI
RUN apt-get update && \
    apt-get install -y wget unzip fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 libdrm2 libgtk-3-0 libnspr4 libnss3 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libxss1 libxtst6 xdg-utils xvfb && \
    rm -rf /var/lib/apt/lists/*

# Скачать и установить Chrome 139.0.7258.66
RUN wget -O /tmp/chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.66/linux64/chrome-linux64.zip && \
    unzip /tmp/chrome-linux64.zip -d /tmp/ && \
    mv /tmp/chrome-linux64 /opt/chrome && \
    ln -s /opt/chrome/chrome /usr/bin/google-chrome && \
    rm /tmp/chrome-linux64.zip

# Скачать и установить ChromeDriver 139.0.7258.66
RUN wget -O /tmp/chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.66/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver-linux64.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver-linux64*

# Проверить версии Chrome и ChromeDriver
RUN google-chrome --version && chromedriver --version

# Создать пользователя для безопасности
RUN useradd -m -s /bin/bash selenium && \
    mkdir -p /app && \
    chown selenium:selenium /app

WORKDIR /app

# Копировать requirements и установить Python-зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копировать все скрипты
COPY . /app
RUN chown -R selenium:selenium /app

USER selenium

# Настроить переменные окружения для Chrome и Python
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome
ENV PATH="/usr/local/bin:$PATH"

ENTRYPOINT ["/bin/bash"]
