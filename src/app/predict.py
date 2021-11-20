
from src.models import predict_model
import pandas as pd
import numpy as np

df = pd.read_csv("../../data/raw/liste_ingredient.csv")
liste_ingredients = df.columns.tolist()

def ingredient_to_dataframe(ingredients):
    #Create dataframe of all ingredients
    initial_dataframe=pd.DataFrame(data=liste_ingredients,columns=["Ingredients"])
    ingredients = []
    #Create dataframe from input list of ingredients 
    dataframe_ingredient=pd.DataFrame(data=ingredients,columns=["Ingredients"])
    dataframe_ingredient['Presence']=np.ones(len(ingredients))
    #Merge and replace NaNs with 0s
    final_dataframe = initial_dataframe.merge(dataframe_ingredient,how="left").replace(np.nan, 0)

    return final_dataframe

def predict_score(ingredients_user):
    score = 1
    df_213_ing = ingredient_to_dataframe()
    
    score = predict_model(df_213_ing)
    
    return score

