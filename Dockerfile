FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Instala dependencias del sistema necesarias para WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango1.0-0 \
    libcairo2 \
    libffi-dev \
    libgdk-pixbuf2.0-0 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libjpeg62-turbo \
    libopenjp2-7 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .

#COPY .env /app/.env

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]