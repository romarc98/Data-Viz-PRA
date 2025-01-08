#!/usr/bin/env python
# coding: utf-8

# <div style="background-color:#e6f7ff; padding:15px; border-radius:10px;">
#     <h1 style="color:#004080;">📊 Lending Loan Database. Visualización.</h1>
#     <p> Lending Club es una plataforma estadounidense de préstamos entre particulares (P2P, peer-to-peer) que 
# conecta directamente a prestatarios con inversores. Fue fundada en 2006 con la definición de un modelo 
# de negocio innovador que permitió que personas solicitar préstamos personales sin intermediación 
# bancaria, mientras que los inversores obtenían retornos competitivos al financiar dichos préstamos.</p>
#     <p> Se visualiza un conjunto de datos históricos de préstamos emitidos por Lending Club entre los años 2007 y 2016 con los siguientes objetivos: </p>
#     <h3 style="color:#004080;">🎯 Objetivos:</h3>
#     <ul>
#     <li>Explorar relaciones/explicabilidad entre variables idiosincráticas para la gestión del riesgo de crédito (<i>Loan_amnt</i>, <i>Grade</i>, <i>Annual_inc</i>, <i>emp_length</i>, etc...) en función del estado del préstamo <i>loan_status</i></li>
#         <li> Definición y observación del "default" geográficamente. </li>
#         <li> Carácter temporal de morosidad y flujo de los préstamos (entendibilidad macro).</li>
#     </ul>
#     
#     LINK GITHUB: https://github.com/romarc98/Data-Viz-PRA
# </div>
# 
# 

# <div style="background-color:#f0f8ff; padding:10px; border-radius:10px;">
#     <h2 style="color:#004080;">🔍 Importación inicial para visualización Code-Based:
#     </h2>
# </div>

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
import sweetviz as sv
# from umap import UMAP

color_palette = px.colors.sequential.Blues[2:] 

sns.set_theme(style="whitegrid")
get_ipython().run_line_magic('matplotlib', 'inline')

# Carga de datos:
df = pd.read_csv('./loan.csv', low_memory=False)


# <div style="background-color:#f0f8ff; padding:10px; border-radius:10px;">
#     <h2 style="color:#004080;">🔍 Tratamiento del conjunto de datos:
#     </h2>
# </div>

# <div style="background-color:#004080; padding:10px; border-radius:10px;">
#         <h4 style="color: white;"> 📌 Selección del Subconjunto de datos para trabajar:
#     </h4>
# </div>

# In[2]:


# Filtrado del subconjunto de variables de interés del dataset total:
selected_columns = ['loan_amnt', 'grade', 'loan_status', 'annual_inc', 'addr_state', 'issue_d', 'emp_length']
available_columns = [col for col in selected_columns if col in df.columns]

if not available_columns:
    raise KeyError("Ninguna de las columnas seleccionadas está presente en el dataset.")

df_filtered = df[available_columns].copy()


# In[3]:


# Información general del dataset filtrado:
print("Información general del dataset:")
print(df_filtered.info())


# In[4]:


# Conversión de la variable fecha
if 'issue_d' in df_filtered.columns:
    df_filtered['issue_d'] = pd.to_datetime(df_filtered['issue_d'], format='%b-%Y', errors='coerce')


# In[5]:


# Información general del dataset filtrado:
print("Información general del dataset:")
print(df_filtered.info())


# <div style="background-color:#f0f8ff; padding:10px; border-radius:10px;">
#     <h2 style="color:#004080;">🔍 Visualización aumentada con SweetViz:
#     </h2>
# </div>

# In[6]:


#  Visualización aumentadas de las variables de interés del storytelling:
report = sv.analyze(df_filtered)
report.show_html('loan_data_sweetviz_report.html') 

print("Reporte generado: 'loan_data_sweetviz_report.html'")


# <div style="background-color:#e6f7ff; padding:15px; border-radius:10px;">
#     <h1 style="color:#004080;">🔍 Tratamiento de la variable loan_status. Concepto de Default:</h1>
#     <p> De la visualización de loan_stts (e.g. SweetViz), podemos ver como está compuesta por distintos niveles. No obstante, el evento de default es una variable que sigue una distribución binomial basada en Default/No-Default según si existen evidencias del mismo o no. 
#         
# La definición de default es amplia teniendo en cuenta la regulación, las autoridades competetes, el país... Por ello, podemos adoptar una definición ad-hoc para el ejercicio basada en juicio común:
#         
# <b>No-Default:</b> Fully Paid y Current.
#         
# <b>Default:</b>  Charged Off, Late (31-120 days), In Grace Period, Late (16-30 days), Does not meet the credit policy. Status:Fully Paid, Does not meet the credit policy. Status:Charged Off, Default
#     
# </div>

# In[7]:


main_statuses = ["Fully Paid", "Current"]
df_filtered['loan_status_grouped'] = df_filtered['loan_status'].apply(
    lambda x: "Non-Default" if x in main_statuses else "Default")

# Observación:
fig = px.bar(
    df_filtered['loan_status_grouped'].value_counts().reset_index(),
    x='index',
    y='loan_status_grouped',
    color='index',
    title="Distribución de Loan Status (Agrupado)",
    labels={"index": "Estado del préstamo", "loan_status_grouped": "Frecuencia"},
    color_discrete_map={"Non-Default": color_palette[2], "Default": color_palette[5]},
    template="simple_white",
)
fig.update_layout(
    title_font_size=20,
    xaxis_title="Estado del préstamo (Agrupado)",
    yaxis_title="Frecuencia",
    font=dict(size=14),
)
fig.show()


# <div style="background-color:#e6f7ff; padding:15px; border-radius:10px;">
#     <h1 style="color:#004080;">🔍 Relación de variables con loan Status Grouped (Marca de default)</h1>
# </div>

# <div style="background-color:#004080; padding:10px; border-radius:10px;">
#         <h4 style="color: white;"> 📌 Loan Amount:
#     </h4>
# </div>

# In[8]:


fig = px.box(
    df_filtered,
    x="loan_status_grouped",
    y="loan_amnt",
    color="loan_status_grouped",
    title="Distribución de Loan Amount por Loan Status (Agrupado)",
    labels={"loan_amnt": "Monto del préstamo ($)", "loan_status_grouped": "Estado del préstamo"},
    color_discrete_map={"Non-Default": color_palette[2], "Default": color_palette[5]},
    template="simple_white",
)
fig.update_layout(
    title_font_size=20,
    xaxis_title="Estado del préstamo (Agrupado)",
    yaxis_title="Monto del préstamo ($)",
    font=dict(size=14),
    template="simple_white",
    boxmode="group", 
)
fig.show()


# <div style="background-color:#004080; padding:10px; border-radius:10px;">
#         <h4 style="color: white;"> 📌 Grade (calificación crediticia del acreditado):
#     </h4>
# </div>

# In[9]:


# obtención de las freq. relativas y %'s de cada nivel:
df_grouped = (
    df_filtered.groupby(["grade", "loan_status_grouped"])
    .size()
    .reset_index(name="count")
)
df_grouped["percentage"] = df_grouped.groupby("grade")["count"].transform(lambda x: x / x.sum() * 100)

# stacked barplot:
fig = px.bar(
    df_grouped,
    x="grade",
    y="percentage",
    color="loan_status_grouped",
    title="Distribución de Loan Status Agrupado por Nivel de Grade (Percent Stacked)",
    labels={
        "grade": "Nivel de Grade",
        "percentage": "Porcentaje (%)",
        "loan_status_grouped": "Estado del Préstamo",
    },
    color_discrete_map={"Non-Default": color_palette[2], "Default": color_palette[5]},
    template="simple_white",
)
fig.update_layout(
    title_font_size=20,
    xaxis_title="Nivel de Grade",
    yaxis_title="Porcentaje (%)",
    font=dict(size=14),
    legend_title="Estado del Préstamo",
)
fig.show()


# <div style="background-color:#004080; padding:10px; border-radius:10px;">
#         <h4 style="color: white;"> 📌 Annual Income:
#             Tratamos la variable en términos de Outliers por el número elevado que presenta.
#     </h4>
# </div>

# In[10]:


# Criterio 1,5 * IRQ:
Q1 = df_filtered['annual_inc'].quantile(0.25)
Q3 = df_filtered['annual_inc'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filtrado:
df_no_outliers = df_filtered[(df_filtered['annual_inc'] >= lower_bound) & (df_filtered['annual_inc'] <= upper_bound)]

# Boxplot sin outliers
fig = px.box(
    df_no_outliers,
    x="loan_status_grouped",
    y="annual_inc",
    color="loan_status_grouped",
    title="Distribución de Ingresos Anuales por Loan Status (Sin Outliers)",
    labels={"annual_inc": "Ingresos Anuales ($)", "loan_status_grouped": "Estado del Préstamo"},
    color_discrete_map={"Non-Default": color_palette[2], "Default": color_palette[5]},
    template="simple_white",
)

# Personalizar el diseño
fig.update_layout(
    title_font_size=20,
    xaxis_title="Estado del préstamo (Agrupado)",
    yaxis_title="Ingresos Anuales ($)",
    font=dict(size=14),
)
fig.show()


# <div style="background-color:#004080; padding:10px; border-radius:10px;">
#         <h4 style="color: white;"> 📌Emp_Legth (longitud de historia laboral):
#     </h4>
# </div>

# In[11]:


# obtención de las freq. relativas y %'s de cada nivel:
df_grouped_2 = (
    df_filtered.groupby(["emp_length", "loan_status_grouped"]).size().reset_index(name="count")
)

df_grouped_2["percentage"] = df_grouped_2.groupby("emp_length")["count"].transform(lambda x: x / x.sum() * 100)

# gráfico de barras sin apilar (no stacked)
fig = px.bar(
    df_grouped_2,
    x="emp_length",
    y="percentage",
    color="loan_status_grouped",
    title="Distribución de Loan Status Agrupado por Nivel de Años de Empleo (No Apilado)",
    labels={
        "emp_length": "Nivel de Años de Empleo",
        "percentage": "Porcentaje (%)",
        "loan_status_grouped": "Estado del Préstamo",
    },
    color_discrete_map={"Non-Default": color_palette[2], "Default": color_palette[5]},
    template="simple_white",
)

fig.update_layout(
    title_font_size=20,
    xaxis_title="Nivel de Años de Empleo",
    yaxis_title="Porcentaje (%)",
    font=dict(size=14),
    legend_title="Estado del Préstamo",
)
fig.show()


# <div style="background-color:#e6f7ff; padding:15px; border-radius:10px;">
#     <h1 style="color:#004080;">🔍 Definición y observación del "default" geográficamente.</h1>
# </div>

# In[12]:


# Agrupación de los datos:
state_risk_grouped = df_filtered.groupby('addr_state')['loan_status_grouped'].value_counts(normalize=True).unstack().fillna(0)
state_risk_grouped['Default'] = state_risk_grouped.get('Default', 0)
state_risk_grouped['Non-Default'] = state_risk_grouped.get('Non-Default', 0)

# Winsorization al percentil 95 para viz correcta del mapa:
state_risk_grouped['Default'] = state_risk_grouped['Default'].clip(upper=state_risk_grouped['Default'].quantile(0.95))

# Mapa geográfico:
fig = px.choropleth(state_risk_grouped, 
                    geojson='https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json', 
                    locations=state_risk_grouped.index, 
                    locationmode="USA-states",
                    color='Default',
                    scope="usa",
                    title="Riesgo de Crédito por Estado (Agrupado)",
                    color_continuous_scale="RdBu_r", 
                    range_color=[0, state_risk_grouped['Default'].quantile(0.95)]) 
fig.update_geos(visible=False, resolution=110)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


# <div style="background-color:#e6f7ff; padding:15px; border-radius:10px;">
#     <h1 style="color:#004080;">🔍 Carácter temporal de morosidad y flujo de los préstamos (entendibilidad macro). </h1>
# </div>

# In[13]:


import plotly.graph_objects as go
import plotly.express as px

# nueva columna para año y mes
df_filtered['year_month'] = df_filtered['issue_d'].dt.to_period('M')

# Default Rate por mes
default_rate_by_month = df_filtered.groupby('year_month')['loan_status_grouped'].value_counts(normalize=True).unstack().fillna(0)['Default']

# Loans by month:
loan_count_by_month = df_filtered.groupby('year_month').size()

# Graficación combinada:
fig = go.Figure()

# DR:
fig.add_trace(go.Scatter(
    x=default_rate_by_month.index.astype(str),
    y=default_rate_by_month.values,
    mode='lines',
    name="Tasa de Default",
    line=dict(color='red')
))
# Loans
fig.add_trace(go.Bar(
    x=loan_count_by_month.index.astype(str),
    y=loan_count_by_month.values,
    name="Número de Préstamos",
    marker=dict(color='blue', opacity=0.6),
    yaxis='y2'
))
# Layout:
fig.update_layout(
    title="Evolución de la Tasa de Default y Número de Préstamos a lo largo del Tiempo",
    xaxis_title="Fecha de Emisión (Mes-Año)",
    yaxis_title="Tasa de Default (%)",
    yaxis2=dict(
        title="Número de Préstamos",
        overlaying="y",
        side="right",
        showgrid=False,
    ),
    font=dict(size=14),
    template="simple_white",
    legend_title="Leyenda",
    title_font_size=20,
)

fig.show()


# <div style="background-color:#e6f7ff; padding:15px; border-radius:5px;">
#     <h2 style="color:#004080;">📌 Conclusiones a partir del conjunto de datos. Observación atemporal sobre toda la ventana de datos que disponemos.</h2>
#     <ul>
#         <li> Variable Default:</li>
# 
# <ul>La agregación presenta mucha lógica para entender el evento binomial, el cual se presenta de manera esperada sobre una cartera crediticia entorno al 13%. </ul>
#         <li> Variables y default: las variables a contrastar se han escogido en base a criterio experto cualitativo, al ser de manera genérica variables core en portfolios crediticios o y/o calificaciones/grades, que son el principal elemento que diferencia el riesgo. Por ello: </li>
# <ul> Grade: existe una diferenciación coherente y marcada en la calificación del acreditado y su propensión al default. </ul>
# <ul> Los años de empleo, el salario anual y el monto del préstamo, no diferencian tan exhaustivamente el evento de default. </ul> 
#         <li> Distribución geográfica del default</li></ul> <ul> Se observa el default sobre todo el territorio de EEUU. Iowa presenta la mayor tasa, seguida por los estados del Sureste. En este punto, variables de inmigración quizás serían de interés, aunque se vulneraría uno de los principios de concesión de crédito, por lo que se mantiene al márgen cualquier consideración.  </ul> 
#         <li> Evolución temporal del default</li> <ul> Se observa  como [1] la tasa de default es muy elevada en los primeros años de Lending Club, al ser años críticos de la crisis de la vivienda que vivió el país entre 2008-2011 y [2] es precisamente a partir de 2014, cuando el negocio de préstamos se empieza a consolidar, observándose una cantidad en auge representativa de concesiones a medida que la situación macroeconómica va a mejor y tiende a estabilizarse (vemos como el default disminuye su volatilidad y se estabilida por debajo del 20% hasta caer a partir de 2016, al ser este el mejor momento del ciclo económico post crisis hasta el 2018). </ul> 
#    
# </div>
# 
