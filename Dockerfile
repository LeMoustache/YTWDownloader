FROM tiangolo/uvicorn-gunicorn:python3.9

COPY * /app/
COPY html/ /app/html
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
