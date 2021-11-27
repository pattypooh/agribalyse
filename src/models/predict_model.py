import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#MODELS_FILE_PATH = './../models'
#INTERIM_FILE_PATH = './../data/interim'
#INPUT_DATA_FILE_PATH = './../data/processed/'

#Modifications in directory paths necessary for deployment of app in Heroku
curren_dir = os.getcwd()



score_predictor = joblib.load(os.path.join(curren_dir,'src/models/score_predictor.joblib'))
canonical_df = pd.read_csv(os.path.join(curren_dir,'data/processed/ingredients_data_format.csv'))
statistics_df = pd.read_csv(os.path.join(curren_dir,'data/interim/Agribalyse_MinMax ingredient.csv'))


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

def format_ingredients_list(user_input, base_df, statistics_df)->pd.DataFrame:
    '''
        Takes the user input of ingredients list and statistics_df and fills in the values in base_df
        
        Parameters
        ------------------
        user_input: 
            List like of str (correponding to ingredients)
        base_df:
            The base dataframe to fill in with 1s for every ingredient in user_input and the statistics(min,max) for the same ingredients 
        statistics_df
            The statistics of every ingredient

        Returns
        --------------------
        None 

    '''
    statistics_user_input = generate_transposed_statistics(statistics_df.set_index('Ingredients').loc[user_input,:].reset_index())
    base_df.loc[:,statistics_user_input.columns] = statistics_user_input
    base_df.loc[:,user_input] = 1



def predict(ingredients):
    '''
    Launch the model and predicts the score of the list of ingredients
    Parameters
    ---------------
    ingredients
        - List type of str representend a list of ingredients used in a dish recipe
    Returns
    ----------------
    A float value representing the score EF of the list of ingredients   
    '''


    base_df = canonical_df.copy()

    #Before predicting, add extra features
    format_ingredients_list(ingredients, base_df, statistics_df)
    score = score_predictor.predict(base_df)

    return score