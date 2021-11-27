import streamlit as st 
import pandas as pd
#import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
#We import the necessary function to an active ingredient filter
import os
import predict

#Modifications in directory paths necessary for deployment of app in Heroku
curren_dir = os.getcwd()


#Global variables
file_name = os.path.join(curren_dir,'data/raw/Agribalyse_Detail ingredient.csv')

#Set page title and icon
st.set_page_config(page_title='Envfoodprint', page_icon = "🌳", layout = 'wide', initial_sidebar_state = 'auto')



# hide Made with Streamlit
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#title
st.header("L'empreinte environnementale de ton assiette")            

dataset = pd.read_csv(file_name)
ingredients_list = dataset['Ingredients'].drop_duplicates().sort_values(ascending=True)

DEFAULT = ' -Click Me  ...   👈'


@st.cache
def get_table_polluants():
    global dataset
    grouped_dataset = dataset.groupby("Ingredients")["Score unique EF (mPt/kg de produit)"].mean().reset_index()
    grouped_dataset = grouped_dataset.sort_values('Score unique EF (mPt/kg de produit)', ascending=False)
    #grouped_dataset.rename(columns = {'Score unique EF (mPt/kg de produit)':'Score EF par kg de produit'}, inplace=True)
    grouped_dataset = grouped_dataset.reset_index().drop('index', axis=1)
    return grouped_dataset

@st.cache
def get_table_plats():
    global dataset
    #plats_df = dataset[["Nom Français","Ingredients","Score unique EF (mPt/kg de produit)"]]
    #data['Nom Français'].drop_duplicates() 
    plats_df = dataset.drop_duplicates(subset=['Nom Français'])[['Ciqual AGB', 'Nom Français']]   
    return plats_df


def selectbox_with_default(text, values, default=DEFAULT, sidebar=False):
    func = st.sidebar.selectbox if sidebar else st.selectbox
    return func(text, np.insert(np.array(values, object), 0, default))

def _set_block_container_style(max_width_100_percent: bool = False, padding_top: int = 5, padding_right: int = 10,
                            padding_left: int = 5,padding_bottom: int = 10,):
    if max_width_100_percent:
        max_width_str = f"max-width: 100%;"
    else:
        max_width_str = f"max-width: 1200px;"
    st.markdown(f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


# Application starts here
def main():
    _set_block_container_style()
    menu = ['À propos','À vos calculs', 'À propos de nous']
    st.sidebar.image(os.path.join(curren_dir,"src/agribalyse_logo.png"), use_column_width=True)
    choice = st.sidebar.radio('Select a page:',menu)
    if choice == 'À propos':
        st.subheader("Le programme AGRIBALYSE")
        st.write('AGRIBALYSE® est un programme collectif et innovant qui met à disposition des données de référence sur les impacts environnementaux des **produits \
            agricoles et alimentaires** à travers une base de données construite selon la méthodologie des Analyse du Cycle de Vie (ACV). Source: https://doc.agribalyse.fr/documentation/')

        st.write('L\'analyse des systèmes de production de l’ensemble des aliments consommés en France métropolitaine représente un défi scientifique considérable, de par son \
                    ampleur et la complexité des systèmes de production, de transformation et de distribution, sur un marché mondialisé. \
                    La réalisation des calculs a donc nécessité de s’appuyer sur un grand nombre de données statistiques, complétées par des hypothèses et des dires d’experts.\
                        _source: Agribalyse-Guide-VF_Planche.pdf_')

        st.subheader("Le projet")
        st.write("L'idée de connaître l'impact environnementale des nos plats quotidiens nous à fortement attiré.")

        st.write('Selon la documentation, les données fournies dans la version simplifiée d’Agribalyse® – Partie Alimentation – représentent les indicateurs calculés \
                pour des produits « standards », les plus consommés en France. On trouvera ainsi par exemple l’impact d’une **pizza Margherita \
                « standard »**, constituée de  \n - tomates « standards » conventionnelles,  \n - de gruyère et de jambon standards « conventionnels »,')  
        st.write('issus des systèmes de production majoritaires aujourd’hui, et d’emballages majoritaires observés pour ce type de produit. Les impacts \
                de la « tomate standard conventionnelle » de la pizza représentent la moyenne pondérée des impacts de tomates majoritairement \
                utilisés pour les produits transformés (c’est-a dire 18 % des tomates issues de la production \
                    française, 46 % de tomates italiennes et 36 % de tomates espagnoles') 

        st.image(os.path.join(curren_dir,'src/pizza.PNG'))

        st.write("Cette base est constituée de : ")
        st.write("- 200 productions agricoles")
        st.write("- 2500 aliments prêts à être consommés")

        st.write('Il s’agit à la fois de produits agricoles (une pomme) et de produits transformés (une compote de pomme, un muffin…). Elle couvre toutes les \
                catégories de produits des principales filières consommées en France. Elle inclut ainsi les produits alimentaires produits à l’étranger et \
                importés (café, chocolat…)')

        if st.checkbox('Afficher les données'):
            st.write(dataset)
        
    elif choice == 'À vos calculs':
        st.subheader("**Les ingrédients les plus polluants selon l'indice environnemental PEF** ")
        st.markdown("*_Product Environmental Footprint_")
        st.write("")
        st.write("")
        st.markdown("🍟 🌮 🥓 " "🍳 🍼 🥛" "🥭 🥑 🍆")
        score_ingredient = get_table_polluants()
        st.markdown("L' « Eco-indicateur Point » (Pt) est un indice pondérant les 16 indicateurs, et ainsi permettre de quantifier l'impact des aliments sur la dégradation environnementale.")
        st.text("1 Pt est représentatif de l’impact environnemental annuel de 1000 habitants européens. (1 habitant pour 1 mPt)")
        
        st.dataframe(score_ingredient, width=700)

        st.write("")
        st.write("")
        
        st.subheader("**🎯🎯 A vous de jouer 🎯🎯**")
        st.write("")
        st.markdown("Vous pouvez choisir de calculer l'impact d'un plat ou de sélectionner des ingrédients.")
        st.subheader("🎯 Quel sera le Score environnemental PEF de votre plat ?")
        st.write("")
        st.write("")

        selection = get_table_plats()['Nom Français'] 

        make_selection = selectbox_with_default('------ Choisissez un plat', selection)
        #if make_selection == DEFAULT:
            #st.warning("**- ⬆ Sélectionnez votre plat ⬆ -**")
            #raise StopException
        st.write("")
        button_sent = st.button("👌  Voir le score environnemental")
        if button_sent:
            st.success("**Le score de votre plat est de : **")
            #st.write("**Les ingrédients et l'impact environnement de votre plat : **")
            ingredients = dataset[dataset['Nom Français'].isin([make_selection])]
            #st.write("le score de ton plat est de : ")
            total = round(ingredients["Score unique EF (mPt/kg de produit)"].sum(),2)
            ingredients = ingredients[['Ingredients', 'Score unique EF (mPt/kg de produit)']]
            st.write({f"{total} mPt par kg de produit"})
            st.write("*les ingrédients de votre plat : *")
            st.write(ingredients)
            st.subheader('') 
            #st.write("**Pourcentage des ingrédients dans le score environnemental**")
            fig = px.pie(ingredients, values='Score unique EF (mPt/kg de produit)', names='Ingredients')
            st.plotly_chart(fig)
        
        st.write("")
        st.write("")
        st.write("")

        st.subheader("🎯 Choisissez vos ingrédients pour évaluer l'impact sur l'environnement")
        

        multiselection = ingredients_list
        
        # supression de l'ingredient Autres étapes
        #multiselection = multiselection.drop([4])
        options = st.multiselect('------ Choisissez des ingrédients', multiselection)
        st.write("")
        button_sent = st.button("👌  Valider les ingrédients")
        if button_sent:
            st.write("🍎 🥦🍇   🦑🍖🥩")
            st.write("Vos Ingrédients ... :", options)
            #st.write("Résultat", ingredient_to_dataframe(multiselection,options))
            score_to_print = predict.predict_score(options)[0]
            st.write("Résultat. Votre plat pollue autant que {:0.2f} personnes européennes en une seule année!🌍 👨 👩 🌳".format(score_to_print))
            #st.write(score)
        
    else:
        st.subheader('À propos de nous')#
        st.write("Ce projet fait partie intégrante de la formation Fullstack au sein du bootcamp Jedha")
        st.write("Notre équipe [Aura](https://github.com/aimorenov),\n[Patricia](https://github.com/pattypooh),\n[Malika](https://github.com/mbe-repo),\n[Anatole](https://github.com/anatolereffet)")
        
main()
