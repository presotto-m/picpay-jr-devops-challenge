FROM python:3.9
WORKDIR /app
ADD . /app
EXPOSE 8081
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
