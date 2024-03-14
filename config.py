import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask and extensions use this as cryptographic key for signatures and tokens
    # Real secret key set in prod, plain text is fine for test
    SECRET_KEY = os.environ.get("SECRET_KEY") or "really-super-secret-key-shh"
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")