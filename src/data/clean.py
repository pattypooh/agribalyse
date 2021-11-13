import pandas as pd

def strip_text_columns(df:pd.DataFrame)->pd.DataFrame:
    '''
    Retrieves columns of type ''object'' (string) and strips trailing spaces in their values
    '''
    index_obj_cols = df.select_dtypes(include='object').columns
    for col in index_obj_cols:
        df[col] = df[col].str.strip()
    return df
def clean_column_types(df: pd.DataFrame):
    pass

def clean_missing(df: pd.DataFrame):
    pass


def clean_duplicates(data_df:pd.DataFrame)->pd.DataFrame:
    tr_df = data_df.pipe(strip_text_columns)
    return tr_df


def clean_str_values(data_df:pd.DataFrame)->pd.DataFrame:
    tr_df = data_df.pipe(strip_text_columns) \
            .pipe(clean_duplicates)
            
    return tr_df

def hello():
    print("Hello agriworld")