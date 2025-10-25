# Dockerfile
FROM python:3.11-slim

# set workdir
WORKDIR /je_an_ararat

# copy

RUN py -m  pip install --no-cache-dir -r /je_an_ararat/requirements.txt

COPY . /je_an_ararat/

# ensure uvicorn can serve static files

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", ]
