from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '34f009c096b31ad747ae9af6bd3dd1a7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\AIRBLUE SERVICES\\Desktop\\dev\\flask\\frappe\\assignment\\instance\\site.db'
db = SQLAlchemy(app)

from library import routes