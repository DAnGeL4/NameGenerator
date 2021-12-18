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
class GlobalFlags(medb.Document):
    '''
    Contains a flag whether the checksum db has been changed.
    '''
    globalExist = medb.BooleanField(default=False)

    meta = {'collection': 'GlobalFlags',
            'max_documents': 1,
            'db_alias': 'mdbCheckSum'}


class ChecksumFiles(medb.Document):
    '''
    Contains data about used files and state of his data.
    '''
    file = medb.StringField(required=True, 
                            unique=True)
    checksum = medb.StringField(max_length=200, 
                            required=True)

    meta = {'collection': 'ChecksumFiles',
            'db_alias': 'mdbCheckSum'}

###FINISH FunctionalBlock

###START MainBlock
###FINISH Mainblock