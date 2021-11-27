###START ImportBlock
###FINISH ImportBlock

###START GlobalConstantBlock

#####BEGIN TemplateBlock
TEMPLATE_GLOBAL_RACE = {
    "Races": [
        #TEMPLATE_LOCAL_RACE
    ]
}
TEMPLATE_LOCAL_RACE = {
    "tmp_Race": {
        "Genders": {
            "Female": {
                "Names": []
            }, 
            "Male": {
                "Names": []
            }
        },
        "Surnames": []
    }
}
TEMPLATE_GLOBAL_ANALYTIC = {
    "Analytics": {
        #TEMPLATE_NAMES_ANALYTIC
    }
}
TEMPLATE_NAMES_ANALYTIC = {
    "tmp_Race":{
        "Max_Names_Count": 0,               #How much names in initialized DB.
        "Female_Names_Count": 0,
        "Male_Names_Count": 0,
        "Surnames_Count": 0,
        "Name_Letters_Count": {             #Names lenght and their repeats
            #TEMPLATE_RATING_ANALYTIC       ##amount.
        },
        "Vowels_Count": {                   #Vowels amount in names and their 
            #TEMPLATE_RATING_ANALYTIC       ##repeats amount.
        },
        "Consonants_Count": {               #Consonants amount in names and 
            #TEMPLATE_RATING_ANALYTIC       ##their repeats amount.
        },
        "First_Letters": {                  #First letters in names and their
            #TEMPLATE_RATING_ANALYTIC       ##repeats amount.
            "Vowels_Count": 0,              #Count of names with this first
            "Consonants_Count": 0,          ##letter
        },
        "Letters": {                        #All letters, used in names, and 
            #TEMPLATE_RATING_ANALYTIC       ##their repeats amount.
        },
        "Vowels_Chains": {
            "Chains": {                     #Themselve vowel chains and their 
                #TEMPLATE_RATING_ANALYTIC   ##amount.
            },
            "Chain_Frequency": {            #Amount of names with vowel chains and 
                #TEMPLATE_RATING_ANALYTIC   ##their repeats amount.
            },
            "Length_Count_Names": {         #The max number of repeats of a chain of a certain
                #TEMPLATE_CHAINS_ANALYTIC   ##length in a name and the number of such names
            }
        },
        "Consonants_Chains": {
            "Chains": {                     #Themselve consonant chains and
                #TEMPLATE_RATING_ANALYTIC   ##their amount.
            },
            "Chain_Frequency": {            #Amount of names with consonant chains 
                #TEMPLATE_RATING_ANALYTIC   ##and their repeats amount.
            },
            "Length_Count_Names": {         #The max number of repeats of a chain of a certain
                #TEMPLATE_CHAINS_ANALYTIC   ##length in a name and the number of such names
            }
        },
        "Chains_Combinations": {             #Combinations of 2 adjacent letters
            #TEMPLATE_RATING_ANALYTIC       ##chains includings 1 letter chains
        },
        "Name_Endings": {                   #Combinations of 2 adjacent letters
            #TEMPLATE_RATING_ANALYTIC       ##chains but in the end name.
        }
    }
}
TEMPLATE_RATING_ANALYTIC = {                #Container for keys from #TEMPLATE_NAMES_ANALYTIC
    "tmp_Key": {
        "Count": 0,
        "Chance": 0,
    }
}
TEMPLATE_CHAINS_ANALYTIC = {                #Container for #Length_Count_Names key from #TEMPLATE_NAMES_ANALYTIC
    "tmp_Length": {
        "Max_Count_In_Name": 0,
        "Names_Count": 0,
        "Chance": 0,
    }
}
#####END TemplateBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock
###FINISH FunctionalBlock

###START MainBlock
###FINISH Mainblock