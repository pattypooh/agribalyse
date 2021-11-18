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
        
        st.write("Depuis 2013, AGRIBALYSE® est un programme collectif et innovant qui met à disposition des données de référence sur les impacts environnementaux des produits agricoles et alimentaires à travers une base de données construite selon la méthodologie des Analyses du Cycle de Vie (ACV).")
        st.write("La méthode de l’Analyse du Cycle de Vie est une méthode reconnue et utilisée à l’échelle internationale par la communauté scientifique, les acteurs privés et les pouvoirs politiques.")
        st.write("L'ACV est une méthode de quantification des impacts d’un produit sur l’environnement tout au long de son cycle de vie (ex : agriculture, transport, emballage etc.). En plus d'être une méthode prenant en compte toutes les étapes du cycle de vie d'un produit, cette méthode prend en compte plusieurs grands enjeux environnementaux (changement climatique, qualité de l’eau, qualité de l’air, impact sur les sols…) et pas seulement le climat.")
        
        url = 'https://agribalyse.ademe.fr/'
        st.markdown(url, unsafe_allow_html=True)
        
        
        st.subheader("Découvrez l’impact environnemental de l'alimentation selon les indicateurs ACV")
        st.write('Agribalyse met à disposition une base de données environnementale de référence sur des produits agricoles et alimentaires')
        st.write("2500 produits, 16 indicateurs construits selon l’approche scientifique de l’Analyse de Cycle de Vie")
        st.write("Un programme collaboratif associant des scientifiques et experts des secteurs agricoles, agroalimentaires et de l’environnement")
        st.write("Un outil au service des professionnels agricoles et alimentaires, et des consommateurs") 
        st.write("**Découvrer le jeu de données **")
        if st.checkbox('Afficher les données'):
            st.write(dataset)
        
    elif choice == 'Home':
        st.write("**Quels sont les aliments avec la plus grosse empreinte carbone ? 😒 😒**")
        st.write("🍖 La **viande rouge** 🥩 🍔 ? ")
        st.write("🍳 Les **protéines animales** 🍼 🥛?")
        st.write("🥭 Les produits **hors saison** 🥑 🍆? ")
        st.write("🛩️ Le bio a-t-il une meilleure empreinte carbone que le non bio ⛴️  ✈️? ")
        st.write("")

        st.subheader("L'impact de votre assiette sur le changement climatique (kg CO2 eq/kg de produit)")
        st.write("**14 indicateurs permettent de mesurer l'impacte de notre consommation sur l'empreinte carbonne.**")
        st.write("Quelle sera ton impacte .....")
        data = dataset[["Nom Français","Ingredients","Score unique EF (mPt/kg de produit)"]]
        selection = data['Nom Français'].drop_duplicates()

        DEFAULT = ' -Click Me  ...   👈'
        def selectbox_with_default(text, values, default=DEFAULT, sidebar=False):
            func = st.sidebar.selectbox if sidebar else st.selectbox
            return func(text, np.insert(np.array(values, object), 0, default))

        make_selection = selectbox_with_default('Commence par choisir ton plat ...', selection)
        if make_selection == DEFAULT:
            st.warning("**- ⬆ Sélectionne un plat ⬆ -**")
            #raise StopException
        
        st.write("**Les ingrédients et l'impact environnement de votre plat : **")
        ingredient = data[data['Nom Français'].isin([make_selection])]
        st.write("le score de ton plat est de : ")
        total = round(ingredient["Score unique EF (mPt/kg de produit)"].sum(),2)
        ingredient = ingredient[['Ingredients', 'Score unique EF (mPt/kg de produit)']]
        st.write({f"le score de ton plat est de {total} mPt par kg de produit"})
        st.write(ingredient)
        st.subheader('') 
        st.write("**Pourcentage des ingrédients dans le score environnemental**")
        fig = px.pie(ingredient, values='Score unique EF (mPt/kg de produit)', names='Ingredients')
        st.plotly_chart(fig)
        
        #menu déroulant Ingredient selection multiple
        st.write("**Choisit tes ingrédients et calculons le score de ... : **")
        multiselection = data['Ingredients'].drop_duplicates()
          # supression de l'ingredient Autres étapes
        multiselection = multiselection.drop([4])
        options = st.multiselect('------', multiselection)
        button_sent = st.button("Valider les ingrédients")
        if button_sent:
            st.write("🥬🥦🍇   🦑🍖🥩")
            st.write("Ingrédients choisit ... :", options)
     
   
    
    else:
        st.subheader('About')#
    

if __name__ == '__main__':
    main()    
