from sqlalchemy import create_engine, text
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ทดสอบการเชื่อมต่อ
try:
    # เปิด session
    session = SessionLocal()

    # รันคำสั่ง SQL พื้นฐานเพื่อทดสอบการเชื่อมต่อ
    session.execute(text("SELECT 1"))
    print("Connection to the database was successful!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # ปิด session
    session.close()
