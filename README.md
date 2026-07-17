# Workout Tracker API
## Description
A Flask REST API for managing workouts and exercises.  
Trainers can create workouts, create exercises, and assign exercises to workouts with sets, reps, and duration tracking.
Built with:
- Flask
- SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite

## Setup
Install dependencies:
```bash
pipenv install
pipenv shell
```
Create database:
```bash
flask db init
flask db migrate -m "create tables"
flask db upgrade
```
Seed data:
```bash
python -m server.seed
```
Run server:
```bash
python -m server.app
```
API runs at:
```
http://127.0.0.1:5555
```

## Endpoints

### Exercises
```
GET    /exercises
GET    /exercises/<id>
POST   /exercises
DELETE /exercises/<id>
```
### Workouts
```
GET    /workouts
GET    /workouts/<id>
POST   /workouts
DELETE /workouts/<id>
```
### Workout Exercises
```
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
```

## Models
**Exercise**
- id
- name
- category
- equipment_needed

**Workout**
- id
- date
- duration_minutes
- notes

**WorkoutExercise**
- workout_id
- exercise_id
- reps
- sets
- duration_seconds

## Testing
Run:
```bash
pytest
```