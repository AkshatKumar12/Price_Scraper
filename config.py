import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///products.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TTL = 600  # 10 minutes
    RATE_LIMIT = 10  # requests per minute
