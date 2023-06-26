from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from base import Base
from Students.StudentService import students_route
from Providers.ProviderService import providers_route
from ProviderCategory.ProviderCategoriesService import provider_categories_route
from Users.UserService import users_route
from Ratings.RatingsService import ratings_route
from Requests.RequestServices import request_services_route
from flask_cors import CORS
from flask_mail import Mail


app = Flask(__name__)
app.secret_key = '0hyvgta56h'

#instantiating the database and sqlalchemy
engine = create_engine('postgresql://postgres:extreme1001@campserve-database.cwt8zh4gaxtg.us-east-1.rds.amazonaws.com/campserve')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

#App blueprints
app.register_blueprint(students_route)
app.register_blueprint(providers_route)
app.register_blueprint(provider_categories_route)
app.register_blueprint(users_route)
app.register_blueprint(ratings_route)
app.register_blueprint(request_services_route)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'isinesam@gmail.com'
app.config['MAIL_PASSWORD'] = 'lvrmqxfoqfbgaieg'
app.config['MAIL_DEFAULT_SENDER'] = 'isinesam@gmail.com'

mail = Mail(app)

#Database connection
try:
    engine.connect()
    Base.metadata.create_all(engine)
    session.commit()
    print('database created')
except Exception as e:
    print('connection failed: %s'%(e))
    session.rollback()
finally:
    session.close()


if __name__ == '__main__':
    CORS(app)
    app.run(host= '0.0.0.0', port= 5000, debug=True)