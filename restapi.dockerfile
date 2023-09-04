FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install "pymongo[srv]" -r requirements.txt

EXPOSE 8080

ENV MONGO_URI="mongodb+srv://varshney:Sj55888@cluster0.jqzobx2.mongodb.net/JWT_AUTH?retryWrites=true&w=majority"

CMD ["python", "app.py"]
