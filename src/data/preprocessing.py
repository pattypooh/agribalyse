import pandas as pd
import logging
import re
from pandas.core.frame import DataFrame
import unidecode
from pathlib import Path

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)

def _remove_quotes(raw_text)->str:
    '''
    Remove quotes from word contractions in raw_text. For ex. d'emballage --> emballage
    '''
    clean_text = re.sub('\w+\'', '', raw_text)
    return clean_text

def new_column_name(name) ->str:
    '''
    Format a name by removing short words like de, des, aux,... and replacing spaces with underscores (_)
    '''
    #new_name = remove_quotes(name)
    tokens = [_remove_quotes(unidecode.unidecode(token)) for token in name.split('(')[0].strip().split(' ')]
    if len(tokens) >2:
        tokens = [token for token in tokens if len(token) > 3]
    new_name = '_'.join(tokens)
    return new_name

def new_column_names(df:pd.DataFrame):
    '''
    Returns new column names of a dataframe, according to 
    '''
    new_names = [new_column_name(name) for name in df.columns.to_list()] 
    return new_names

def strip_text_columns(df:pd.DataFrame)->pd.DataFrame:
    '''
    Retrieves columns of type ''object'' and strips trailing spaces in the values

    '''
    index_obj_cols = df.select_dtypes(include='object').columns
    for col in index_obj_cols:
        df[col] = df[col].str.strip()
    return df

def toto():
    print('hola')
