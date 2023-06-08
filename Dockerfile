FROM python:3
ENV PYTHONUNBUFFERED=1
COPY . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
