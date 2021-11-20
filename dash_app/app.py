import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
#import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Computing a recipe to see if this would work out on Dash viz
df = pd.read_csv("/Users/reffet/Desktop/Jedha Formation/Projets /agribalyse/data/raw/Agribalyse_Detail ingredient.csv")
df_25163 = df[df['Ciqual code'] == 25163]

fig = px.pie(df_25163, values='Score unique EF (mPt/kg de produit)', names='Ingredients',
             title='Boulettes de boeuf cuite')#,
             #hover_data=['lifeExp'], labels={'lifeExp':'life expectancy'})
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])


app.run_server(debug=True)