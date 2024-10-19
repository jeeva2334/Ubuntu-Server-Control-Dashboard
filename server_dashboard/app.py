from flask import Flask, render_template
from routes.system import system_blueprint
from routes.services import services_blueprint
from routes.execute import execute_blueprint
from routes.files import files_blueprint
from routes.users import users_blueprint
from routes.groups import group_blueprint

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(system_blueprint, url_prefix='/api/system')
app.register_blueprint(services_blueprint, url_prefix='/api/services')
app.register_blueprint(execute_blueprint, url_prefix='/api/execute')
app.register_blueprint(files_blueprint, url_prefix='/api/files')
app.register_blueprint(users_blueprint, url_prefix='/api/users')
app.register_blueprint(group_blueprint, url_prefix='/api/groups')

# Index Route
@app.route('/')
def index():
    return render_template("dashboard.html")

@app.route('/users')
def user_template():
    return render_template("users.html")

@app.route('/users/<id>')
def user_details_template(id):
    return render_template("users_details.html", id=id)

@app.route('/groups/<int:id>')
def group_details_template(id):
    return render_template("group_details.html", id=id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
