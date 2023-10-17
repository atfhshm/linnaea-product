__all__ = ["invalid_register_object"]

invalid_register_object = {
    "first_name": ["This field is required."],
    "last_name": ["This field is required."],
    "email": ["A user with that email already exists.", "Enter a valid email address."],
    "username": ["A user with that username already exists."],
    "phone_number": ["A user with that email already exists."],
    "password": [
        "Passwords missmatch.",
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric.",
    ],
}

invalid_password_object = {
    "password": ["Invalid password."],
    "new_password": [
        "Passwords missmatch.",
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric.",
    ],
}
