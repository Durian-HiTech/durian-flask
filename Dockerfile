FROM python:3.7
WORKDIR /app
COPY . /app
RUN apt-get update &&\
    apt-get install -y libsndfile1
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["gunicorn", "main:app", "-b", ":8080", "--timeout", "300"]