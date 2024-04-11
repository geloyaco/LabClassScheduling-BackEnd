# main.py
from fastapi import FastAPI
from model.instructors import InstructorsRouter
from model.admin import AdminRouter
from model.bookingrequest import BookingRequestRouter
from model.semschedule import SemScheduleRouter
from model.computerlab import ComputerLabRouter  

app = FastAPI()

# Include CRUD routes from modules
app.include_router(InstructorsRouter, prefix="/api")
app.include_router(AdminRouter, prefix="/api")
app.include_router(BookingRequestRouter, prefix="/api")
app.include_router(SemScheduleRouter, prefix="/api")
app.include_router(ComputerLabRouter, prefix="/api")  
