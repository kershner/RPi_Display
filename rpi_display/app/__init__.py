from flask import Flask
app = Flask(__name__)  # Initialize Flask Object
app.secret_key = 'Pi Display Project'
from app import routes