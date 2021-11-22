import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

MODELS_FILE_PATH = './../models'
INTERIM_FILE_PATH = './../data/interim'
INPUT_DATA_FILE_PATH = './../data/processed/'

score_predictor = joblib.load(os.path.join(MODELS_FILE_PATH,'score_predictor.joblib'))
canonical_df = pd.read_csv(os.path.join(INPUT_DATA_FILE_PATH,'ingredients_data_format.csv'))
statistics_df = pd.read_csv(os.path.join(INTERIM_FILE_PATH,'Agribalyse_MinMax ingredient.csv'))


def get_transposed(statistics_df, metric, prefix:str):
    metric_df =  statistics_df.set_index('Ingredients')[[metric]].transpose().reset_index(drop=True)
    new_col_names = [f'{prefix}{c}' for c in metric_df.columns]
    metric_df.columns = new_col_names
    return metric_df

def generate_transposed_statistics(df):
    #transpose minEF
    minEF_df = get_transposed(df, 'min_EF', prefix='min_EF_')
    
    #transpose maxEF
    maxEF_df = get_transposed(df, 'max_EF', 'max_EF_')
    
    #Concatenate minEF and maxEF
    return pd.concat([minEF_df, maxEF_df], axis=1)

def format_ingredients_list(user_input, canonical_df, statistics_df)->pd.DataFrame:
    statistics_user_input = generate_transposed_statistics(statistics_df.set_index('Ingredients').loc[user_input,:].reset_index())
    canonical_df.loc[:,statistics_user_input.columns] = statistics_user_input
    canonical_df.loc[:,user_input] = 1


def predict(ingredients):
    #Before predicting, add extra features
    format_ingredients_list(ingredients, canonical_df, statistics_df)

    score = score_predictor.predict(canonical_df)
    return score