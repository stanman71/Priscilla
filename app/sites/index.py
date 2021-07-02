from flask                       import url_for, render_template, request, redirect
from werkzeug.security           import check_password_hash
from flask_login                 import LoginManager, login_user, logout_user

from flask_wtf                   import FlaskForm
from wtforms                     import StringField, PasswordField, BooleanField
from wtforms.validators          import DataRequired

from app                         import app
from app.backend.database_models import *
from app.common                  import COMMON, STATUS
from app.assets                  import *



""" ############# """
""" login manager """
""" ############# """

login_manager = LoginManager()
login_manager.init_app(app)

class LoginForm(FlaskForm):
	name        = StringField  (u'Name'    , validators=[DataRequired()])
	password    = PasswordField(u'Password', validators=[DataRequired()])
	remember    = BooleanField('remember me')

@login_manager.user_loader
def load_user(user_id):
    return GET_USER_BY_ID(user_id)


""" ################### """
""" site index / logout """
""" ################### """

@app.route('/', methods=['GET', 'POST'])
def index():
    page_title       = 'Bianca | Login'
    page_description = 'The login page'    

    # define login form here
    form = LoginForm()

    # Flask message injected into the page, in case of any errors
    msg = None

    if form.validate_on_submit():
        user = GET_USER_BY_NAME(form.name.data)

        if user:
            
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

            else:
                msg = "Wrong Password"

        else:
            msg = "Wrong Name"

    data = {'navigation': 'None'}

    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template( 'layouts/default.html',
                            data=data,
                            title=page_title,        
                            description=page_description,   
                            content=render_template( 'pages/index.html', 
                                                     form=form,
                                                     msg=msg) 
                            )


# logout user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))