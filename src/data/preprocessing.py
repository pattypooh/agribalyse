# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv
import re
import unidecode
import utils
import numpy as np

log_fmt = '%(asctime)s - %(module)s - %(funcName)s - %(levelname)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)
## Configuraiton that can be loaded from a conf file
def synthese_keep_columns():
    keep_cols = [i for i in range(27)]
    return keep_cols

def ingredients_keep_columns():
    keep_cols = [0, *range(6, 22)]
    return keep_cols

def etapes_keep_columns():
    keep_cols = [0, *range(6, 102)]
    return keep_cols

def synthese_key()->int:
    return 0

def ingredients_key()->int:
    return 0

def etapes_key()->int:
    return 0

def merge_keys():
    return[synthese_key(), ingredients_key(), etapes_key()]


def column_name(df: pd.DataFrame, index_col:int)-> str:
    return df.columns[index_col]

## Configuraiton that can be loaded from a conf file

def _remove_quotes(raw_text)->str:
    '''
    Remove quotes from word contractions in raw_text. For ex. d'emballage --> emballage
    '''
    clean_text = re.sub('\w+\'', '', raw_text)
    return clean_text

def _new_column_name(name, stop_words) ->str:
    '''
    Format a name by removing short words like de, des, aux,... and replacing spaces with underscores (_)
    '''
    split_pattern = r'(\(.*\))' # this pattern matches all characters between parenthesis and the parenthesis 
    tokens = re.sub(split_pattern, '', name).split(' ')
    logger.debug(f'tokens:{tokens}')
    tokens = [_remove_quotes(unidecode.unidecode(token)).strip() for token in tokens]
    tokens = [token for token in tokens if token not in stop_words]
    logger.debug(f'tokens:{tokens}')
    new_name = '_'.join(tokens)
    return new_name


def change_column_names(df:pd.DataFrame):
    '''
    Retrieves df column names and transforms them to cut the spaces, remove stop words

    Returns
    ---------
    DataFrame  the current dataframe with new names
    '''
    stop_words = ['de', 'aux', 'des', 'et', 'en', 'au' ,'-', 'du']
    current_names = df.columns.tolist()
    new_names = [_new_column_name(name, stop_words) for name in current_names]
    df.columns = new_names
    return df

def cast_dtype_to_str(data_df:pd.DataFrame, columns)->pd.DataFrame:
    if type(columns) == list:
        if len(columns) < 1:
            raise Exception("Sorry, no column names were passed") 
        dict_dtypes = {col:str for col in columns}
    else:
        if type(columns) != str:
            raise Exception("Sorry, the type of the column name must be str")
        dict_dtypes = {columns:str}
    
    #dict_dtypes = {col:str for col in columns}
    tr_df = data_df.astype(dict_dtypes)
    return tr_df

def merge_dataset(df1, df2, df1_key, df2_key)->pd.DataFrame:   
    
    if df1[df1_key].dtype != df2[df2_key].dtype:
        raise TypeError("Different dtypes of keys used to merge") 
    
    merged_df = pd.merge(df1, df2, left_on=df1_key, right_on=df2_key, how='inner')
    return merged_df

def pivot_ingredients(ingred_df, column='Ingredients')->pd.DataFrame:
    '''
    Pivot dataframe of ingredients to convert each ingredient into colum :using get_dummies
    '''
    #ingred_pivot = pd.get_dummies(ingred_df, columns=[column])
    ingred_pivot = pd.pivot(ingred_df, index=[], columns=[], values=[]).rename_axis(None)
    return ingred_pivot

def merge_datasets(synthese_df, ingred_df, etapes_df, df1_key, df2_key, df3_key, d2_keep, d3_keep)->pd.DataFrame:
    '''
    Creates 2 merged data sets. The 1st one is the synthese vs ingredients and the 2nd one is
    synthse vs etapes.  
    '''
    #transform all keys to strings (or ints)
    logger.info('Starting merging datasets')

    syn_df= cast_dtype_to_str(synthese_df, df1_key)
    ing_df= cast_dtype_to_str(ingred_df, df2_key).iloc[:,d2_keep]
    logger.info(f'{ingred_df.shape}')
    eta_df= cast_dtype_to_str(etapes_df, df3_key).iloc[:, d3_keep]
    print(df1_key, df2_key, df3_key)

    # first pivot ingredients dataframe
    ing_df = pivot_ingredients(ing_df, 'Ingredients')
    
    merged_syn_ingred_df = merge_dataset(syn_df, ing_df, df1_key, df2_key)
    merged_syn_etape_df = merge_dataset(syn_df, eta_df, df1_key, df3_key)

    return merged_syn_ingred_df, merged_syn_etape_df

def preprocess_dataset(file_name: str, input_filepath, output_filepath):
    '''
    Reads a file, then standardize the column names, clean spaces in categorical data, remove duplicates and 
    saves a new cleaned file
    Parameters:
    ----------------------
    file_name: 
        A file name
    input_filepath: 
        The path where the file_name can be found
    output_filepath: 
        The path where the new file is saved, with the same name than file_name

    '''
    logger.info(f'Preprocessing dataset {input_filepath}/{file_name}')

    data_df = utils.load_dataset(input_filepath, file_name)
    data_df = change_column_names(data_df)
    #TODO move this cleaning to make_dataset
    # data_df = clean_str_values(data_df)
    #data_df.to_csv(os.path.join(output_filepath,file_name), index=False )
        
    logger.debug(f'Dataset preprocessed and saved at {output_filepath}/{file_name}')
    return data_df


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    logger.info('Making final data set from raw data')    
    # Retrieve all files in from raw data folder and make basic cleaning
    files = ['Agribalyse_Synthese.csv', 'Agribalyse_Detail ingredient.csv', 'Agribalyse_Detail etape.csv']
    dfs = list()
    for file_name in files:
        df = preprocess_dataset(file_name, input_filepath, output_filepath)
        dfs.append(df)
    # Check that the files were created in the output_filpath
    #TODO
    # retrieve columns to be used for merge
    merge_columns = [column_name(df, merge_keys()[i]) for i,df in enumerate(dfs)]
    new_ingred_df, new_etape_df = merge_datasets(*dfs, *merge_columns, \
                                d2_keep=ingredients_keep_columns(), d3_keep=etapes_keep_columns())

    new_ingred_df.to_csv(os.path.join(output_filepath, files[1]))
    new_etape_df.to_csv(os.path.join(output_filepath, files[2]))



if __name__ == '__main__':
    #log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    #logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()