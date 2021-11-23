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
    menu = ['À propos','À vos calculs', 'À propos de nous']
    #choice = st.sidebar.selectbox("Menu", menu)
    st.sidebar.image("agribalyse_logo.png", use_column_width=True)
    choice = st.sidebar.radio('Select a page:',menu)
    if choice == 'À propos':
        st.subheader("Le cheminement de notre projet")
        st.write("Suite à différentes discussions de projets pouvant être intéressants et parlant à un large public, notre attention s'est portée sur un aspect méconnu des recettes de cuisine.")
        st.write("En effet l'aspect environnemental de chaque recette est souvent ignoré ou laissé de côté, en nous appuyant sur la base agribalayse nous avons trouvé un terrain d'étude qui nous semblait pertinent.")
        st.write("Notre première approche s'est tout d'abord déroulée par une exploration approfondie de la base _**Agribalyse**_.")
        st.write("")
        st.write("En effet cette base est constituée de : ")
        st.write("- x variables explicatives")
        st.write("- y variables numériques")

        st.subheader("Concernant l'approche utilisée et le processus employé")
        st.write("Nous avons opté pour un pre-processing usuel de notre donnée enlevant les variables qui n'étaient pas pertinentes à notre sens.")
        st.write("")
        st.write("Par la suite nous avons effectué une réduction de dimension avant de procéder à une sélection de nos features")
        st.write("")
        #Utilisation de quels modèles et quels sont nos résultats au global? 
        #doit-on évoquer l'aspect overfitting géré ou garde-t-on cela pour la présentation? 

        if st.checkbox('Afficher les données'):
            st.write(dataset)
        
    elif choice == 'À vos calculs':
        st.subheader("**Les ingrédients les plus polluants selon l'indice environnemental PEF** ")
        st.markdown("*_Product Environmental Footprint_")
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
        st.subheader('À propos de nous')#
        st.write("Ce projet fait partie intégrante de la formation Fullstack au sein du bootcamp Jedha")
        st.write("Notre équipe [Aura](https://github.com/aimorenov),\n[Patricia](https://github.com/pattypooh),\n[Malika](https://github.com/mbe-repo),\n[Anatole](https://github.com/anatolereffet)")
    

if __name__ == '__main__':
    main() 

#options = pd.DataFrame(options, columns="Ingredients")
            #if options["Ingredients"] == ingredient_to_dataframe['Ingredients']:
                #ingredient_to_dataframe["Presence"] = 1
