# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv
import preprocessing

def synthese_keep_columns():
    keep_cols = [i for i in range(27)]
    return keep_cols

def ingredients_keep_columns():
    keep_cols = [0, *range(6, 22)]
    return keep_cols

def etapes_keep_columns():
    keep_cols = [0, *range(6, 102)]
    return keep_cols


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    
    logger = logging.getLogger(__name__)
    logger.info('Making final data set from raw data')
    
    # Retrieve all files in from raw data folder and make basic cleaning
    agribalise_df = pd.read_csv(os.path.join(input_filepath,'Agribalyse.csv'))
    
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
