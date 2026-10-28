import csv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

students = {
    1: {"name": "Anu", "course": "Python"},
    2: {"name": "Rahul", "course": "Java"}
}

libraries = {
    1: {"name": "lib1", "location": "East"},
    2: {"name": "lib2", "location": "West"}
}

app = FastAPI()


class Student(BaseModel):
    id: int
    name: str
    course: str


class Library(BaseModel):
    id: int
    name: str
    location: str


def save_students():
    with open("students.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "course"])
        for sid, s in students.items():
            writer.writerow([sid, s["name"], s["course"]])


def save_libraries():
    with open("libraries.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "location"])
        for lid, lib in libraries.items():
            writer.writerow([lid, lib["name"], lib["location"]])


# create the CSV files when the app starts
save_students()
save_libraries()


@app.get("/students")
def get_students():
    return students


@app.get("/libraries")
def get_libraries():
    return libraries


@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]


@app.get("/library/{library_id}")
def get_library(library_id: int):
    if library_id not in libraries:
        raise HTTPException(status_code=404, detail="Library not found")
    return libraries[library_id]


@app.post("/students")
def add_student(student: Student):
    students[student.id] = {"name": student.name, "course": student.course}
    save_students()
    return student


@app.post("/library")
def add_library(library: Library):
    libraries[library.id] = {"name": library.name, "location": library.location}
    save_libraries()
    return library


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = {"name": student.name, "course": student.course}
    save_students()
    return student


@app.put("/library/{library_id}")
def update_library(library_id: int, library: Library):
    if library_id not in libraries:
        raise HTTPException(status_code=404, detail="Library not found")
    libraries[library_id] = {"name": library.name, "location": library.location}
    save_libraries()
    return {"updated": libraries[library_id]}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    removed = students.pop(student_id)
    save_students()
    return {"deleted": removed}


@app.delete("/library/{library_id}")
def delete_library(library_id: int):
    if library_id not in libraries:
        raise HTTPException(status_code=404, detail="Library not found")
    removed = libraries.pop(library_id)
    save_libraries()
    return {"deleted": removed}