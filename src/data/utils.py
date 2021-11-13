import pandas as pd
import os

def load_dataset(input_filepath:str, file_name):
    #file_name = 'Agribalyse_Synthese.csv'
    data_df = pd.read_csv(os.path.join(input_filepath,file_name))
    return data_df



