from sqlmodel import create_engine, SQLModel

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Jpassword@localhost:3306/requiem"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

from app.models.post_model import PostBase
from app.models.user_model import UserBase
from app.models.view_model import ViewBase

def create_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
