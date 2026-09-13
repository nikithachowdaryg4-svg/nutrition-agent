import sqlite3


DATABASE_NAME = "nutriai.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # User profile table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            weight REAL,
            height REAL,
            activity_level TEXT,
            goal TEXT,
            diet_type TEXT,
            health_condition TEXT,
            allergies TEXT
        )
    """)

    # Meal log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT,
            calories REAL,
            protein REAL,
            carbohydrates REAL,
            fat REAL,
            fiber REAL,
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_profile(
    name,
    age,
    gender,
    weight,
    height,
    activity_level,
    goal,
    diet_type,
    health_condition,
    allergies
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO user_profile
        (name, age, gender, weight, height, activity_level,
         goal, diet_type, health_condition, allergies)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        gender,
        weight,
        height,
        activity_level,
        goal,
        diet_type,
        health_condition,
        allergies
    ))

    connection.commit()
    connection.close()


def save_meal(
    food_name,
    calories,
    protein,
    carbohydrates,
    fat,
    fiber
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO meal_logs
        (food_name, calories, protein, carbohydrates, fat, fiber)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        food_name,
        calories,
        protein,
        carbohydrates,
        fat,
        fiber
    ))

    connection.commit()
    connection.close()


def get_meal_logs():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM meal_logs
        ORDER BY logged_at DESC
    """)

    logs = cursor.fetchall()

    connection.close()

    return logs