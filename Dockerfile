FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD . /app
RUN ./generate-env.sh
RUN pip install pipenv
RUN pipenv install --system --deploy
