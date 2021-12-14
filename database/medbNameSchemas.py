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
#####Names
class Race(medb.Document):
    race = medb.StringField(max_length=200, 
                            required=True, 
                            unique=True)

    meta = {'collection': 'Race',
            'db_alias': 'mdbName'}


class Gender(medb.Document):
    name = medb.StringField(required=True,
                            unique_with='race')
    race = medb.ReferenceField(Race, 
                            required=True,
                            reverse_delete_rule=medb.CASCADE)

    meta = {'allow_inheritance': True,
            'abstract': True,
            'db_alias': 'mdbName'}


class Male(Gender):

    meta = {'collection': 'Male',
            'db_alias': 'mdbName'}


class Female(Gender):

    meta = {'collection': 'Female',
            'db_alias': 'mdbName'}


class Surnames(Gender):
    
    meta = {'collection': 'Surnames',
            'db_alias': 'mdbName'}

###FINISH FunctionalBlock

###START MainBlock
###FINISH Mainblock