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
    globalExist = medb.BooleanField(default=False)

    meta = {'collection': 'GlobFlags',
            'max_documents': 1,
            'db_alias': 'mdbCheckSum'}

class ChecksumFiles(medb.Document):
    file = medb.StringField(required=True, 
                            unique=True)
    checksum = medb.StringField(max_length=200, 
                            required=True)

    meta = {'collection': 'ChecksumFiles',
            'db_alias': 'mdbCheckSum'}

###FINISH FunctionalBlock

###START MainBlock
###FINISH Mainblock