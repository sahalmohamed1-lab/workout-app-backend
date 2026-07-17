import os
import unittest
from datetime import date
from server.app import app
from server.models import db, Exercise, Workout

TEST_DB = "test.db"

class WorkoutApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{TEST_DB}"
        cls.client = app.test_client()

    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            exercise = Exercise(
                name="Burpee",
                category="Cardio",
                equipment_needed=True
            )
            workout = Workout(
                date=date(2026, 7, 14),
                duration_minutes=40,
                notes="Test workout"
            )
            db.session.add_all([exercise, workout])
            db.session.commit()
            self.exercise_id = exercise.id
            self.workout_id = workout.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_add_exercise_to_workout_accepts_url_ids(self):
        response = self.client.post(
            f"/workouts/{self.workout_id}/exercises/{self.exercise_id}/workout_exercises",
            json={
                "reps": 10,
                "sets": 2,
                "duration_seconds": 300
            }
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["workout_id"], self.workout_id)
        self.assertEqual(data["exercise_id"], self.exercise_id)
        self.assertEqual(data["reps"], 10)
        self.assertEqual(data["sets"], 2)
        self.assertEqual(data["duration_seconds"], 300)

if __name__ == "__main__":
    unittest.main()