from datetime import date
from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Resetting database...")
    db.drop_all()
    db.create_all()
    print("Creating exercises...")
    push_up = Exercise(
        name="Push Up",
        category="Strength",
        equipment_needed=False
    )
    treadmill = Exercise(
        name="Treadmill Sprint",
        category="Cardio",
        equipment_needed=True
    )
    yoga = Exercise(
        name="Yoga Stretch",
        category="Flexibility",
        equipment_needed=False
    )
    plank = Exercise(
        name="Plank",
        category="Strength",
        equipment_needed=False
    )
    squats = Exercise(
        name="Bodyweight Squat",
        category="Strength",
        equipment_needed=False
    )
    db.session.add_all([
        push_up,
        treadmill,
        yoga,
        plank,
        squats
    ])
    db.session.commit()
    print("Creating workouts...")
    workout1 = Workout(
        date=date(2023, 10, 15),
        duration_minutes=45,
        notes="Upper body workout."
    )
    workout2 = Workout(
        date=date(2023, 10, 16),
        duration_minutes=30,
        notes="Morning cardio session."
    )
    workout3 = Workout(
        date=date(2023, 10, 17),
        duration_minutes=60,
        notes="Full body workout."
    )
    db.session.add_all([
        workout1,
        workout2,
        workout3
    ])
    db.session.commit()
    print("Creating workout exercises...")
    workout_exercises = [
        WorkoutExercise(
            workout=workout1,
            exercise=push_up,
            sets=3,
            reps=15
        ),
        WorkoutExercise(
            workout=workout1,
            exercise=plank,
            duration_seconds=90
        ),

        WorkoutExercise(
            workout=workout2,
            exercise=treadmill,
            duration_seconds=900
        ),
        WorkoutExercise(
            workout=workout3,
            exercise=squats,
            sets=4,
            reps=12
        ),
        WorkoutExercise(
            workout=workout3,
            exercise=yoga,
            duration_seconds=1200
        )
    ]
    db.session.add_all(workout_exercises)
    db.session.commit()
    print("\nDatabase seeded successfully!")