
import pandas as pd
import numpy as np
from src.models import predict_model

df = pd.read_csv("liste_ingredient.csv")

liste_ingredients = df.columns.tolist()

def isiterable(obj):
    '''
    Getting sur an object is an iterable (i.e. a list )
    '''
    try:
        iter(obj)
        return True
    except TypeError: #not iterable
        return False

def ingredient_to_dataframe(liste_ingredients, ingredient_for_recipe):
    #Create dataframe of all ingredients
    initial_dataframe=pd.DataFrame(data=liste_ingredients,columns=["Ingredients"])
    #Create dataframe initialized at a zero value
    initial_dataframe["Presence"] = np.zeros(len(liste_ingredients))
    #Locate ingredient and flag it as a 1 value in Presence column
    initial_dataframe.loc[initial_dataframe["Ingredients"].isin(ingredient_for_recipe),'Presence']=1.0

    return initial_dataframe
def input_dataframe():
    ingred_df = pd.read_csv("liste_ingredient.csv")
    base_df = ingred_df.iloc[0:1, 13:]
    for col in base_df.columns:
        base_df[col].values[:] = 0
    return base_df

def predict_score(user_ingredients):
    '''
    Calls predict_model.predict with the list of user ingredients
    '''
    score = 0

    if len(user_ingredients) == 0:
        score = 'Please define the ingredients' 
    else:
        clean_ingredients = list(set(user_ingredients)) #removing duplicates
        score = predict_model.predict(clean_ingredients)
    return score

