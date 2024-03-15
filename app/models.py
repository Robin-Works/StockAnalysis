from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sqlA
import sqlalchemy.orm as sqlOrm
from app import db
from app import login
from flask_login import UserMixin

# Defines user table for the SQLite db
class User(UserMixin, db.Model):
    id: sqlOrm.Mapped[int] = sqlOrm.mapped_column(primary_key=True)
    username: sqlOrm.Mapped[str] = sqlOrm.mapped_column(sqlA.String(64), index=True, unique=True)
    email: sqlOrm.Mapped[str] = sqlOrm.mapped_column(sqlA.String(120), index=True, unique=True)
    passHash: sqlOrm.Mapped[Optional[str]] = sqlOrm.mapped_column(sqlA.String(256)) # Optional allows this to be nullable
    
    posts: sqlOrm.WriteOnlyMapped["Post"] = sqlOrm.relationship(back_populates="author")
    
    def setPassword(self, password):
        self.passHash = generate_password_hash(password)
        
    def checkPassword(self, password):
        return check_password_hash(self.passHash, password)
    
    def __repr__(self):
        return "<User {}>".format(self.username)
    
class Post(db.Model):
    id: sqlOrm.Mapped[int] = sqlOrm.mapped_column(primary_key=True)
    body: sqlOrm.Mapped[str] = sqlOrm.mapped_column(sqlA.String(140))
    timestamp: sqlOrm.Mapped[datetime] = sqlOrm.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    userId: sqlOrm.Mapped[int] = sqlOrm.mapped_column(sqlA.ForeignKey(User.id), index=True)
    
    author: sqlOrm.Mapped[User] = sqlOrm.relationship(back_populates="posts")
    
    def __repr__(self):
        return "<post {}>".format(self.body)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))