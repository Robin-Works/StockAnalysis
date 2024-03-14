from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sqlA
import sqlalchemy.orm as sqlOrm
from app import db

# Defines user table for the SQLite db
class User(db.Model):
    id: sqlOrm.Mapped[int] = sqlOrm.mapped_column(primary_key=True)
    username: sqlOrm.Mapped[str] = sqlOrm.mapped_column(sqlA.String(64), index=True, unique=True)
    email: sqlOrm.Mapped[str] = sqlOrm.mapped_column(sqlA.String(120), index=True, unique=True)
    passHash: sqlOrm.Mapped[Optional[str]] = sqlOrm.mapped_column(sqlA.String(256)) # Optional allows this to be nullable
    
    posts: sqlOrm.WriteOnlyMapped["Post"] = sqlOrm.relationship(back_populates="author")
    
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