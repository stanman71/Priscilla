from flask            import Flask
from flask_bootstrap  import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail       import Mail

import os

app = Flask(__name__, static_url_path='/login')

#app.config.from_object('app.configuration.ProductionConfig')
app.config.from_object('app.configuration.DevelopmentConfig')

# Expose globals to Jinja2 templates
app.add_template_global(app.config , 'cfg'   )


from app.database import database
from app.sites import index, views

app.run(host='localhost', port=5000, debug=True)