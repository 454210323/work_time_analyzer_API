import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/work"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    UPLOAD_FOLDER = "resource/upload_file"
    GENERATED_FOLDER = "resource/generated_file"


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
