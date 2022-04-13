from flask import request, url_for
from flask import redirect, session

from modules.dbTools import ME_DBService
from modules.nameGen import ManualNameGen

def get_random_name(race, gender):
    nameGen = ManualNameGen()
    name = nameGen.createCharacterName(race, gender)
    
    if not name:
        name = "Generation_error"
    return name

def get_race_list():
    service = ME_DBService()
    race_list = service.getRacesList()
    
    if not race_list:
        race_list = ['Have_not_race']
        
    return race_list

def get_gender_list():
    service = ME_DBService()
    gender_list = service.getGenderGroupsList()
    
    if not gender_list:
        gender_list = ['Have_not_gender']
        
    return gender_list

def check_name_lists():
    if 'selected_names' not in session:
        session['selected_names'] = list([])
    if 'removed_names' not in session:
        session['removed_names'] = list([])
    if 'name_id_list' not in session:
        session['name_id_list'] = 0

def add_name_to(session_key):
    session['name_id_list'] += 1
  
    data = {
        'id': session['name_id_list'],
        'name': request.form.get('nameInput'), 
        'race': request.form.get('raceSelect'), 
        'gender': request.form.get('genderSelect')
    }
  
    session['race'] = data['race']
    session['gender'] = data['gender']
    session[session_key].append(data)
  
    if 'name' in session:
      session.pop('name')

def generate_name():
    race = request.form.get('raceSelect')
    gender = request.form.get('genderSelect')
  
    name = get_random_name(race, gender)
  
    session['name'] = name
    session['race'] = race
    session['gender'] = gender

def select_remove_generate():
  
    if request.method == 'POST':
        _ = check_name_lists()
      
        if request.form.get('select_name') == 'select_name':
            _ = add_name_to('selected_names')
          
        elif request.form.get('remove_name') == 'remove_name':
            _ = add_name_to('removed_names')
          
        elif request.form.get('generate_name') == 'generate_name':
            _ = generate_name()
            return redirect(url_for('general'))
          
    return redirect(url_for('general'))

def exclude_by_id(name_id, session_key):
    _ = check_name_lists()
  
    name_list = session[session_key]
    for i in range(len(name_list)):
      
      if name_list[i]['id'] == name_id:
        name_list.pop(i)
        break
        
    return name_list

def exclude_name(name_id):
    if request.args.get('exclude_name') == 'exclude_s_name':
        session['selected_names'] = exclude_by_id(name_id, 
                                                  'selected_names')
      
    elif request.args.get('exclude_name') == 'exclude_r_name':
        session['removed_names'] = exclude_by_id(name_id, 
                                                 'removed_names')
  
    return redirect(url_for('general'))