# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv
import re
from pandas.core import indexing
import unidecode
import numpy as np
import box

log_fmt = '%(asctime)s - %(module)s - %(funcName)s - %(levelname)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)

## Configuration values for each table.  It could be loaded from a conf file
dict_params= {'synthese': {'file_name':'Agribalyse_Synthese.csv',
                            'keep_cols':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], #columns to keep
                            'index_key':[0], #table primary key
                            },
            'ingredients':{'file_name':'Agribalyse_Detail ingredient.csv',
                            'keep_cols':[0, 2, 3, 4, 5, 6, 7],#columns to keep
                            'index_key':[0], #table primary key
                            'pivot_idx_key':[0, 1, 2, 3, 4], # Column index to use for pivot
                            'pivot_idx_col':5, # Position of the column that will be pivoted
                            'pivot_idx_values':6,# Position of the column to be used as values for the pivoted column
                            'pivot_keep_cols':[0, 2, 3, 4, 5, 6, 7],}, 

            'etapes':{'file_name':'Agribalyse_Detail etape.csv',
                    'keep_cols':[0, 8, 9, 10, 11, 12, 13],#columns to keep
                            'index_key':[0], #table primary key
                            }
            }

params = box.Box(dict_params) #It allows to use dots instead of [ ] to access a value in a dictionary

def get_param(dataset_name:str, param_name:str):
    return dict_params[dataset_name][param_name]


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
    tokens = [_remove_quotes(unidecode.unidecode(token)).strip() for token in tokens]
    tokens = [token for token in tokens if token not in stop_words]
    new_name = '_'.join(tokens)
    return new_name

def change_column_names(df:pd.DataFrame):
    '''
    Retrieves df column names and transforms them to cut the spaces, remove stop words

    Returns
    ---------
    DataFrame  the current dataframe with new names
    '''
    logger.debug(f'Formatting column names of dataframe')
    stop_words = ['de', 'aux', 'des', 'et', 'en', 'au' ,'-', 'du']
    current_names = df.columns.tolist()
    new_names = [_new_column_name(name, stop_words) for name in current_names]
    df.columns = new_names
    return df

def cast_dtype_to_str(data_df:pd.DataFrame, columns)->pd.DataFrame:
    '''
    Changes the dtype for columns in a DataFrame
    Input
    -------------
    data_df  The dataframe
    columns  The column label or list of column labels representing to be casted to str
    A new dataframe with the same size of the input data_df but with dtypes changed.
    Returns
    -------------
    '''
    logger.debug(f'Start casting columns:{columns} to str')
    #logger.debug(f'type of input columns: {type(columns)}')
    if type(columns) == list:
        if len(columns) < 1:
            raise Exception("Sorry, the list of columns to cast is empty") 
        cols = data_df.columns[columns].tolist()
        dict_dtypes = {col:str for col in cols}
    else:
        if type(columns) != int:
            raise Exception("Sorry, the type of the column name must be the position in the dataframe")
        col = data_df.columns[columns]
        dict_dtypes = {col:str}
    
    #dict_dtypes = {col:str for col in columns}
    tr_df = data_df.astype(dict_dtypes)
    logger.debug(f'dict_types:{dict_dtypes}')
    return tr_df

def merge_dataset(df1, df2, df1_key, df2_key)->pd.DataFrame:
    '''
    Left Join of 2 dataframes on df1_key and df2_key 
    Input
    -------------
    df1  The left dataframe 
    df2  The right dataframe
    df1_key   int of list of ints to be used as join key
    df2_key   int of list of ints to be used as join key
    
    Returns
    -------------
    A merged dataframe 
    '''
    logger.debug('Start merging')
    key_column1 = df1.columns[df1_key].tolist()
    key_column2 = df2.columns[df2_key].tolist()
    logger.debug(f'df1:{df1.shape}, df2:{df2.shape}. Keys columns: {key_column1}, {key_column2}')

  #  if df1[key_column1].dtypes != df2[key_column2].dtypes:
  #      raise TypeError("Different dtypes of keys used to merge") 
    
    merged_df = pd.merge(df1, df2, left_on=key_column1, right_on=key_column2, how='left', suffixes=(None,"_y"))
    merged_df.drop(labels=key_column2, axis=1, inplace=True)
    return merged_df

def _create_sparse_ingredients(ing_df, key_columns
                             ,pivot_column, value_columns)->pd.DataFrame:
    #1st, replace values of Score_unique_EF with 1 
    subset_ingred = ing_df.loc[:,['Ciqual_AGB', 'Nom_Francais', 'Groupe_aliment', 'Sous-groupe_aliment', 'LCI_Name' , 'Ingredients', 'Score_unique_EF_']]
    subset_ingred.loc[subset_ingred['Score_unique_EF_'] > 0, 'Score_unique_EF_'] = 1
    drop_cols = ['Nom_Francais', 'Groupe_aliment', 'Sous-groupe_aliment', 'LCI_Name'] 
    subset_ingred = subset_ingred.fillna(0)
    subset_ingred['Score_unique_EF_'] = subset_ingred['Score_unique_EF_'].astype(np.int16)
    # pivot the dataframe to have ingredients in columns axis
    pivot_subset_ingred = pd.pivot(subset_ingred, index=['Ciqual_AGB', 'Nom_Francais', 'Groupe_aliment', 'Sous-groupe_aliment', 'LCI_Name'], \
                               columns='Ingredients', values='Score_unique_EF_').reset_index()
    pivot_subset_ingred = pivot_subset_ingred.rename_axis(None, axis=1)
    numeric_cols = pivot_subset_ingred.select_dtypes(include=np.number).columns
    pivot_subset_ingred = pivot_subset_ingred.fillna(0)
    pivot_subset_ingred[numeric_cols] = pivot_subset_ingred[numeric_cols].astype(int)
    pivot_subset_ingred=pivot_subset_ingred.drop(columns=drop_cols)
    return pivot_subset_ingred

def _create_features_min_max_ing(ing_df, key_columns, pivot_column, value_columns)->pd.DataFrame:
    
    pivot_index = ['Ciqual_AGB', 'Nom_Francais', 'Groupe_aliment', 'Sous-groupe_aliment', 'LCI_Name']
    pivot_columns = ['Ingredients']
    pivot_values = ['min_EF', 'max_EF']
    drop_cols = ['Nom_Francais', 'Groupe_aliment', 'Sous-groupe_aliment', 'LCI_Name'] 

    pivot_ing_minmax = pd.pivot(data=ing_df, index=pivot_index, columns=pivot_columns, values=pivot_values,).reset_index()
    new_col_index = [f'{multiindex[0]}_{multiindex[1]}' if multiindex[1]!='' else multiindex[0] for multiindex in pivot_ing_minmax.columns]
    pivot_ing_minmax.columns=new_col_index
    pivot_ing_minmax = pivot_ing_minmax.fillna(0)
    pivot_ing_minmax = pivot_ing_minmax.drop(columns=drop_cols)
    return pivot_ing_minmax

    #pd.concat([ing_pivot_df, subset_ingred], axis=1, join='inner')

def pivot_ingredients(data_df, make_one_hot=True, add_features=True):
    pivot_index = ['Ciqual_AGB', 'Nom_Francais', 'Groupe_aliment', 'Sous-groupe_aliment', 'LCI_Name']
    pivot_columns = ['Ingredients']
    pivot_values = ['Score_unique_EF_','min_EF', 'max_EF']
    
    #ing_pivot_df = pd.pivot(data=data_df, index=pivot_index, columns=pivot_columns)\
    #    .reset_index().rename_axis(None, axis=1)

    ing_pivot_df = pd.pivot(data=data_df, index=pivot_index, columns=pivot_columns, values=pivot_values,).reset_index()
    #Create new index column names
    new_col_index = [f'{multiindex[0]}_{multiindex[1]}' if multiindex[1]!='' else multiindex[0] for multiindex in ing_pivot_df.columns]
    new_col_index
    ing_pivot_df.columns=new_col_index    
   
    ing_pivot_df.fillna(0, inplace=True)
    num_columns = ing_pivot_df.select_dtypes(include=np.number).columns
    if make_one_hot: #If values should be only 0 and 1
        for c in num_columns:
            index_ones = ing_pivot_df[c] > 0
            ing_pivot_df.loc[index_ones, c] = 1

    drop_labels = ['Nom_Francais', 'Groupe_aliment', 'Sous-groupe_aliment', 'LCI_Name']#index_column[1:]
    ing_pivot_df.drop(labels=drop_labels, axis=1, inplace=True)
    return ing_pivot_df

def load_dataset(input_filepath:str, file_name):
    #file_name = 'Agribalyse_Synthese.csv'
    data_df = pd.read_csv(os.path.join(input_filepath,file_name))
    return data_df

def preprocess_dataset(file_name: str, input_filepath, output_filepath, index_key:int, format_column_names=True):
    '''
    Reads a file, then changes the column names by removing spaces and removing some text that is between "( )"
    Parameters:
    ----------------------
    file_name: 
        A file name
    input_filepath: 
        The path where the file_name can be found
    output_filepath: 
        The path where the new file is saved, with the same name than file_name
    index_key:
         An int or list of ints representing the primary key of the dataset
    format_column_names:
      If True, then the column names will change to have  more readable and short column names
                        If False, the names will be kept as the original dataset
    '''
    logger.debug(f'Input parameters:{file_name}, {input_filepath}, {output_filepath}, {index_key}, {format_column_names}')
    logger.info(f'Preprocessing dataset {input_filepath}/{file_name}')

    data_df = load_dataset(input_filepath, file_name)
    if format_column_names:
        data_df = change_column_names(data_df)

    #Change the primary key to type 'str' (because later it will be used for merge and the tables primary keys must have the same type)
    if type(index_key) is int:
        key = index_key
    elif type(index_key) is list or type(index_key) is box.BoxList:
        key = data_df.columns[index_key].to_list()
    else:
        raise TypeError(f'The index_key type should be an integer number of a list of integer numbers. Current type {type(index_key)}')
    data_df = cast_dtype_to_str(data_df, index_key)
    logger.debug(f'Dataset preprocessed from {input_filepath}/{file_name}')
    
    return data_df

def _transform_column_names(input_filepath, output_filepath):
    dfs = dict()
    for param_key, param_value in params.items():# For every table in the parameters
        file_name = param_value.file_name#get_param(dataset_name,'file_name')
        keep_columns = param_value.keep_cols.to_list()# get_param(param_key, 'keep_cols')
        key = param_value.index_key.to_list()#get_param(dataset_name, 'index_key')
        logger.debug(f'{param_key} before transforming column names')
        dfs[param_key]=preprocess_dataset(file_name, input_filepath, output_filepath, key).iloc[:, keep_columns]
    return dfs

def _get_describe_ingredients(orig_ing_df):
    desc_ingred_df = orig_ing_df.groupby('Ingredients')['Score_unique_EF_'].describe()[['min', 'max']].reset_index()
    desc_ingred_df.columns=['Ingredients', 'min_EF', 'max_EF']
    return desc_ingred_df

def _create_canonical(ingred_df):
    base_df = ingred_df.iloc[0:1, 13:]#Hard coded. TODO Parameterize
    for col in base_df.columns[:213]:#TODO 213 ingredients hard coded. The rest are extra features
        base_df[col].values[:] = 0
    return base_df

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger.info('Preprocessing datasets from raw data')    
    key_columns = ['Ciqual_AGB', 'Nom_Francais', 'Groupe_aliment', 'Sous-groupe_aliment', 'LCI_Name' , 'Ingredients']
    pivot_column = 'Ingredients'
    value_columns = 'Score_unique_EF_'

    # 1. Retrieve all files from /data/raw folder and make basic cleaning and merge
    #files = ['Agribalyse_Synthese.csv', 'Agribalyse_Detail ingredient.csv', 'Agribalyse_Detail etape.csv']
    dfs = _transform_column_names(input_filepath, output_filepath)
    
    #2. pivot ingredients dataframe
    orig_ing_df = dfs['ingredients']
    desc_ingred_df = _get_describe_ingredients(orig_ing_df)

    desc_ingred_df.to_csv(os.path.join('./../data/interim', 'Agribalyse_MinMax ingredient.csv'))
    
    ing_df = orig_ing_df.merge(desc_ingred_df, how='left', left_on='Ingredients', right_on='Ingredients') 
    
    sparse_ing_df = _create_sparse_ingredients(orig_ing_df,key_columns, pivot_column, value_columns)
    
    pivot_values = ['min_EF', 'max_EF']
    pivot_ing_minmax = _create_features_min_max_ing(ing_df, key_columns, pivot_column, pivot_values)

    drop_cols = ['Nom_Francais', 'Groupe_aliment', 'Sous-groupe_aliment', 'LCI_Name']
    #new_ing_df = pd.concat([sparse_ing_df, pivot_ing_minmax], axis=1, join='inner').drop(columns=drop_cols)
    new_ing_df = sparse_ing_df.merge(pivot_ing_minmax, how = 'inner', left_on='Ciqual_AGB', right_on="Ciqual_AGB")
    dfs['ingredients'] = new_ing_df
   
    
    #3. merge synthese vs ingredients
    synthese_key = params.synthese.index_key.to_list()#get_param('synthese', 'index_key')
    ingredients_key = params.ingredients.index_key.to_list() #get_param('ingredients', 'index_key')
    etapes_key = params.etapes.index_key.to_list()#get_param('etapes', 'index_key')
    
    #3. merge synthese vs ingredients and synthse vs etapes    
    keep_synthese_merge = []
    new_ingred_df = merge_dataset(dfs['synthese'], dfs['ingredients'], synthese_key,ingredients_key)
    new_etape_df = merge_dataset(dfs['synthese'], dfs['etapes'], synthese_key, etapes_key)

    new_ingred_df.fillna(0, inplace=True)
    new_etape_df.fillna(0, inplace=True)
    #4. Save the new datasets
    new_ingred_df.to_csv(os.path.join(output_filepath, params.ingredients.file_name), index=False)
    new_etape_df.to_csv(os.path.join(output_filepath, params.etapes.file_name), index=False)
    #5. Save extra dataframe for the format of the ingredients input 
    base_df = _create_canonical(new_ingred_df, index=False)
    base_df.to_csv(os.path.join(output_filepath,'ingredients_data_format.csv'), index=False)

    logger.info(f'End preprocessing. 3 files were created {params.ingredients.file_name,}\
            ,{params.etapes.file_name}, ingredients_data_format.csv in {output_filepath}')

if __name__ == '__main__':
    #log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    #logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
    for param_key, param_value in params.items():# For every table in the parameters
        file_name = param_value.file_name#get_param(dataset_name,'file_name')
        keep_columns = param_value.keep_cols.to_list()#get_param(dataset_name, 'keep_cols')
        key = param_value.index_key.to_list()#get_param(dataset_name, 'index_key')
        print(file_name, keep_columns, key)
        print(type(file_name), type(keep_columns), type(key))
