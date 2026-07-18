from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
import os
from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import ( exercise_schema, exercises_schema, workout_schema, workouts_schema, workout_exercise_schema)

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return jsonify({
        "message": "Workout API is running successfully!"
    }), 200

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Resource not found"
    }), 404

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({
            "error": "Exercise not found"
        }), 404
    return jsonify(exercise_schema.dump(exercise)), 200

@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(
            request.get_json()
        )
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
        return jsonify(
            exercise_schema.dump(exercise)
        ), 201
    except ValueError as error:
        db.session.rollback()
        return jsonify({
            "error": str(error)
        }), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "Exercise name already exists"
        }), 400

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({
            "error": "Exercise not found"
        }), 404
    db.session.delete(exercise)
    db.session.commit()
    return "", 204

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({
            "error": "Workout not found"
        }), 404
    return jsonify(workout_schema.dump(workout)), 200

@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(
            request.get_json()
        )
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
        return jsonify(
            workout_schema.dump(workout)
        ), 201
    except ValueError as error:
        db.session.rollback()
        return jsonify({
            "error": str(error)
        }), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "Unable to create workout"
        }), 400

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({
            "error": "Workout not found"
        }), 404
    db.session.delete(workout)
    db.session.commit()
    return "", 204

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return jsonify({
            "error": "Workout or Exercise not found"
        }), 404
    try:
        data = workout_exercise_schema.load(
            request.get_json() or {}
        )
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds")
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return jsonify(
            workout_exercise_schema.dump(workout_exercise)
        ), 201
    except ValueError as error:
        db.session.rollback()
        return jsonify({
            "error": str(error)
        }), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "Unable to add exercise to workout"
        }), 400

if __name__ == "__main__":
    app.run(
        port=5555,
        debug=True
    )