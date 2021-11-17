import streamlit as st 
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

header_container = st.container()

# pic_Agribalyse

#dataset = pd.read_csv("Agribalyse_Detail ingredient.csv")
dataset = pd.read_csv('../../data/raw/Agribalyse_Detail ingredient.csv')


with header_container:
    st.title("Agribalyse")
    

def main():
        
    
    menu = ['A propos','Home', 'About']
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == 'A propos':
        st.title("Découvrez l’impact environnemental de l'alimentation selon les indicateurs ACV")
        st.write('Agribalyse, la base de données environnementale de référence sur des produits agricoles et alimentaires')
        st.write("2500 produits, 16 indicateurs construits selon l’approche scientifique de l’Analyse de Cycle de Vie")
        st.write("Un programme collaboratif associant des scientifiques et experts des secteurs agricoles, agroalimentaires et de l’environnement")
        st.write("Un outil au service des professionnels agricoles et alimentaires, et des consommateurs") 
        st.write("**Découvrer le jeu de données.**")
        if st.checkbox('Afficher les données'):
            st.write(dataset)
        
    elif choice == 'Home':
        st.subheader("L'impact de votre assiette sur l'environnement")
        data = dataset[["Nom Français","Ingredients","Score unique EF (mPt/kg de produit)"]]
        selection = data['Nom Français'].drop_duplicates()
        #make_selection = st.selectbox('Selectionner un plat', selection)  
        
        DEFAULT = ' -Click Me  ...   👈'
        def selectbox_with_default(text, values, default=DEFAULT, sidebar=False):
            func = st.sidebar.selectbox if sidebar else st.selectbox
            return func(text, np.insert(np.array(values, object), 0, default))

        make_selection = selectbox_with_default('Commence par choisir ton plat ...', selection)
        if make_selection == DEFAULT:
            st.warning("**- Selectionner un plat -**")
            #raise StopException
        
        st.write("**Les ingredients et l'impact envirronement de votre plat : **")
        ingredient = data[data['Nom Français'].isin([make_selection])]
        ingredient = ingredient[['Ingredients', 'Score unique EF (mPt/kg de produit)']]
        st.write(ingredient)
        st.subheader('') 
        st.write("**Pourcentage des ingrédients dans le score environnementale **")
        fig = px.pie(ingredient, values='Score unique EF (mPt/kg de produit)', names='Ingredients')
        st.plotly_chart(fig)
        
        

    
    else:
        st.subheader('About')#
    

if __name__ == '__main__':
    main()    
