# Start with python 3.10 image
FROM python:3.10-slim

# Environment vars
ARG PROJECT_ID=local
ENV PROJECT_ID=$PROJECT_ID

# Copy the current directory into /app on the image
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

# Entry point command
CMD streamlit run main.py --server.port 80 --browser.serverAddress 0.0.0.0 --server.enableCORS False --server.enableXsrfProtection False