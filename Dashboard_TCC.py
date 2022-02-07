import dash
from dash import dcc 
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import json


SP_municipios_geo_json = json.load(open(r"municipios_tratados_geo.json", encoding="utf8")) #para o mapa
df_municipios = pd.read_csv(r"df_mapa.csv", sep=";") #para o mapa

df_gerais = pd.read_csv(r"dados_tratados_1.csv", sep=";") #para grafico box plot
df_idadeXobitos = pd.read_csv(r"dados_grafico_idadeXobito.csv", sep=";") #para correlação idade avançada e óbito
df_comorbidades = pd.read_csv(r"df_comorbidades_graficos_barras.csv", sep=";") #para graficos de barras comorbidades



############################################
#           Instância do Dash              #
############################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig = px.choropleth_mapbox(df_municipios,
                           locations="Municipio",
                           color="percent_obitos",
                           geojson=SP_municipios_geo_json,
                           center={"lat":-22.248519, "lon":-48.254707},
                           zoom=5.6,
                           color_continuous_scale="Redor",
                           opacity=0.4 )

fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)
fig.show()


#1 grafico de pizza para mostrar a baixa ocorrência de obitos
labels = "Recuperados", "Óbito"
sizes = df_gerais["Obito"].value_counts()
fig1 = go.Figure(layout={"template": "plotly_dark"})
fig1 = px.pie(df_gerais, values=sizes, names=labels, title="Resultados dos casos na amostra",)
fig1.update_traces(textposition='inside', textinfo='percent+label')
fig1.update_layout(
    showlegend=False,
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=50, r=50, t=50, b=50),
    template="plotly_dark",
    title_x=0.5
)
fig1.show()


#2 grafico box separando homens e mulheres   marker_color="rgb(7,40,89)"
fig2 = px.box(df_gerais, x="Obito", y="Idade", color="Genero", title="Distribuição da idade nos casos de óbitos e recuperados")
fig2.show()
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=50, r=50, t=50, b=50),
    template="plotly_dark"
)

#3 graficos de pontos para mostrar a correlação da idade avançada e obitos
fig3 = px.scatter(df_idadeXobitos, x="Idade", y="Qtd_Obitos", trendline="ols", title="Quantidade de óbitos para cada idade")
fig3.show()
fig3.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=50, r=50, t=50, b=50),
    template="plotly_dark",
    title_x=0.5
)

#4 
fig4 = px.scatter(df_idadeXobitos, x="Idade", y="Percentual_Obitos", trendline="ols", title="Porcentagem de óbitos para cada idade")
fig4.show()
fig4.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=50, r=50, t=50, b=50),
    template="plotly_dark", 
    title_x=0.5
)

#5 grafico de barras empilhadas count
fig5 = go.Figure(data=[
    go.Bar(name="Recuperados", x=df_comorbidades["Comorbidade"], y=df_comorbidades["Count_Recuperados"]),
    go.Bar(name="Obitos", x=df_comorbidades["Comorbidade"], y=df_comorbidades["Count_Obitos"])
])
fig5.update_layout(barmode="stack")
fig5.show()
fig5.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=50, r=50, t=50, b=50),
    template="plotly_dark",
    title_text="Quantidade de casos para cada comorbidade",
    title_x=0.5
)

#6 grafico de barras empilhadas proportion
fig6 = go.Figure(data=[
    go.Bar(name="Recuperados", x=df_comorbidades["Comorbidade"], y=df_comorbidades["Prop_Recuperados"]),
    go.Bar(name="Obitos", x=df_comorbidades["Comorbidade"], y=df_comorbidades["Prop_Obitos"])
])
fig6.update_layout(barmode="stack")
fig6.show()
fig6.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=50, r=50, t=50, b=50),
    template="plotly_dark",
    title_text="Porcentagem de óbitos para cada comorbidade", 
    title_x=0.5
)


############################################
#                  Layout                  #
############################################

app.layout = dbc.Container(
    dbc.Row([
        html.Div([
            html.Img(id="logo", src=app.get_asset_url("puc_logo_branca.png"), height=80),
            html.H5("Impacto de Fatores de Risco em Casos Confirmados de Covid-19 no Estado de São Paulo")
        ], style={'textAlign': 'center'}),
        dbc.Col([
            dbc.Row([
                dcc.Graph(id="choroplath-map", figure=fig)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="pie-map", figure=fig1)
                ], style={"padding": "25px"}),
                dbc.Col([
                    dcc.Graph(id="box-map", figure=fig2)
                ], style={"padding": "25px"})
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="scatter-count-map", figure=fig3)
                ], style={"padding": "25px"}),
                dbc.Col([
                    dcc.Graph(id="scatter-prop-map", figure=fig4)
                ], style={"padding": "25px"})
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="stacked-count-map", figure=fig5)
                ], style={"padding": "25px"}),
                dbc.Col([
                    dcc.Graph(id="stacked-prop-map", figure=fig6)
                ], style={"padding": "25px"})
            ])                        
        ])

    ])
)

  

if __name__ == "__main__":    
    app.run_server(debug=False, port=8051)

