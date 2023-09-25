FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["pytest", "-v", "-s", "--remote-url", "http://192.168.1.136:4444/wd/hub", "-n", "auto", "--alluredir", "allure-report"]