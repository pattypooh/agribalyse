
#from src.models import predict_model
import pandas as pd
import numpy as np

df = pd.read_csv("../../data/raw/liste_ingredient.csv")
liste_ingredients = df.columns.tolist()

def ingredient_to_dataframe(liste_ingredients, ingredient_for_recipe):
    #Create dataframe of all ingredients
    initial_dataframe=pd.DataFrame(data=liste_ingredients,columns=["Ingredients"])
    #Create dataframe initialized at a zero value
    initial_dataframe["Presence"] = np.zeros(len(liste_ingredients))
    #Locate ingredient and flag it as a 1 value in Presence column
    initial_dataframe.loc[initial_dataframe["Ingredients"].isin(ingredient_for_recipe),'Presence']=1.0

    return initial_dataframe

#def predict_score(ingredients_user):
#    score = 1
#    df_213_ing = ingredient_to_dataframe()
#    
#    score = predict_model(df_213_ing)
#   
#    return score
