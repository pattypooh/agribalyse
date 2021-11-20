import numpy as np
import pandas as pd

df = pd.read_csv("../../data/raw/liste_ingredient.csv")

liste_ingredients = df.columns.tolist()

#Create dataframe of all ingredients
df_ing=pd.DataFrame(data=liste_ingredients,columns=["Ingredients"])
df_ing 
#Create dataframe from input list of ingredients 
input_ls=["oeuf","lait"]

df_input=pd.DataFrame(data=input_ls,columns=["Ingredients"])
df_input['Presence']=np.ones(len(input_ls))
df_input
#Merge and replace NaNs with 0s
df_merge=df_ing.merge(df_input,how="left").replace(np.nan, 0)
df_merge