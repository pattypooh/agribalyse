import streamlit as st 
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
#We import the necessary function to an active ingredient filter
from predict import ingredient_to_dataframe
import os
import predict



print(os.curdir)
dataset = pd.read_csv('./../data/raw/Agribalyse_Detail ingredient.csv')
ingredients_list = dataset['Ingredients'].drop_duplicates().sort_values(ascending=True)
 

def main():    
    menu = ['A propos','A vos calculs', 'A propos de nous']
    #choice = st.sidebar.selectbox("Menu", menu)
    choice = st.sidebar.radio('Select a page:',menu)
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
        
    elif choice == 'A vos calculs':
        st.subheader("**Les ingrédients les plus polluants selon l'indice environnemental PEF** ")
        st.markdown("*_Product Environmental Footprint_")
        #st.write("🍖 🥩 🍔 La **viande** rouge ? ")
        #st.write("🍳 🍼 🥛 Les **protéines** animales ?")
        #st.write("🥭 🥑 🍆 Les produits **hors saison** ? ")
        st.write("")
        st.write("")
        st.markdown("🍟 🌮 🥓 " "🍳 🍼 🥛" "🥭 🥑 🍆")
        score_ingredient = dataset.groupby("Ingredients")["Score unique EF (mPt/kg de produit)"].mean().reset_index()
        #score_ingredient.rename(columns = {'Score unique EF (mPt/kg de produit)':'Empreinte écologique'})
        score_ingredient = score_ingredient.sort_values('Score unique EF (mPt/kg de produit)', ascending=False)
        score_ingredient.rename(columns = {'Score unique EF (mPt/kg de produit)':'Score EF par kg de produit'}, inplace=True)
        st.dataframe(score_ingredient)
        
        st.write("")
        st.write("")
        
        st.subheader("**🎯🎯 A vous de jouer 🎯🎯**")
        st.write("")
        st.markdown("Vous pouvez choisir de calculer l'impact d'un plat ou de sélectionner des ingrédients.")
        st.subheader("🎯 Quel sera le Score environnemental PEF de votre plat ?")
        st.write("")
        st.write("")

        data = dataset[["Nom Français","Ingredients","Score unique EF (mPt/kg de produit)"]]
        selection = data['Nom Français'].drop_duplicates()  
        

        DEFAULT = ' -Click Me  ...   👈'
        def selectbox_with_default(text, values, default=DEFAULT, sidebar=False):
            func = st.sidebar.selectbox if sidebar else st.selectbox
            return func(text, np.insert(np.array(values, object), 0, default))

        make_selection = selectbox_with_default('------ Choisissez un plat', selection)
        #if make_selection == DEFAULT:
            #st.warning("**- ⬆ Sélectionnez votre plat ⬆ -**")
            #raise StopException
        st.write("")
        button_sent = st.button("👌  Voir le score environnemental")
        if button_sent:
            st.success("**Le score de votre plat est de : **")
            #st.write("**Les ingrédients et l'impact environnement de votre plat : **")
            ingredient = data[data['Nom Français'].isin([make_selection])]
            #st.write("le score de ton plat est de : ")
            total = round(ingredient["Score unique EF (mPt/kg de produit)"].sum(),2)
            ingredient = ingredient[['Ingredients', 'Score unique EF (mPt/kg de produit)']]
            st.write({f"{total} mPt par kg de produit"})
            st.write("*les ingrédients de votre plat : *")
            st.write(ingredient)
            st.subheader('') 
            #st.write("**Pourcentage des ingrédients dans le score environnemental**")
            fig = px.pie(ingredient, values='Score unique EF (mPt/kg de produit)', names='Ingredients')
            st.plotly_chart(fig)
        
        st.write("")
        st.write("")
        st.write("")

        st.subheader("🎯 Choisissez vos ingrédients pour évaluer l'impact sur l'environnement")
        

        multiselection = ingredients_list
          # supression de l'ingredient Autres étapes
        multiselection = multiselection.drop([4])
        options = st.multiselect('------ Choisisez des ingrédients', multiselection)
        st.write("")
        button_sent = st.button("👌  Valider les ingrédients")
        if button_sent:
            st.write("🥬🥦🍇   🦑🍖🥩")
            st.write("Vos Ingrédients ... :", options)
            #st.write("Résultat", ingredient_to_dataframe(multiselection,options))
            score = st.write("Résultat", predict.predict_score(options))
            st.write(score)
     
    else:
        st.header('Promo dsmpt-paris-06')
        st.write()
        st.write()

        st.write("Aura MORENOVEGA")
        st.write("Malika BERREHAIL")
        st.write("Patricia ESCALERA")
        st.write("Anatole REFLET")
        
        st.markdown("Retrouvez notre code dur github :")
        url2 = 'https://github.com/pattypooh/agribalyse'
        st.markdown(url2, unsafe_allow_html=True)
        
        
    

if __name__ == '__main__':
    main()    
