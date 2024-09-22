from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app import models,schemas
from app.database import SessionLocal, engine
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตทุก method เช่น GET, POST
    allow_headers=["*"],  # อนุญาตทุก headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/parts", response_model=schemas.Part)
def create_part(part: schemas.PartCreate, db: Session = Depends(get_db)):
    db_part = models.Part(**part.dict())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

@app.get("/parts", response_model=list[schemas.Part])
def read_parts(db: Session = Depends(get_db)):
    parts = db.query(models.Part).all()
    return parts

@app.get("/parts/{part_id}", response_model=schemas.Part)
def read_part(part_id: int, db: Session = Depends(get_db)):
    part = db.query(models.Part).filter(models.Part.id == part_id).first()
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return part

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # ตรวจสอบว่าเป็นไฟล์ Excel หรือไม่
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")

        # อ่านข้อมูลไฟล์จาก UploadFile และแปลงเป็น BytesIO
        contents = await file.read()  # อ่านไฟล์
        excel_data = BytesIO(contents)  # แปลงเป็น BytesIO

        # อ่านไฟล์ Excel ด้วย pandas
        df = pd.read_excel(excel_data)

        # ตรวจสอบว่ามีคอลัมน์ 'Part No' อยู่ในไฟล์หรือไม่
        if 'Part No' not in df.columns:
            raise HTTPException(status_code=400, detail="Missing 'Part No' column in the Excel file.")

        # ลูปผ่านแต่ละแถวใน Excel และเก็บข้อมูลในฐานข้อมูล
        for index, row in df.iterrows():
            row_part = row['Part No']
            for col in df.columns[1:]:  # ข้าม 'Part No' และเข้าถึงคอลัมน์ที่เกี่ยวข้อง
                if pd.notna(row[col]):  # ถ้าข้อมูลไม่ใช่ NaN
                    col_part = col
                    changeover_time = row[col]

                    # ตรวจสอบว่าข้อมูล row_part และ col_part มีอยู่ในฐานข้อมูลหรือไม่
                    existing_part = db.query(models.Part).filter_by(row_part=row_part, col_part=col_part).first()

                    if existing_part:
                        # ถ้ามีข้อมูล row_part และ col_part อยู่แล้ว ให้อัปเดตค่า changeover_time
                        existing_part.changeover_time = changeover_time
                    else:
                        # ถ้าไม่มีข้อมูล ให้เพิ่มเข้าไปใหม่
                        new_part = models.Part(row_part=row_part, col_part=col_part, changeover_time=changeover_time)
                        db.add(new_part)

        db.commit()
        return {"message": "Upload Successful"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


@app.get("/export")
def export_parts(db: Session = Depends(get_db)):
    try:
        parts = db.query(models.Part).all()

        # รวบรวมข้อมูลทั้งหมด
        part_names = list(set([part.row_part for part in parts] + [part.col_part for part in parts]))
        part_names.sort()

        # สร้างตารางข้อมูลสำหรับการ export
        data = { "Part No": part_names }

        for part_name in part_names:
            data[part_name] = []
            for row_part in part_names:
                part = db.query(models.Part).filter_by(row_part=row_part, col_part=part_name).first()
                if part:
                    data[part_name].append(part.changeover_time)
                else:
                    data[part_name].append('NaN')

        # แปลงข้อมูลเป็น DataFrame
        df = pd.DataFrame(data)

        # สร้างไฟล์ Excel
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=parts_export.xlsx"})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error exporting data: {str(e)}")


