from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Report(BaseModel):
    date: str
    new_applications: int
    target: int
    percentage: int
    amount: int
    outgoing_calls: int
    new_meetings: int
    meeting_amount: int
    office_visits: int
    contract_conclusion: int
    contract_amount: int
    plan_for_tomorrow: Optional[str] = None

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
    plan_for_tomorrow: Optional[str] = Form(None)
):
    report = Report(
        date=date,
        new_applications=new_applications,
        target=target,
        percentage=percentage,
        amount=amount,
        outgoing_calls=outgoing_calls,
        new_meetings=new_meetings,
        meeting_amount=meeting_amount,
        office_visits=office_visits,
        contract_conclusion=contract_conclusion,
        contract_amount=contract_amount,
        plan_for_tomorrow=plan_for_tomorrow
    )
    # Здесь вы можете сохранить отчет в базу данных или выполнить другие действия
    return {"message": "Отчет успешно отправлен", "report": report.dict()}

# Создайте папку templates и внутри нее файл form.html
# В form.html добавьте ваш HTML код
