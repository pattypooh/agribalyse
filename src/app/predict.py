
from src.models import predict_model

def transform_ing_dataframe(ingredients):
    dataframe=pd.DataFrame()
    return dataframe

def predict_score(ingredients_user):
    score = 1
    df_213_ing = transform_ing_dataframe()
    
    score = predict_model(df_213_ing)
    
    return score

