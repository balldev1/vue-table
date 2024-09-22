# ใช้ Python 3.9 เป็น base image
FROM python:3.9-slim

# ตั้งค่า working directory เป็น /code
WORKDIR /code

# คัดลอก requirements.txt ไปยัง container
COPY ./requirements.txt /code/requirements.txt

# ติดตั้ง dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# คัดลอกโค้ดทั้งหมดไปยัง container
COPY ./app /code/app

# เปิดพอร์ต 8000
EXPOSE 8000

# รันแอปด้วย Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
