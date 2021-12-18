###START ImportBlock
##systemImport
import mongoengine as medb

##customImport
###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock
class Race(medb.Document):
    '''
    Contains data about races found in the names db.
    '''
    race = medb.StringField(max_length=200, 
                            required=True, 
                            unique=True)

    meta = {'collection': 'Race',
            'db_alias': 'mdbName'}
            

class GenderGroups(medb.Document):
    '''
    Contains data about gender groups (including common).
    '''
    gender_group = medb.StringField(max_length=200, 
                                required=True,
                                unique=True)

    meta = {'collection': 'GenderGroups',
            'db_alias': 'mdbName'}


class GenderTemplate(medb.Document):
    '''
    Template for gender clases.
    Contains data about name and race of name.
    '''
    name = medb.StringField(required=True,
                            unique_with='race')
    race = medb.ReferenceField(Race, 
                            required=True,
                            reverse_delete_rule=medb.CASCADE)

    meta = {'allow_inheritance': True,
            'abstract': True,
            'db_alias': 'mdbName'}


class Male(GenderTemplate):
    '''
    Contains data about names for male gender group.
    '''
    meta = {'collection': 'Male',
            'db_alias': 'mdbName'}


class Female(GenderTemplate):
    '''
    Contains data about names for female gender group.
    '''
    meta = {'collection': 'Female',
            'db_alias': 'mdbName'}


class Surnames(GenderTemplate):
    '''
    Contains data about names for surname gender group.
    '''
    meta = {'collection': 'Surnames',
            'db_alias': 'mdbName'}

###FINISH FunctionalBlock

###START MainBlock
###FINISH Mainblock