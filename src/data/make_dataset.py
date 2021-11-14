# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv
import preprocessing



def clean_trailing_spaces(df:pd.DataFrame)->pd.DataFrame:
    '''
    Retrieves columns of type ''object'' (string) and strips trailing spaces in their values
    '''
    index_obj_cols = df.select_dtypes(include='object').columns
    for col in index_obj_cols:
        df[col] = df[col].str.strip()
    return df

def clean_missing(df: pd.DataFrame):
    pass

def clean_duplicates(data_df:pd.DataFrame)->pd.DataFrame:
    tr_df = data_df.pipe(clean_trailing_spaces)
    return tr_df

def clean_products(data_df:pd.DataFrame)->pd.DataFrame:
    pass

def clean_all(data_df:pd.DataFrame)->pd.DataFrame:
    tr_df = data_df.pipe(clean_trailing_spaces) \
            .pipe(clean_duplicates)\
                .pipe(clean_products)
            
    return tr_df

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    
    logger = logging.getLogger(__name__)
    logger.info('Making final data set from raw data')
    file_name = ['Agribalise_Detail ingredient.csv']

    # Retrieve all files in from raw data folder and make basic cleaning
    data_df = pd.read_csv(os.path.join(input_filepath,file_name))
    data_df = clean_all(data_df)

    
    logging.info(f'Data set ready for training')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
