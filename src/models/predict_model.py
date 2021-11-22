import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

score_predictor = joblib.load("./../models/score_predictor.joblib")
desc_ingred = pd.read_csv('./../data/processed/ingredients_data_format.csv')

def rename_pivoted_columns(pivot_ing_minmax: pd.DataFrame)->pd.DataFrame:
    new_minmax_df = pivot_ing_minmax.copy()
    new_col_index = [f'{multiindex[0]}_{multiindex[1]}' if multiindex[1]!='' else multiindex[0] for multiindex in pivot_ing_minmax.columns]
    new_minmax_df.columns=new_col_index
    new_minmax_df = new_minmax_df.fillna(0)
    #new_minmax_df = new_minmax_df.drop(columns=drop_cols)
    return new_minmax_df

def add_features(user_ingred_df)->pd.DataFrame:
    new_ing_df = user_ingred_df.merge(desc_ingred, how = 'inner', left_on='Ciqual_AGB', right_on="Ciqual_AGB")


def predict(ingredients):
    #ici le model
    #Before predicting, add extra features
    

    score = score_predictor.predict(ingredients)
    return score