###START ImportBlock
##systemImport
import mongoengine as medb

##customImport
from database.medbNameSchemas import Race

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock

#####BEGIN Embedded and Templates Documents Area
    #.first embedded documents by order
    #(including embedded document template)
    #.second template documents
#####
class FirstLettersCounts(medb.EmbeddedDocument):
    vowelsCount = medb.IntField(min_value=0,
                                    default=0)
    consonantsCount = medb.IntField(min_value=0,
                                    default=0)
    
    meta = {'db_alias': 'mdbAnalytic'}
            
class ChainsAnalyticTemplate(medb.EmbeddedDocument):
    key = medb.StringField(max_length=200, 
                                required=True,
                                unique=True)
    count = medb.IntField(min_value=0,
                            default=0)
    chance = medb.FloatField(min_value=0,
                            default=0.0)
    
    meta = {'allow_inheritance': True,
            'abstract': True,
            'db_alias': 'mdbAnalytic'}

class Chains(ChainsAnalyticTemplate):

    meta = {'db_alias': 'mdbAnalytic'}

class ChainFrequency(ChainsAnalyticTemplate):
    
    meta = {'db_alias': 'mdbAnalytic'}

class LengthCountNames(medb.EmbeddedDocument):
    length = medb.IntField(min_value=0,
                                default=0)
    maxCountInName = medb.IntField(min_value=0,
                                default=0, 
                                unique_with='length')
    namesCount = medb.IntField(min_value=0,
                                default=0)
    chance = medb.FloatField(min_value=0,
                                default=0.0)
    
    meta = {'db_alias': 'mdbAnalytic'}

class RatingAnalyticTemplate(medb.Document):
    race = medb.ReferenceField(Race, 
                                required=True,
                                reverse_delete_rule=medb.CASCADE)
    key = medb.StringField(max_length=200, 
                                required=True,
                                unique_with='race')
    count = medb.IntField(min_value=0,
                            default=0)
    chance = medb.FloatField(min_value=0,
                            default=0.0)
    
    meta = {'allow_inheritance': True,
            'abstract': True,
            'db_alias': 'mdbAnalytic'}

class GroupChainsTemplate(medb.Document):
    race = medb.ReferenceField(Race, 
                                required=True,
                                reverse_delete_rule=medb.CASCADE)
    chains = medb.EmbeddedDocumentListField(Chains)
    chainFrequency = medb.EmbeddedDocumentListField(
                                ChainFrequency)
    lengthCountNames = medb.EmbeddedDocumentListField(
                                LengthCountNames)
    
    meta = {'allow_inheritance': True,
            'abstract': True,
            'db_alias': 'mdbAnalytic'}
#####END Embedded and Templates Documents Area

class GlobalCounts(medb.Document):
    race = medb.ReferenceField(Race, 
                                required=True,
                                unique=True,
                                reverse_delete_rule=medb.CASCADE)
    maxNamesCount = medb.IntField(min_value=0,
                                    default=0)
    femaleNamesCount = medb.IntField(min_value=0,
                                    default=0)
    maleNamesCount = medb.IntField(min_value=0,
                                    default=0)
    surnamesCount = medb.IntField(min_value=0,
                                    default=0)
    firstLettersCounts = medb.EmbeddedDocumentField(
                                    FirstLettersCounts)

    meta = {'collection': 'GlobalCounts',
            'db_alias': 'mdbAnalytic'}

class NameLettersCount(RatingAnalyticTemplate):
    
    meta = {'collection': 'NameLettersCount',
            'db_alias': 'mdbAnalytic'}

class VowelsCount(RatingAnalyticTemplate):
    
    meta = {'collection': 'VowelsCount',
            'db_alias': 'mdbAnalytic'}

class ConsonantsCount(RatingAnalyticTemplate):
    
    meta = {'collection': 'ConsonantsCount',
            'db_alias': 'mdbAnalytic'}

class FirstLetters(RatingAnalyticTemplate):
    
    meta = {'collection': 'FirstLetters',
            'db_alias': 'mdbAnalytic'}

class Letters(RatingAnalyticTemplate):
    
    meta = {'collection': 'Letters',
            'db_alias': 'mdbAnalytic'}

class ChainsCombinations(RatingAnalyticTemplate):
    
    meta = {'collection': 'ChainsCombinations',
            'db_alias': 'mdbAnalytic'}

class NameEndings(RatingAnalyticTemplate):
    
    meta = {'collection': 'NameEndings',
            'db_alias': 'mdbAnalytic'}

class VowelsChains(GroupChainsTemplate):
    
    meta = {'collection': 'VowelsChains',
            'db_alias': 'mdbAnalytic'}

class ConsonantsChains(GroupChainsTemplate):
    
    meta = {'collection': 'ConsonantsChains',
            'db_alias': 'mdbAnalytic'}
###FINISH FunctionalBlock

###START MainBlock
###FINISH Mainblock