from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=100,
            error="Exercise name must be between 2 and 100 characters."
        )
    )
    category = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["Cardio", "Strength", "Flexibility", "Balance"],
            error="Category must be Cardio, Strength, Flexibility, or Balance."
        )
    )
    equipment_needed = fields.Bool(required=True)
    workouts = fields.List(
        fields.Nested(
            lambda: WorkoutSummarySchema()
        ),
        dump_only=True
    )

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int()
    exercise_id = fields.Int()
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

class WorkoutSummarySchema(Schema):
    id = fields.Int()
    date = fields.Date()
    duration_minutes = fields.Int()

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(
            min=1,
            max=600,
            error="Workout duration must be between 1 and 600 minutes."
        )
    )
    notes = fields.Str(
        validate=validate.Length(
            max=500
        )
    )
    workout_exercises = fields.List(
        fields.Nested(
            WorkoutExerciseSchema
        ),
        dump_only=True
    )

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()