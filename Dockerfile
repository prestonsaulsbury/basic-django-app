FROM python:3.11
ENV PYTHONUNBUFFERED 1

RUN mkdir /basic-django-app
COPY . /basic-django-app

RUN apt-get update && apt-get install -y zsh
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

WORKDIR /basic-django-app
RUN pip install -r ./main/mysite/requirements.txt
