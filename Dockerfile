FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=pdf_service.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application when the container launches
CMD ["flask", "run"]