from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)

class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError(
                "Exercise name must be at least 2 characters long."
            )
        return value.strip().title()

    @validates("category")
    def validate_category(self, key, value):
        if not value:
            raise ValueError("Category is required.")
        return value.strip().title()

class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    __table_args__ = (
        db.CheckConstraint(
            "duration_minutes > 0",
            name="check_positive_duration"
        ),
    )
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True
    )
    @validates("notes")
    def validate_notes(self, key, value):
        if value and len(value) > 500:
            raise ValueError(
                "Notes cannot exceed 500 characters."
            )
        return value

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError(
                "Workout duration must be greater than zero."
            )
        return value

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )
    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value < 1:
            raise ValueError(
                "Sets must be at least 1."
            )
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value < 0:
            raise ValueError(
                "Reps cannot be negative."
            )
        return value

    @validates("duration_seconds")
    def validate_duration(self, key, value):
        if value is not None and value < 0:
            raise ValueError(
                "Duration cannot be negative."
            )
        return value