# main.py
from fastapi import FastAPI
from model.users import users_router
from model.roles import roles_router
from model.laboratories import laboratories_router
from model.courses import courses_router
from model.instructors import instructors_router
from model.schedules import schedules_router
from model.notifications import notifications_router
from model.schedule_history import schedule_history_router
from model.activity_logs import activity_logs_router


app = FastAPI(title="LabClass API", version="1.0")

# Registering routers
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(roles_router, prefix="/api", tags=["Roles"])
app.include_router(laboratories_router, prefix="/api", tags=["Laboratories"])
app.include_router(courses_router, prefix="/api", tags=["Courses"])
app.include_router(instructors_router, prefix="/api", tags=["Instructors"])
app.include_router(schedules_router, prefix="/api", tags=["Schedules"])
app.include_router(notifications_router, prefix="/api", tags=["Notifications"])
app.include_router(schedule_history_router, prefix="/api", tags=["Schedule History"])
app.include_router(activity_logs_router, prefix="/api", tags=["Activity Logs"])
