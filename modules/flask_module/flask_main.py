###START ImportBlock
##systemImport
import os
import typing as typ
from flask import Flask, render_template
from flask import session

##customImport
from modules.flask_module.routes import routes
from modules.flask_module import app as app_mod

###FINISH ImportBlock

###START GlobalConstantBlock
app = Flask('app')
app.config['SECRET_KEY'] = os.environ['flask_secret_key']
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock

@app.route(routes['index'])
def general() -> str:
    '''
    Main path processing function.
    '''
    _ = app_mod.check_name_lists()
  
    selected_names = session['selected_names']
    removed_names = session['removed_names']
    
    generate_settings = dict({
        'race_list': app_mod.get_race_list(),
        'gender_list': app_mod.get_gender_list(),
    })
    
    return render_template('index.html', 
                           generate_settings=generate_settings,
                           selected_names=selected_names,
                           removed_names=removed_names)

@app.route(routes['slct_rm_gen'], methods=['POST',])
def select_remove_generate() -> str:
    '''
    The function of processing the selection in the list 
    of selected, removed or generating a name.
    '''
    respond = app_mod.select_remove_generate()          
    return respond

@app.route(routes['exclude'])
def exclude_name(name_id) -> str:
    '''
    A function to handle the exclusion of 
    a name from selected or deleted lists.
    '''
    respond = app_mod.exclude_name(name_id)
    return respond

###FINISH FunctionalBlock

###START MainBlock

def main() -> typ.NoReturn:
    '''
    Runs the flask application.
    '''
    app.run(host='0.0.0.0', port=8080)

###FINISH Mainblock