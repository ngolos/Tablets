import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time
import requests
import re
from streamlit_lottie import st_lottie

#from streamlit_lottie import st_lottie_spinner
st.set_page_config(page_title="Tablets Report", page_icon="⚕️​", layout="wide")


#def load_lottieurl(url: str):
#    r = requests.get(url)
#    if r.status_code != 200:
#        return None
#    return r.json()



#file_url = 'https://assets2.lottiefiles.com/packages/lf20_v7nRH3.json'
#lottie_dog = load_lottieurl(file_url)
#st_lottie(lottie_dog, speed=1, height=150, key="initial")




#st.markdown("<h1 style='text-align: center; color: red;'>Tablets Report</h1>", unsafe_allow_html=True)

#st.markdown("<p style='text-align: center; color: black;'>This interactive report is created as an example of explatory sales data analysis report for Amazon's Categories.</p>", unsafe_allow_html=True)





st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

func_csv = "https://raw.githubusercontent.com/ngolos/Tablets/main/functions.csv"
tablets_csv = "https://raw.githubusercontent.com/ngolos/Tablets/main/tablets_all.csv"
ingredients_csv = "https://raw.githubusercontent.com/ngolos/Tablets/main/ingredients.csv"

@st.cache
def get_data(url):

    #df = pd.read_csv(url_csv, keep_default_na=False)
    df=pd.read_csv(url, keep_default_na=False)
    #ingr_df=pd.read_csv(ingredients_csv, keep_default_na=False)
    #df=pd.read_csv(tablets_csv, keep_default_na=False)
    #df[["Price", "Mo. Revenue","D. Sales"]] = df[["Price", "Mo. Revenue","D. Sales"]].apply(pd.to_numeric)
    #df['Mo_Revenue_Mln']=(df['Mo. Revenue']/1000000).round(4)
    #df['Mo. Revenue'] = df['Mo. Revenue'].astype(str).astype(float, errors='ignore')
    #df['Sales_Mln'] = (df['Sales_Mln']).round(2)
    return df


st.title('Tablets Report')
"""
- Part 1: Overall view - Top Ingredients, Top Brands.
- Part 2: function based view.
- Part 3: could be google trends, etc.
- All the data is based on May_November'2021 Amazon BSL in Dietaty Supplements Category.
"""
st.write("---")
functions=get_data("https://raw.githubusercontent.com/ngolos/Tablets/main/functions.csv")
ingredients=get_data("https://raw.githubusercontent.com/ngolos/Tablets/main/ingredients1.csv")
tablets_all=get_data("https://raw.githubusercontent.com/ngolos/Tablets/main/tablets_all.csv")
ingredients_all=get_data("https://raw.githubusercontent.com/ngolos/Tablets/main/ingredients_all_.csv")
top_brands=get_data("https://raw.githubusercontent.com/ngolos/Tablets/main/top_brands.csv")
# Filters
#st.sidebar.header('User Input Features')
#product_choice = []

#product_type = df['Sup_Type'].drop_duplicates()
#product_choice = st.sidebar.multiselect('Select product form:', options=sorted(product_type), default='Capsules')

#category list
#function_type=['Beauty', 'Body', 'Brain', 'Digest', 'Energy', 'Fitness', 'Immune', 'Joints', 'Multi', 'Stress_Sleep','Weight_Mngm' ]
#function_choice = st.sidebar.selectbox('Select functionality:', function_type)
function_type=['Beauty', 'Body', 'Brain', 'Digest', 'Energy', 'Fitness', 'Immune', 'Joints', 'Stress_Sleep','Weight_Mngm' ]
function_choice = st.sidebar.selectbox('Select functionality:', function_type)
#month_list
month=['nov', 'oct', 'sep', 'aug', 'jul', 'jun', 'may']
month_choice = st.sidebar.selectbox('Select month:', month)


pattern=f"Mo_Revenue_{month_choice}"
#st.dataframe(tablets_all)
Revenue_All=(tablets_all[pattern].astype(str).replace("",0).astype(float, errors='ignore').fillna(0).sum())/1000000
Rev_All=Revenue_All.round(2)
st.header(f"Tablets Overall: {month_choice}'21 Monthly Sales Est:$ {Rev_All} Mln")
#st.subheader(f'{Revenue_All}')
top=ingredients_all.nlargest(20,month_choice).round(1)

bars = alt.Chart(top).mark_bar().encode(
    x=alt.X(month_choice, title="Sales Estimates, mln$"),
    y=alt.Y("ingr:O", sort='-x', title=""),
)

text = bars.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text=month_choice
)

ingr_chart=(bars + text).properties(height=300)

#functions_chart
functions=functions.round(1)
bars_f = alt.Chart(functions).mark_bar().encode(
    x=alt.X(month_choice, title="Sales Estimates, mln$"),
    y=alt.Y("function:O", sort='-x', title=""),
)

text_f = bars_f.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text=month_choice
)

funct_chart=(bars_f + text_f).properties(height=300)

#top_brands chart

ss=top_brands.nlargest(15,month_choice).round(1)
bars_brands = alt.Chart(ss).mark_bar().encode(
    x=alt.X(month_choice, title="Sales Estimates, mln$"),
    y=alt.Y("Brand:O", sort='-x', title=""),
)

text_brands = bars_brands.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text=month_choice
)

brand_chart=(bars_brands + text_brands).properties(height=300)


col01, col02, col03, col04, col05, col06 = st.columns([3,1,3,1,3,1])
with col01:
    #col1.metric(label="Dogs", value="%.2f" % total_sales_dogs)
    st.subheader(f"Top 20 Ingredients in {month_choice}'21")
    st.altair_chart(ingr_chart)
with col03:
    #col1.metric(label="Dogs", value="%.2f" % total_sales_dogs)
    st.subheader(f"Functions in {month_choice}'21")
    st.altair_chart(funct_chart)
#st.altair_chart(ingr_chart, use_container_width=True)
#functions list
with col05:
#    #col1.metric(label="Dogs", value="%.2f" % total_sales_dogs)
    st.subheader(f"Top Brands {month_choice}'21")
    st.altair_chart(brand_chart)

#function_type=['Beauty', 'Body', 'Brain', 'Digest', 'Energy', 'Fitness', 'Immune', 'Joints', 'Stress_Sleep','Weight_Mngm' ]
st.dataframe(top_brands)

filtered_df = ingredients.loc[ingredients['function']==function_choice].nlargest(15, month_choice)
filtered_df1 = ingredients.loc[ingredients['function']==function_choice]

##prepare df for ranks
filtered_df1['may_rank'] = filtered_df1['may'].rank(ascending=False)
filtered_df1['jun_rank'] = filtered_df1['jun'].rank(ascending=False)
filtered_df1['jul_rank'] = filtered_df1['jul'].rank(ascending=False)
filtered_df1['aug_rank'] = filtered_df1['aug'].rank(ascending=False)
filtered_df1['sep_rank'] = filtered_df1['sep'].rank(ascending=False)
filtered_df1['oct_rank'] = filtered_df1['oct'].rank(ascending=False)
filtered_df1['nov_rank'] = filtered_df1['nov'].rank(ascending=False)
filtered_df1=filtered_df1.sort_values(by='nov_rank').head(10)
cols=['ingr','may_rank', 'jun_rank', 'jul_rank', 'aug_rank', 'sep_rank', 'oct_rank','nov_rank']

df=filtered_df1.filter(items=cols).transpose()
df.columns = df.iloc[0]
df = df.iloc[1:11].reset_index()
#df=df.head(10) #if i want to show top 10 ingredients
source=pd.melt(frame=df, id_vars='index', var_name='Ingredient', value_name='rank')
source['index']=source['index'].str.replace('_rank', '')

#df[df['Type'].isin(target_choice)]
#["Mo_Revenue_Mln"].sum().round(2)

chart=alt.Chart(filtered_df).mark_bar().encode(
    y=alt.Y('ingr:N', sort='-x', title=""),
    x=alt.X(month_choice, title="Sales Estimates, mln$")
    #color=alt.Color('Type:N',scale=alt.Scale(domain=domain, range=range)),
    #color='Type:N',
    #tooltip=['Sales_Mln', 'Sup_Type', 'Active Ingredient'],
    #column="Sup_Type"
)

categoryNames=['may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov']

chart2=alt.Chart(source).mark_line(point = True).encode(
    x = alt.X("index:N", title="", sort=categoryNames, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("rank",scale=alt.Scale(domain=[12,0]),axis=alt.Axis(tickCount=10)),
    color=alt.Color("Ingredient:N"),
    tooltip=['Ingredient', 'rank']
).interactive()


#st.dataframe(source)

st.write("---")
st.header('Category by Functionality')

col1, col2, col3, col4 = st.columns([3,1,3,3])
with col1:
    #col1.metric(label="Dogs", value="%.2f" % total_sales_dogs)
    st.subheader(f"{function_choice}:Top 10 Ingredients in {month_choice}")
    st.altair_chart(chart)
with col3:
    #col1.metric(label="Dogs", value="%.2f" % total_sales_dogs)
    st.subheader(f"{function_choice}:Rank of Top 10 Ingredients")
    st.altair_chart(chart2, use_container_width=True)
