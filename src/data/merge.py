import pandas as pd

def merge_datasets(df1, df2, df3, df1_key, df2_key, df3_key, d2_keep, d3_keep)->pd.DataFrame:
    #d2_keep = [0, *range(6,22)] # * allows to unravel the range
    merged_df = pd.merge(df1, df2.iloc[:, d2_keep], left_on=df1_key, right_on=df2_key, how='inner')
    merged_df = pd.merge(merged_df, df3.iloc[:, d3_keep], left_on=df1_key, right_on=df3_key, how='inner')

    return merged_df