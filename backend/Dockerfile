FROM python:3.8
WORKDIR .
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# run 
COPY . .
CMD ["python", "main.py"]