<template>
  <v-container>
    <!-- ปุ่ม Export ข้อมูล -->
    <v-btn @click="exportData">Export Data</v-btn>

    <!-- ปุ่ม Upload File -->
    <v-btn @click="triggerFileUpload" >Upload File</v-btn>

    <!-- Input File ที่ซ่อนอยู่ -->
    <input type="file" ref="fileInput" @change="handleFileChange" style="display: none;" />

    <!-- แสดงข้อมูลใน v-data-table -->
    <v-data-table :headers="headers" :items="tableData" class="elevation-1">
      <template v-slot:item="{ item }">
        <tr>
          <td>{{ item.part_no }}</td>
          <td v-for="header in colHeaders" :key="header">{{ item[header] !== undefined ? item[header] : 'NaN' }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      parts: [],  // เก็บข้อมูล JSON ที่ดึงมาจาก backend
      file: null,  // ไฟล์ที่จะอัปโหลด
      colHeaders: ['TG11111', 'TG22222', 'TG33333', 'TG44444', 'TG55555', 'TG66666'],  // ชื่อคอลัมน์ (Part No)
      headers: [
        { text: 'Part No', value: 'part_no' },
        { text: 'TG11111', value: 'TG11111' },
        { text: 'TG22222', value: 'TG22222' },
        { text: 'TG33333', value: 'TG33333' },
        { text: 'TG44444', value: 'TG44444' },
        { text: 'TG55555', value: 'TG55555' },
        { text: 'TG66666', value: 'TG66666' }
      ],  // ใช้สำหรับแสดงหัวตารางใน v-data-table
      tableData: []  // ข้อมูลตารางที่ผ่านการแปลงแล้ว
    };
  },
  methods: {
    triggerFileUpload() {
      // เปิด input file dialog
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      this.file = event.target.files[0];  // เก็บไฟล์ที่ผู้ใช้อัปโหลด
      this.uploadFile();  // อัปโหลดไฟล์เมื่อมีการเลือกไฟล์
    },
    async fetchParts() {
      try {
        const response = await axios.get('http://localhost:8000/parts');  // ดึงข้อมูล JSON จาก backend
        this.parts = response.data;  // เก็บข้อมูลที่ดึงมาในตัวแปร parts
        this.transformData();  // เรียกฟังก์ชันแปลงข้อมูล
      } catch (error) {
        console.error("Error fetching parts:", error);
      }
    },
    async uploadFile(){
      const formData = new FormData();
      formData.append('file', this.file);

      try {
        await axios.post('http://localhost:8000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.fetchParts();  // อัปเดตข้อมูลหลังจากอัปโหลดเสร็จ
      } catch (error) {
        console.error("Error uploading file:", error.response.data);  // แสดงข้อผิดพลาด
      }
    },
    async exportData() {
      try {
        const response = await axios.get('http://localhost:8000/export', {responseType: 'blob'});
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'parts.xlsx');
        document.body.appendChild(link);
        link.click();
      } catch (error) {
        console.error("Error exporting data:", error);
      }
    },
    transformData() {
      // แปลงข้อมูลจาก JSON ให้เป็นรูปแบบตาราง (cross-tab)
      const table = {};

      this.parts.forEach(part => {
        if (!table[part.row_part]) {
          table[part.row_part] = { part_no: part.row_part };
        }
        table[part.row_part][part.col_part] = part.changeover_time;
      });

      // แปลง object ให้เป็น array เพื่อแสดงใน v-data-table
      this.tableData = Object.values(table);
    }
  },
  mounted() {
    this.fetchParts();  // ดึงข้อมูลมาแสดงทันทีเมื่อโหลดหน้าเว็บ
  }
}
</script>

