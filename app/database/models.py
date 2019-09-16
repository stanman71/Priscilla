from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


from app        import app
from app.common import COMMON, STATUS, DATATYPE

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id       = db.Column(db.Integer,     primary_key=True)
    username = db.Column(db.String(64),  unique = True)
    email    = db.Column(db.String(120), unique = True)
    role     = db.Column(db.String(50))   
    password = db.Column(db.String(100))


""" ################################ """
""" ################################ """
""" create tables and default values """
""" ################################ """
""" ################################ """


# create all database tables
db.create_all()

# create default user
if User.query.filter_by(username='admin').first() is None:
    user = User(
        username  = "admin",
        email     = "member@example.com",
        role      = "administrator",
        password  = "sha256$OeDkVenT$bc8d974603b713097e69fc3efa1132991bfb425c59ec00f207e4b009b91f4339",     
    )
    db.session.add(user)
    db.session.commit()






def GET_USER_BY_ID(id):
    return User.query.get(int(id))


def GET_USER_BY_NAME(username):
    for user in User.query.all():       
        if user.username.lower() == username.lower():
            return user       
 