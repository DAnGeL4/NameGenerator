import os
from flask import Flask, render_template
from flask import session

from modules.flask_module.routes import routes
from modules.flask_module import app as app_mod

app = Flask('app')
app.config['SECRET_KEY'] = os.environ['flask_secret_key']

@app.route(routes['general'])
def general():
    app_mod.check_name_lists()
  
    selected_names = session['selected_names']
    removed_names = session['removed_names']
    
    generate_settings = dict({
        'race_list': app_mod.get_race_list(),
        'gender_list': app_mod.get_gender_list(),
    })
    
    return render_template('general.html', 
                           generate_settings=generate_settings,
                           selected_names=selected_names,
                           removed_names=removed_names)

@app.route(routes['slct_rm_gen'], methods=['POST',])
def select_remove_generate():
    respond = app_mod.select_remove_generate()          
    return respond

@app.route(routes['exclude'])
def exclude_name(name_id):
    respond = app_mod.exclude_name(name_id)
    return respond


def main():
  app.run(host='0.0.0.0', port=8080)