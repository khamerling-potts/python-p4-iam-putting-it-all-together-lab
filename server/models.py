from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db, bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-recipes.user", "-_password_hash")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship(
        "Recipe", back_populates="user", cascade="all, delete-orphan"
    )

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    # @validates("username")
    # def validate_username(self, key, username):
    #     if username == "":
    #         raise ValueError("username must not be empty")
    #     if db.session.query(User.id).filter_by(username=username).first():
    #         raise ValueError("username must be unique")
    #     return username

    def __repr__(self):
        return f"<User {self.username}>"


class Recipe(db.Model, SerializerMixin):
    __tablename__ = "recipes"
    __table_args__ = (db.CheckConstraint("length(instructions) >= 50"),)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="recipes")

    # @validates("title")
    # def validate_title(self, key, title):
    #     if title == "":
    #         raise ValueError("Title cannot be empty")
    #     return title

    # @validates("instructions")
    # def validate_instructions(self, key, instructions):
    #     if instructions == "":
    #         raise ValueError("Instructions cannot be empty")
    #     if len(instructions) < 50:
    #         raise ValueError("Instruction must be at least 50 characters long")
    #     return instructions

    def __repr__(self):
        return f"<Recipe {self.id}: {self.title}>"
