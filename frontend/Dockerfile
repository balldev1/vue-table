# ใช้ Node.js เป็น base image
FROM node:16-alpine

# ตั้งค่า working directory เป็น /frontend
WORKDIR /frontend

# คัดลอกไฟล์ package.json และ package-lock.json ไปยัง container
COPY package*.json ./

# ติดตั้ง dependencies
RUN npm install

# คัดลอกโค้ดทั้งหมดไปยัง container
COPY .. .

# เปิดพอร์ต 8080 สำหรับ frontend
EXPOSE 8080

# รัน frontend ด้วย npm run serve
CMD ["npm", "run", "serve"]