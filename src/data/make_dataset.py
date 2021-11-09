# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv
import preprocessing

def load_dataset(input_filepath:str, file_name):
    #file_name = 'Agribalyse_Synthese.csv'
    data_df = pd.read_csv(os.path.join(input_filepath,file_name))
    return data_df

def basic_clean(data_df:pd.DataFrame):
    tr_df = data_df.pipe(preprocessing.strip_text_columns)
    return tr_df

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    file_name = 'Agribalyse_Synthese.csv'
    synthese_df = load_dataset(input_filepath, file_name)
    synthese_df = basic_clean(synthese_df)
    synthese_df.to_csv(os.path.join(output_filepath,file_name))
    
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
