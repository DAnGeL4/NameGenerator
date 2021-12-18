###START ImportBlock
##systemImport
import mongoengine as medb
import typing as typ

##customImport
from database.medbNameSchemas import Race, GenderGroups

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock

#####BEGIN Embedded and Templates Documents Area
    #.first embedded documents by order
    #(including embedded document template)
    #(exception for templates for multi databases)
    #.second template documents
#####
class FirstLettersCounts(medb.EmbeddedDocument):
    '''
    Template for embedded field of first letters count.
    Contains data about count of names with type of first letters.
    '''
    vowelsCount = medb.IntField(min_value=0,
                                    default=0)
    consonantsCount = medb.IntField(min_value=0,
                                    default=0)
    
    meta = {'db_alias': 'mdbAnalytic'}
            

class ChainsAnalyticTemplate(medb.EmbeddedDocument):
    '''
    Template for embedded field of chains clases.
    Contains data about key count and chance.
    '''
    count = medb.IntField(min_value=0,
                            default=0)
    chance = medb.FloatField(min_value=0,
                            default=0.0)
    
    meta = {'allow_inheritance': True,
            'abstract': True,
            'db_alias': 'mdbAnalytic'}


class ChainsTemplate(ChainsAnalyticTemplate):
    '''
    Template for embedded field of chains clases.
    Contains data about string key, his count and chance.
    '''
    key = medb.StringField(max_length=200,              #*
                                required=True)

    meta = {'db_alias': 'mdbAnalytic'}


class ChainFrequencyTemplate(ChainsAnalyticTemplate):
    '''
    Template for embedded field of chains clases.
    Contains data about number key, his count and chance.
    '''
    key = medb.IntField(min_value=0,                    #*
                            default=0)
    
    meta = {'db_alias': 'mdbAnalytic'}


class LengthCountNames(medb.EmbeddedDocument):
    '''
    Template for embedded field of chains clases.
    Contains data about length of chains, her count in name, 
    global count and chance.
    '''
    length = medb.IntField(min_value=0,                 #*
                                default=0)
    maxCountInName = medb.IntField(min_value=0,
                                default=0)              #*
    namesCount = medb.IntField(min_value=0,
                                default=0)
    chance = medb.FloatField(min_value=0,
                                default=0.0)
    
    meta = {'db_alias': 'mdbAnalytic'}


class RatingAnalyticTemplate(medb.Document):
    '''
    Template for rating clases.
    Contains data about string key, his count and chance.
    '''
    race = medb.ReferenceField(Race, 
                                required=True,
                                reverse_delete_rule=medb.CASCADE)
    gender_group = medb.ReferenceField(GenderGroups, 
                                required=True,
                                reverse_delete_rule=medb.CASCADE)
    key = medb.StringField(max_length=200, 
                                required=True)
    count = medb.IntField(min_value=0,
                            default=0)
    chance = medb.FloatField(min_value=0,
                            default=0.0)
    
    meta = {'indexes': [
                'key',
                {'fields': ['race', 'gender_group', 'key'], 'unique': True},
            ],
            'allow_inheritance': True,
            'abstract': True,
            'db_alias': 'mdbAnalytic'}


class CountRatingAnalyticTemplate(RatingAnalyticTemplate):
    '''
    Template for rating clases.
    Contains data about number key, his count and chance.
    '''
    key = medb.IntField(min_value=0,
                            default=0)
    
    meta = {'indexes': [
                'key',
                {'fields': ['race', 'gender_group', 'key'], 'unique': True},
            ],
            'allow_inheritance': True,
            'abstract': True,
            'db_alias': 'mdbAnalytic'}


class GroupChainsTemplate(medb.Document):
    '''
    Template for containers of chains.
    Contains data on combinations of adjacent chains 
    of letters (chains can even be 1 letter), their frequency, 
    length and the number of such chains in the name and globally.

    Contains additional functions for working with fields of embedded lists.
    '''
    race = medb.ReferenceField(Race, 
                                required=True,
                                reverse_delete_rule=medb.CASCADE)
    gender_group = medb.ReferenceField(GenderGroups, 
                                required=True,
                                reverse_delete_rule=medb.CASCADE,
                                unique_with='race')
    chains = medb.EmbeddedDocumentListField(ChainsTemplate)
    chainFrequency = medb.EmbeddedDocumentListField(
                                ChainFrequencyTemplate)
    lengthCountNames = medb.EmbeddedDocumentListField(
                                LengthCountNames)
    
    meta = {'allow_inheritance': True,
            'abstract': True,
            'db_alias': 'mdbAnalytic'}
    
    @classmethod
    def _get_embedded_list_field_type(cls, field:str) -> medb.EmbeddedDocument:
        '''
        Returns the type of EmbeddedDocumentListField field.
        '''
        fieldsTypes = dict({
            'chains': ChainsTemplate,
            'chainFrequency': ChainFrequencyTemplate,
            'lengthCountNames': LengthCountNames
            })

        if field not in fieldsTypes.keys():
            return None
        return fieldsTypes[field]

    def add_unique(self, field: str, 
                   embDoc: medb.EmbeddedDocument) -> typ.NoReturn:
        '''
        Adds unique embedded document for field.
        '''
        fieldsOperation = dict({
            'chains': self.add_unique_chain,
            'chainFrequency': self.add_unique_freq,
            'lengthCountNames': self.add_unique_length_count
        })
        fieldsOperation[field](embDoc)

    def add_unique_chain(self, 
                         chainEmbDoc: medb.EmbeddedDocument) -> typ.NoReturn:
        '''
        Adds embedded document for chains if his not exist.
        '''
        existing = self.chains.filter(key=chainEmbDoc.key)
        if existing.count() == 0:
            self.chains.append(chainEmbDoc)
            
    def add_unique_freq(self, 
                        frequencyEmbDoc: medb.EmbeddedDocument) -> typ.NoReturn:
        '''
        Adds embedded document for chainFrequency if his not exist.
        '''
        existing = self.chainFrequency.filter(key=frequencyEmbDoc.key)
        if existing.count() == 0:
            self.chainFrequency.append(frequencyEmbDoc)
    
    def add_unique_length_count(self, 
                                lengthEmbDoc: medb.EmbeddedDocument) -> typ.NoReturn:
        '''
        Adds embedded document for lengthCountNames if his not exist.
        '''
        filtered = self.lengthCountNames.filter(length=lengthEmbDoc.length)
        existing = filtered.filter(maxCountInName=lengthEmbDoc.maxCountInName)
        if existing.count() == 0:
            self.lengthCountNames.append(lengthEmbDoc)
        
#####END Embedded and Templates Documents Area

class GlobalCounts(medb.Document):
    '''
    Contains data about all names counts in names db and
    count of names with type of first letters.
    '''
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


class NameLettersCount(CountRatingAnalyticTemplate):
    '''
    Contains data about names lenght and their repeats amount.
    '''
    meta = {'collection': 'NameLettersCount',
            'db_alias': 'mdbAnalytic'}


class VowelsCount(CountRatingAnalyticTemplate):
    '''
    Contains data about vowels amount in names 
    and their repeats amount.
    '''
    meta = {'collection': 'VowelsCount',
            'db_alias': 'mdbAnalytic'}


class ConsonantsCount(CountRatingAnalyticTemplate):
    '''
    Contains data about consonants amount in names 
    and their repeats amount.
    '''
    meta = {'collection': 'ConsonantsCount',
            'db_alias': 'mdbAnalytic'}

class FirstLetters(RatingAnalyticTemplate):
    '''
    Contains data about first letters in names 
    and their repeats amount.
    '''
    meta = {'collection': 'FirstLetters',
            'db_alias': 'mdbAnalytic'}


class Letters(RatingAnalyticTemplate):
    '''
    Contains data about all letters, used in names, 
    and their repeats amount.
    '''
    meta = {'collection': 'Letters',
            'db_alias': 'mdbAnalytic'}


class VowelsChains(GroupChainsTemplate):
    '''
    Contains data about vowels chains.
    '''
    meta = {'collection': 'VowelsChains',
            'db_alias': 'mdbAnalytic'}


class ConsonantsChains(GroupChainsTemplate):
    '''
    Contains data about consonants chains.
    '''
    meta = {'collection': 'ConsonantsChains',
            'db_alias': 'mdbAnalytic'}


class ChainsCombinations(RatingAnalyticTemplate):
    '''
    Contains data about combinations of adjacent 
    letters chains (includings 1 letter chains)
    '''
    meta = {'collection': 'ChainsCombinations',
            'db_alias': 'mdbAnalytic'}


class NameEndings(RatingAnalyticTemplate):
    '''
    Contains data about Combinations of adjacent 
    letters chains but in the end name.
    '''
    meta = {'collection': 'NameEndings',
            'db_alias': 'mdbAnalytic'}
###FINISH FunctionalBlock

###START MainBlock
###FINISH Mainblock