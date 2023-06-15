from app.schemas.user_schema import  UserRead

users = {
    1: UserRead(id=1, first_name="John", last_name="Doe", email="john.doe@example.com", username="johndoe", password="password123", facebook_account="john.doe", instagram_accoutn="john.doe"),
    2: UserRead(id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com", username="janedoe", password="password123", facebook_account="jane.doe", instagram_accoutn="jane.doe"),
}