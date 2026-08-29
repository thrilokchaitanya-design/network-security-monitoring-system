from app.database import test_database_connection


result = test_database_connection()

print(f"Database connection successful: {result}")