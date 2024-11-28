from fastapi import FastAPI, Form, Request, File, UploadFile, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import databases
import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Boolean,
    Text,
    DateTime,
    SmallInteger,
    String,
    ForeignKey,
    TIMESTAMP,
    Date
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

templates = Jinja2Templates(directory="templates")

DATABASE_URL = "postgresql://db_admin:Hrat6ZyQJORU@37.143.10.252/kmk_mebel"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

class Reports(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    report_date = Column(Date)
    user_id = Column(Integer)
    claims_new = Column(Integer)
    target = Column(Integer)
    calc = Column(Integer)
    calc_amount = Column(Numeric)
    out_calls = Column(Integer)
    plan_count = Column(Integer)
    plan_amount = Column(Numeric)
    come_office = Column(Integer)
    arg_count = Column(Integer)
    arg_amount = Column(Numeric)
    plan_tomorrow = Column(Text)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg = Column(Text)
    full_name = Column(Text)
    counter = Column(Integer)
    send_button = Column(Boolean)
    chat_id = Column(Integer)

class Payment(BaseModel):
    date: str
    contract_number: int
    accounting_type: str
    payment_type: str
    comment: Optional[str] = None

@app.get("/payment", response_class=HTMLResponse)
async def read_payment_form(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})

@app.post("/send_payment")
async def submit_payment(
    date: str = Form(...),
    contract_number: int = Form(...),
    accounting_type: str = Form(...),
    payment_type: str = Form(...),
    comment: Optional[str] = Form(None),
    check_photo: UploadFile = File(...)
):
    payment = Payment(
        date=date,
        contract_number=contract_number,
        accounting_type=accounting_type,
        payment_type=payment_type,
        comment=comment
    )
    # Здесь вы можете сохранить чек и данные в базу данных или выполнить другие действия
    # Например, сохранение файла на сервере
    file_location = f"uploads/{check_photo.filename}"
    with open(file_location, "wb") as file:
        file.write(await check_photo.read())

    return {"message": "Чек успешно отправлен", "payment": payment.dict(), "check_photo": check_photo.filename}

@app.get("/report", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})

@app.post("/send_report")
async def submit_report(
    date: str = Form(...),
    new_applications: int = Form(...),
    target: int = Form(...),
    percentage: int = Form(...),
    amount: int = Form(...),
    outgoing_calls: int = Form(...),
    new_meetings: int = Form(...),
    meeting_amount: int = Form(...),
    office_visits: int = Form(...),
    contract_conclusion: int = Form(...),
    contract_amount: int = Form(...),
    plan_for_tomorrow: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    new_report = Reports(
        report_date=date,
        user_id=1,  # нужно брать из бота
        claims_new=new_applications,
        target=target,
        calc=percentage,
        calc_amount=amount,
        out_calls=outgoing_calls,
        plan_count=new_meetings,
        plan_amount=meeting_amount,
        come_office=office_visits,
        arg_count=contract_conclusion,
        arg_amount=contract_amount,
        plan_tomorrow=plan_for_tomorrow,
    )
    db.add(new_report)
    db.commit()

    # Здесь вы можете сохранить отчет в базу данных или выполнить другие действия
    return {"message": "Отчет успешно отправлен"}

# Создайте папку templates и внутри нее файл form.html
# В form.html добавьте ваш HTML код
