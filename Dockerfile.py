FROM python:3-alpine
WORKDIR /root/
COPY /health/* ./
RUN pip install -r requirements.txt 
EXPOSE 8080/tcp
CMD ["python", "healthchecker.py"]  