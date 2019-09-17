from flask            import Flask
from flask_bootstrap  import Bootstrap
from flask_mail       import Mail

# load RES
from app import assets  

app = Flask(__name__, static_url_path='/static')

#app.config.from_object('app.configuration.ProductionConfig')
app.config.from_object('app.configuration.DevelopmentConfig')

# Expose globals to Jinja2 templates
app.add_template_global(assets     , 'assets')
app.add_template_global(app.config , 'cfg'   )

from app.sites           import login, plants, devices, users, system, system_log, views, errors
from app.database.models import *

app.run(host='localhost', port=5000, debug=True)