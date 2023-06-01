from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from base import Base
from Students.StudentService import students_route
from Providers.ProviderService import providers_route
from ProviderCategory.ProviderCategoriesService import provider_categories_route
from Users.UserService import users_route
from flask_cors import CORS


app = Flask(__name__)

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
    app.run(debug=True)