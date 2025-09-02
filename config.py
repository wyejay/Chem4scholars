
import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
