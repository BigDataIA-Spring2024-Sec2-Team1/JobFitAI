FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./ /app

EXPOSE 8000

CMD ["uvicorn", "resume_analyser:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
