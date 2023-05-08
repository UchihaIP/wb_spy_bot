FROM selenium/standalone-chrome:latest

USER root

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --upgrade
COPY . .
CMD ["python", "main.py"]