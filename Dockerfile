FROM python:3.10

WORKDIR /scrapyApp

COPY . /scrapyApp
RUN pip install --trusted-host pypi.python.org -r requirements.txt


RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN dpkg -i google-chrome-stable_current_amd64.deb; exit 0

RUN apt-get update

RUN apt --fix-broken install -y

RUN echo "Chrome: " && google-chrome --version

ENV PATH="/scrapyApp:${PATH}"

CMD ["scrapy", "crawl", "TheWeatherChannel"]

