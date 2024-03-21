import re
from mySQLDatabase import *


def sanitize(myInput):
    # Sanitize the input to prevent SQL injection
    # Whitelist approach: Allow only alphanumeric characters, underscore, and space
    sanitized_input = re.sub(r'[^a-zA-Z0-9_ ]', '', myInput)

    # Check if any harmful keywords were removed
    removed_keywords = re.findall(r'\b(?:SELECT|DROP|DELETE)\b', myInput)
    if removed_keywords:
        removed_keywords_str = ', '.join(removed_keywords)
        print(f"Removed harmful keywords: {removed_keywords_str}")

    return sanitized_input


def validate_name(name):
    # Allow alphanumeric characters, 3-15 characters long
    pattern = r'^[a-zA-Z0-9_]{3,15}$'
    return re.match(pattern, name)


def validate_username(username):
    # allowing alphanumeric characters and underscore, 4-20 characters long
    pattern = r'^[a-zA-Z0-9_]{4,20}$'
    return re.match(pattern, username)


def validate_password(password):
    # requiring at least 8 characters with one lowercase, one uppercase, one digit
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,20}$'
    return re.match(pattern, password)


def username_exists(username):
    """Check if the username already exists in the database."""
    query = "SELECT * FROM userdata WHERE Username = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result is not None
