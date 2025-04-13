# Use an official Python runtime as a parent image
FROM nikolaik/python-nodejs:python3.13-nodejs18-slim
# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    lsof \ 
    apt-transport-https \
    ca-certificates \
    x11-utils xdg-utils xvfb \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Add the Google Chrome repository
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# USER gitpod

# Add the Chrome as a path variable
ENV CHROME_BIN=/usr/bin/google-chrome

ENV PYTHONUNBUFFERED=1

RUN mkdir app
WORKDIR /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY run.py .
COPY /backend /app/backend
COPY /src /app/src
COPY /frontend /app/frontend
RUN python run.py install



CMD ["python", "run.py"]
