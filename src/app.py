"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    # Intellettuali
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice public speaking and argumentation skills in competitions",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Math Olympiad": {
        "description": "Prepare for and participate in math competitions",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": []
    },
    # Sportive
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Train and compete in school soccer tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": []
    },
    "Basketball Club": {
        "description": "Practice basketball and play friendly matches",
        "schedule": "Fridays, 5:00 PM - 6:30 PM",
        "max_participants": 15,
        "participants": []
    },
    # Artistiche
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    },
    "Drama Society": {
        "description": "Act, direct, and produce school plays and performances",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": []
    },
    "Music Band": {
        "description": "Play instruments and perform in the school band",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
