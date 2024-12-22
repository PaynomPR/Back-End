from fastapi import FastAPI
import os
import uvicorn
from dotenv import load_dotenv

# from database.config import init_db
from sqlalchemy import event
from models.periods import Period
from models.time import Time
from routers.users import user_router
from routers.roles import role_router
from routers.auth import auth_router
from routers.code import code_router
from routers.fixed_taxes import fixed_taxes_router
# from routers.mail import email_router

from routers.employers import employers_router
from routers.accountant import accountant_router
from routers.companies import companies_router
from routers.taxes import taxes_router
from routers.time import time_router
from routers.outemployers import outemployers_router
from routers.time_outemployer import outtime_router
from routers.reports import report_router
from routers.period import period_routes


from models.users import User, Role, Code, UserCode
from models.taxes import FixedTaxes
from models.companies import Companies
from models.employers import Employers


from fastapi.middleware.cors import CORSMiddleware
from database.config import init_db
from database.seed.user import initialize_table
from database.seed.period import initialize_periods

load_dotenv()

URL = os.environ.get("URL")
PORT = os.environ.get("PORT")


# I set up this event before table creation
event.listen(Role.__table__, "after_create", initialize_table)
event.listen(Code.__table__, "after_create", initialize_table)
event.listen(User.__table__, "after_create", initialize_table)
event.listen(FixedTaxes.__table__, "after_create", initialize_table)

event.listen(UserCode.__table__, "after_create", initialize_table)


app = FastAPI()
app.title = "Paynompr - be"


app.add_middleware(
    CORSMiddleware,
    allow_origins=[URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
initialize_periods()

app.include_router(auth_router, tags=["auth"], prefix="/api/auth")
app.include_router(user_router, tags=["users"], prefix="/api/users")
app.include_router(role_router, tags=["roles"], prefix="/api/roles")
app.include_router(code_router, tags=["codes"], prefix="/api/codes")
app.include_router(accountant_router, tags=["accountant"], prefix="/api/accountant")
app.include_router(companies_router, tags=["companies"], prefix="/api/companies")
app.include_router(employers_router, tags=["employers"], prefix="/api/employers")
app.include_router(time_router, tags=["time"], prefix="/api/time")
app.include_router(taxes_router, tags=["taxes"], prefix="/api/taxes")
app.include_router(fixed_taxes_router, tags=["fixed_taxes"], prefix="/api/fixed-taxes")
app.include_router(
    outemployers_router, tags=["outemployers"], prefix="/api/outemployers"
)
app.include_router(outtime_router, tags=["outtime_router"], prefix="/api/outtime")
app.include_router(report_router, tags=["report_router"], prefix="/api/reports")
app.include_router(period_routes, tags=["period_router"], prefix="/api/period")

if __name__ == "__main__":
    uvicorn.run("main:app", port=int(PORT), host="0.0.0.0", reload=True)
