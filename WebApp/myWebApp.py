from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
import plotly.graph_objects as go

# Reading the dataset and the Maps geojson
df=pd.read_csv('../Dataset/Valori.csv',sep=';',skiprows=1)

with open("../Dataset/italy-with-regions_1458.geojson") as f:
    gj = json.load(f)
features = gj['features']

with open("../Dataset/province-italia.json") as f:
    pI = json.load(f)

with open("../Dataset/limits_IT_provinces.geojson") as f:
    gprov = json.load(f)

# Used for the province map
dfPV = pd.json_normalize(pI, meta=['nome','sigla','regione'])
dfPV.drop(columns=['regione'],inplace=True)
dfPV.columns = ['name', 'Prov']
df["Prov"].fillna("NA",inplace=True)
df.loc[df["Prov"]=="FO","Prov"]="FC"
df.loc[df["Prov"]=="PS","Prov"]="PU"
df=pd.merge(df,dfPV,on='Prov')
df.drop(columns=['Prov'],inplace=True)
df = df.rename(columns={'name': 'Prov'})


# Data Exploring
# Drop Useless attributes
df.drop(['Comune_ISTAT','Comune_cat','LinkZona','Stato_prev','Comune_amm','Sup_NL_compr','Sup_NL_loc','Unnamed: 21'],axis=1,inplace=True)
df["Loc_min"] = df["Loc_min"].replace(',', '.', regex=True)
df["Loc_max"] = df["Loc_max"].replace(',', '.', regex=True)
df["Loc_min"]=df["Loc_min"].astype(float)
df["Loc_max"]=df["Loc_max"].astype(float)

df["Compr_min"]=df["Compr_min"].astype(float)
df["Compr_max"]=df["Compr_max"].astype(float)

# Substitute with 0 the Nan values
df["Compr_min"]=df["Compr_min"].fillna(0)
df["Compr_max"]=df["Compr_max"].fillna(0)

#   substitute with 0 the Nan values
df["Loc_min"]=df["Loc_min"].fillna(0)
df["Loc_max"]=df["Loc_max"].fillna(0)

# usefull update for create the map
df.loc[df["Regione"]=="VALLE D'AOSTA/VALLE`E D'AOSTE","Regione"]="VALLE D'AOSTA"
df.loc[df["Regione"]=="TRENTINO-ALTO ADIGE","Regione"]="TRENTINO-ALTO ADIGE/SUDTIROL"
df.loc[df["Regione"]=="FRIULI-VENEZIA GIULIA","Regione"]="FRIULI VENEZIA GIULIA"
df.loc[df["Comune_descrizione"]=="L`AQUILA","Comune_descrizione"]="L'AQUILA"
df.loc[df["Comune_descrizione"]=="REGGIO DI  CALABRIA","Comune_descrizione"]="REGGIO DI CALABRIA"
df.loc[df["Comune_descrizione"]=="REGGIO NELL`EMILIA","Comune_descrizione"]="REGGIO NELL'EMILIA"
dfcom=df.copy()

df.rename(columns={"Compr_max": "Compr","Loc_max": "Loc"},inplace=True)


regions=df["Regione"].unique().tolist()
# regionsMap is a list used for create the chroplet map 
regionsMap= ['Piemonte', 'Trentino-alto adige/sudtirol', 'Lombardia', 'Puglia', 'Basilicata', 
           'Friuli venezia giulia', 'Liguria', "Valle d'aosta", 'Emilia-romagna',
           'Molise', 'Lazio', 'Veneto', 'Sardegna', 'Sicilia', 'Abruzzo',
           'Calabria', 'Toscana', 'Umbria', 'Campania', 'Marche']

regions.sort()
regionsMap.sort()


### Divided by Region
dfRegion=df.groupby("Regione")[["Compr","Loc"]].mean().reset_index()
dfRegionUp=dfRegion.copy()
dfRegion["Regione"]=regionsMap


dfR=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ][["Regione","Compr","Loc"]].groupby("Regione").mean().reset_index()
dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

dfC=df[(df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23) ][["Regione","Compr","Loc"]].groupby("Regione").mean("Compr,Loc").reset_index()
dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

dfT=df[(df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18) ][["Regione","Compr","Loc"]].groupby("Regione").mean("Compr,Loc").reset_index()
dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

dfP=df[(df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10) ][["Regione","Compr","Loc"]].groupby("Regione").mean("Compr,Loc").reset_index()
dfP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)


dfTI=pd.merge(dfR,dfC,on="Regione",how="inner")
dfTI=pd.merge(dfTI,dfT,on="Regione",how="inner")
dfTI=pd.merge(dfTI,dfP,on="Regione",how="inner")

dfTI2=dfTI.copy()
dfTI2["Regione"]=regionsMap


#### DIVISO PER PROVINCIA

ListaProv=df.groupby(["Prov","Regione"]).mean("Compr,Loc").reset_index()
ListaProv=ListaProv.drop(columns=["Cod_Tip","Compr","Loc"])
ProDiv=df.groupby(["Prov","Regione"]).mean("Compr,Loc").reset_index()

dfRp=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ][["Prov","Compr","Loc"]].groupby("Prov").mean().reset_index()
dfRp.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

dfCp=df[(df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23) ][["Prov","Compr","Loc"]].groupby("Prov").mean().reset_index()
dfCp.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

dfTp=df[(df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18) ][["Prov","Compr","Loc"]].groupby("Prov").mean().reset_index()
dfTp.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

dfPp=df[(df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10) ][["Prov","Compr","Loc"]].groupby("Prov").mean().reset_index()
dfPp.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)

dfTIp=pd.merge(dfRp,dfCp,on="Prov",how="inner")
dfTIp=pd.merge(dfTIp,dfTp,on="Prov",how="inner")
dfTIp=pd.merge(dfTIp,dfPp,on="Prov",how="inner")

#####



### DIVISO PER COMUNE
ListaComm=dfcom.groupby(["Comune_descrizione","Prov","Regione"]).mean("Compr_max,Compr_min,Loc_min,Loc_max").reset_index()
ListaComm=ListaComm.drop(columns=["Compr_min","Loc_min","Compr_max","Loc_max"])

dfRc=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ][["Comune_descrizione","Regione","Prov","Compr","Loc","Compr_min","Loc_min"]].groupby(["Comune_descrizione","Prov","Regione"]).mean().reset_index()
dfRc.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

dfCc=df[(df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23) ][["Comune_descrizione","Compr","Loc","Compr_min","Loc_min"]].groupby("Comune_descrizione").mean().reset_index()
dfCc.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

dfTc=df[(df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18) ][["Comune_descrizione","Compr","Loc","Compr_min","Loc_min"]].groupby("Comune_descrizione").mean("Compr,Loc").reset_index()
dfTc.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

dfPc=df[(df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10) ][["Comune_descrizione","Compr","Loc","Compr_min","Loc_min"]].groupby("Comune_descrizione").mean("Compr,Loc").reset_index()
dfPc.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)


Commtot=dfcom.groupby(["Comune_descrizione","Prov","Regione"]).mean("Compr_max,Compr_min,Loc_min,Loc_max").reset_index()
Commtot=Commtot.drop(columns=["Cod_Tip"])
####
dfRcfasc=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ][["Comune_descrizione","Regione","Prov","Compr","Loc","Compr_min","Loc_min","Fascia"]].groupby(["Fascia","Comune_descrizione","Prov","Regione"]).mean().reset_index()
dfRcfasc.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

### Layout Dash app ##################
app = Dash(__name__)
server = app.server
app.title = 'Italy Estate'
div_style = {
    'backgroundColor': '#f2f2f2',  # Grigio
    'borderRadius': '15px',  # Bordi arrotondati
    'padding': '20px',  # Padding interno
    'font-family':'Trebuchet MS'
}


# Contenuto del div, Descrizione del Dataset
div_content = html.Div(
    [
        html.H3('Dataset OMI(Osservatorio sul mercato Immobiliare)',style={'font-family':'Trebuchet MS'}),
        html.P(["il Dataset contiene i dati relativi alle quotazioni immobiliari del secondo semestre del 2022, "
               "per ogni zona territoriale delimitata di ciascun comune ",html.Span("(Zona OMI)",style={'fontWeight': 'bold'}),
               ". Le quotazioni OMI, disponibili in un semestre, sono relative ai comuni censiti negli archivi catastali, le quotazioni OMI non possono intendersi sostitutive della stima puntuale, in quanto forniscono indicazioni di valore di larga massima"
               ". Per ogni comune ci sono diverse informazioni:",
            html.Ul([
            html.Li([html.B("Area_territoriale: "), "Area territoriale in cui si trova l'immobile"]),
            html.Li([html.Span("Regione: ",style={'fontWeight': 'bold'}),"Regione in cui si trova l'immobile"]),
            html.Li([html.Span("Prov: ",style={'fontWeight': 'bold'}),"Provincia in cui si trova l'immobile"]),
            html.Li([html.Span("Comune_ISTAT: ",style={'fontWeight': 'bold'})," Codice Istat del Comune "]),
            html.Li([html.Span("Comune_cat: ",style={'fontWeight': 'bold'}),"Codice del Comune "]),
            html.Li([html.Span("Comune_amm: ",style={'fontWeight': 'bold'}),"Codice catastale del Comune"]),
            html.Li([html.Span("Comune_descrizione: ",style={'fontWeight': 'bold'}),"Nome del Comune in cui si trova l'immobile"]),
            html.Li([html.Span("Fascia: ",style={'fontWeight': 'bold'}),"Una lettera che indica in quale fascia si trova l'immobile, tra fascia Centrale (B), Semicentrale (C), Periferica (D) , Sub Urbana (E), Extra Urbana (R)"]),
            html.Li([html.Span("Zona: ",style={'fontWeight': 'bold'}),"Identifica una zona precisa all'interno della fascia"]),
            html.Li([html.Span("Cod_Tip: ",style={'fontWeight': 'bold'}),"Codice univoco che corrisponde ad un certo tipo d'immobile"]),
            html.Li([html.Span("Descr_Tipologia: ",style={'fontWeight': 'bold'}),"Descrizione del tipo dell'immobile preso in considerazione"]),
            html.Li([html.Span("Stato: ",style={'fontWeight': 'bold'}),"Stato di conservazione dell'immobile: Normale, Ottimo e Scadente"]),
            html.Li([html.Span("Compr_max & Compr_min: ",style={'fontWeight': 'bold'}),"intervallo massimo/minimo, per unità di superficie in euro a metro quadro per l'acquisto dell'immobile"]),
            html.Li([html.Span("Sup_NL_compr: ",style={'fontWeight': 'bold'}),"Superficie Lorda (L) o Netta (N) su cui viene calcolato il costo per l'acquisto dell'immobile"]),
            html.Li([html.Span("Loc_max & Loc_min: ",style={'fontWeight': 'bold'}),"intervallo massimo/minimo, per unità di superficie in euro a metro quadro per l'affitto dell'immobile" ]),
            html.Li([html.Span("Sup_NL_loc: ",style={'fontWeight': 'bold'}),"Superficie Lorda (L) o Netta (N) su cui viene calcolato il costo per l'affitto dell'immobile"])
        ])]),
        html.P(["Per calcolare i valori  medi dei prezzi divisi per regione, provincia o comune vengono utilizzati come valori ",html.Span("Loc_max e Compr_max",style={'fontWeight': 'bold'})]),
        html.P ("Questo Dataset è disponibile nell'area riservata nel sito dell'Agenzia delle entrate, accedendo al  servizio Forniture dati OMI.")

    ],
    style=div_style
)

app.layout =html.Div([
    html.H1('Analisi prezzi degli Immobili',style={ 'text-align': 'center'}),
    html.Div(div_content),
    html.H1('Prezzi degli Immobili',style={ 'text-align': 'center'}),
    html.H1(id='Title',children='Grafico Regioni',style={ 'text-align': 'center'}),
     html.Div([
        html.Div([
            html.H2('Prezzi compravendita immobili',style={'text-align': 'center'}),
            html.H3('Seleziona il tipo di Edificio:',style={ 'text-align': 'center'}),
            dcc.RadioItems(
                id='Tipo', 
                options=[{'label': 'Tutti', 'value': 'Tutti'},
                {'label': 'Residenziale', 'value': 'R'},
                {'label': 'Commerciale', 'value': 'C'},
                {'label': 'Terziario', 'value': 'T'},
                {'label': 'Produttivo', 'value': 'P'}],
                value="Tutti",
                style={ 'text-align': 'center'},
                inline=True
            ),
            html.H2(id='Tit1',style={'text-align': 'center'}),
            dcc.Graph(id='chrop1')
        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
        html.Div([
            html.H2('Prezzi locazione immobili',style={'text-align': 'center'}),
            html.H3('Seleziona il tipo di Edificio:',style={ 'text-align': 'center'}),
            dcc.RadioItems(
                id='Tipo2', 
                options=[{'label': 'Tutti', 'value': 'Tutti'},
                {'label': 'Residenziale', 'value': 'R'},
                {'label': 'Commerciale', 'value': 'C'},
                {'label': 'Terziario', 'value': 'T'},
                {'label': 'Produttivo', 'value': 'P'}],
                value="Tutti",
                style={ 'text-align': 'center'},
                inline=True
            ),
            html.H2(id='Tit2',style={'text-align': 'center'}),
            dcc.Graph(id='chrop2')
        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}
        ),
    ], className="row"),



    html.H3("Seleziona la Regione",style={ 'text-align': 'center'}),
    dcc.Dropdown(options=regions, value='ABRUZZO', id='Reg'),
    html.H3('Seleziona il tipo di Dato:',style={ 'text-align': 'center'}),
    dcc.RadioItems(
        id='scelta', 
        options=[
        {'label': 'Compravendita', 'value': 'cmp'},
        {'label': 'Locazione', 'value': 'loc'}],
        value="cmp",
        inline=True,
        style={'text-align': 'center'}
    ),
    html.H1(id="nameProv",style={'text-align': 'center'}),
    html.Div([
        html.Div([
            html.H1('Regione',style={'text-align': 'center','marginBottom':'100px'}),
            dcc.Graph(id='graph')
        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
        html.Div([
            html.H1('Provincia',style={'text-align': 'center'}),
            dcc.Tabs(id="table-1",value="table-box",children=[
                dcc.Tab(label="Box Plot Province", value="table-box",children=[   
                    html.H2('Scegli la zona',style={'text-align': 'center'}),     
                    dcc.RadioItems(
                        id='sezP', 
                        options=[{'label':'Tutte le Zone','value':'Tutto'},
                        {'label': 'Centrale', 'value': 'B'},
                        {'label': 'Semi Centrale', 'value': 'C'},
                        {'label': 'Periferica', 'value': 'D'},
                        {'label': 'Suburbana', 'value': 'E'},
                        {'label': 'Extraurbana', 'value': 'R'}],
                        value="Tutto",
                        style={ 'text-align': 'center'},
                        inline=True
                    ),
                    dcc.Graph(id='graph3')
                ]),
                dcc.Tab(label="Mappa Province", value="table-map", children=[
                    html.H2('Scegli il tipo di Edificio',style={'text-align': 'center'}),
                    dcc.RadioItems(
                        id='TipoMapP', 
                        options=[{'label': 'Tutti', 'value': 'Tutti'},
                        {'label': 'Residenziale', 'value': 'R'},
                        {'label': 'Commerciale', 'value': 'C'},
                        {'label': 'Terziario', 'value': 'T'},
                        {'label': 'Produttivo', 'value': 'P'}],
                        value="Tutti",
                        style={ 'text-align': 'center'},
                        inline=True
                    ),
                    html.H2(id='TitP',style={'text-align': 'center'}),
                    dcc.Graph(id='mappaProv')      
                ])
            ])

        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}
        ),
    ], className="row"),
    html.H2(id="coms",children='Prezzo medio Immobili Comuni',style={'text-align': 'center'}),
    html.Div(id="graph4"),
    html.H3("Seleziona il comune",style={'text-align': 'center'}),
    dcc.Dropdown(id='CommD'),
    html.H2(id="Com",style={'text-align': 'center'}),
    dcc.Tabs(id="table-2",value="table-dot",children=[
        dcc.Tab(label="Dot Plot Comune", value="table-dot",children=[        
            dcc.Graph(id='DotP')
        ]),
        dcc.Tab(label="Box Plot Comune", value="table-box", children=[
            dcc.Graph(id='BoxP')      
        ])
    ]),
    html.H2("Distribuzione Immobili Residenziali",style={'text-align': 'center'}),
    dcc.Graph(id='Comm2')

])

############################# MAPPA  REGIONI ##############################
@app.callback(
    Output("Tit1","children"),
    Output("Tit2","children"),
    Output("chrop1", "figure"),
    Output("chrop2", "figure"),
    Input("Tipo", "value"),
    Input("Tipo2", "value"))
def display_choropleth(Tipo,Tipo2):
    dfMappa=pd.DataFrame()
    dfMappaLoc=pd.DataFrame()
    dfMappa["Regione"]=dfRegion["Regione"]
    dfMappaLoc["Regione"]=dfRegion["Regione"]

    if Tipo=="Tutti":
        Text="Tutti gli Edifici"
        dfMappa["Value"]=dfRegion["Compr"]
        
    elif Tipo=="R":
        Text="Edifici Residenziali"
        dfMappa["Value"]=dfTI2["ComprR"]

    elif Tipo=="C":
        Text="Edifici Commerciali"
        dfMappa["Value"]=dfTI2["ComprC"]
    elif Tipo=="T":
        Text="Edifici Terziari"
        dfMappa["Value"]=dfTI2["ComprT"]

    elif Tipo=="P":
        Text="Edifici Produttivi"
        dfMappa["Value"]=dfTI2["ComprP"]


    if Tipo2=="Tutti":
        Text2="Tutti gli Edifici"
        dfMappaLoc["Value"]=dfRegion["Loc"]
    elif Tipo2=="R":
        Text2="Edifici Residenziali"
        dfMappaLoc["Value"]=dfTI2["LocR"]
    elif Tipo2=="C":
        Text2="Edifici Commerciali"
        dfMappaLoc["Value"]=dfTI2["LocC"]
    elif Tipo2=="T":
        Text2="Edifici Terziari"
        dfMappaLoc["Value"]=dfTI2["LocT"]
    elif Tipo2=="P":
        Text2="Edifici Produttivi"
        dfMappaLoc["Value"]=dfTI2["LocP"]
    


    figm = go.Figure(data=go.Choropleth(
    geojson=gj, 
    z=dfMappa["Value"],
    text=dfMappa["Value"],
    locations=dfMappa["Regione"], 
    featureidkey="properties.name",
    colorscale ="Blues",
    colorbar_tickprefix = '€',
    colorbar_tickfont_color='black',
    colorbar_title = 'Prezzo Medio<br>Compr. al (m²)  €',
    colorbar_title_font_color='black',
    hovertemplate='Prezzo Medio: %{text:.2f}€ <br>%{location}' + '<extra></extra>'
    
    ))

    figmLoc = go.Figure(data=go.Choropleth(
    geojson=gj, 
    z=dfMappaLoc["Value"],
    text=dfMappaLoc["Value"],
    locations=dfMappaLoc["Regione"], 
    featureidkey="properties.name",
    colorscale ="Blues",
    colorbar_tickprefix = '€',
    colorbar_title = 'Prezzo Medio<br>Locazione al (m²) €',
    colorbar_title_font_color='black',
    colorbar_tickfont_color='black',
    hovertemplate='Prezzo Medio: %{text:.2f}€ <br>%{location}' + '<extra></extra>'
    ))
    figm.update_geos(fitbounds="locations", visible=False,center=None, projection_scale=5)
    figm.update_layout(margin={"r":0,"t":0,"l":0,"b":0},dragmode=False,font=dict(size=15,family='Trebuchet MS',color='black')),
    
    figmLoc.update_geos(fitbounds="locations", visible=False,center=None, projection_scale=5)
    figmLoc.update_layout(margin={"r":0,"t":0,"l":0,"b":0},dragmode=False,font=dict(size=15,family='Trebuchet MS',color='black'))
        
    return Text,Text2,figm,figmLoc





@app.callback(
    Output("graph", "figure"), 
    Output("graph3","figure"),
    Output("mappaProv","figure"),
    Output("CommD","options"),
    Output("CommD","value"),
    Output("nameProv","children"),
    Output("TitP","children"),
    Input("scelta","value"),
    Input("TipoMapP","value"),
    Input("Reg", "value"),
    Input("sezP","value"))
def display_BarPlot2(scelta,scletaProv,Reg,sezP):
 
    Region=Reg


    ### Fascia D
    dfFascR=df[(df["Regione"]==Reg) & ((df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ) ][["Fascia","Compr","Loc"]].groupby("Fascia").mean().reset_index()
    dfFascR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)


    dfFascC=df[(df["Regione"]==Reg) & ((df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23))  ][["Fascia","Compr","Loc"]].groupby("Fascia").mean().reset_index()
    dfFascC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

    dfFascT=df[(df["Regione"]==Reg) & ((df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18))  ][["Fascia","Compr","Loc"]].groupby("Fascia").mean().reset_index()
    dfFascT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

    dfFascP=df[(df["Regione"]==Reg) & ((df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10)) ][["Fascia","Compr","Loc"]].groupby("Fascia").mean().reset_index()
    dfFascP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)
    #pd.merge(dfRp,dfCp,on="Prov",how="inner")
    dfFascFin=pd.merge(dfFascR,dfFascC,on="Fascia",how="left")
    dfFascFin=pd.merge(dfFascFin,dfFascT,on="Fascia",how="left")
    dfFascFin=pd.merge(dfFascFin,dfFascP,on="Fascia",how="left")
    dfFascFin["Fascia"]=["Centrale","Semicentrale","Periferica","Suburbana","Extraurbana"]
    dfFascFin.fillna(0,inplace=True)
 
   
    if scelta=="cmp":    
        title="Prezzo medio Compravendita Immobili"
        fig = go.Figure(data=[
            go.Bar(name="Residenziale ",x=dfFascFin["Fascia"], y=dfFascFin["ComprR"].round(2)),
            go.Bar(name="Commerciale",x=dfFascFin["Fascia"], y=dfFascFin["ComprC"].round(2) ),
            go.Bar(name="Terziario",x=dfFascFin["Fascia"], y=dfFascFin["ComprT"].round(2) ),
            go.Bar(name="Produttivo",x=dfFascFin["Fascia"], y=dfFascFin["ComprP"].round(2) ),
            
        ])
    else:
        title="Prezzo medio Locazione Immobili"
        fig = go.Figure(data=[
            go.Bar(name="Residenziale ",x=dfFascFin["Fascia"], y=dfFascFin["LocR"].round(2) ),
            go.Bar(name="Commerciale",x=dfFascFin["Fascia"], y=dfFascFin["LocC"].round(2) ),
            go.Bar(name="Terziario",x=dfFascFin["Fascia"], y=dfFascFin["LocT"].round(2) ),
            go.Bar(name="Produttivo",x=dfFascFin["Fascia"], y=dfFascFin["LocP"].round(2)),
        
    ])  
    # Change the bar mode
    fig.update_layout(barmode='group',xaxis=dict(title='Zona di Riferimento',titlefont=dict(color='black',size=20,family='Trebuchet MS'),tickfont=dict(color='black',family='Trebuchet MS',size=15)),yaxis=dict(title='Prezzo medio al (m²)',titlefont=dict(color='black',family='Trebuchet MS',size=20),ticksuffix='€',tickfont=dict( color='black',family='Trebuchet MS',size=15)),title=title + " regione " + Region,titlefont=dict(color='black',family='Trebuchet MS',size=18))
    fig.update_traces(texttemplate='%{y:.2s}€', textposition='inside')

    List=ListaProv[ListaProv["Regione"]==Region]["Prov"].to_list()
    ListC=ListaComm[ListaComm["Regione"]==Region]["Comune_descrizione"].to_list()
    dfProv=df.query("Prov in @List")
    

    
    ### GRAFICO PROVINCIA  Prendo i dati necessari
    if sezP=="Tutto":
         
        dfR=dfProv[(dfProv["Cod_Tip"]== 20) | (dfProv["Cod_Tip"]== 19) | (dfProv["Cod_Tip"]== 1) | (dfProv["Cod_Tip"]== 14) | (dfProv["Cod_Tip"]== 15) | (dfProv["Cod_Tip"]== 21) | (dfProv["Cod_Tip"]== 13) | (dfProv["Cod_Tip"]== 22) | (dfProv["Cod_Tip"]== 16) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfR.drop(columns=["Cod_Tip"],inplace=True)
        dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

        dfC=dfProv[(dfProv["Cod_Tip"]== 5) | (dfProv["Cod_Tip"]== 9) | (dfProv["Cod_Tip"]== 17) | (dfProv["Cod_Tip"]== 23) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfC.drop(columns=["Cod_Tip"],inplace=True)
        dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

        dfT=dfProv[(dfProv["Cod_Tip"]== 6) | (dfProv["Cod_Tip"]== 18) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfT.drop(columns=["Cod_Tip"],inplace=True)
        dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

        dfP=dfProv[(dfProv["Cod_Tip"]== 8) | (dfProv["Cod_Tip"]== 7) | (dfProv["Cod_Tip"]== 10) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfP.drop(columns=["Cod_Tip"],inplace=True)
        dfP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)
    else:
        dfR=dfProv[((df["Cod_Tip"]== 20) | (dfProv["Cod_Tip"]== 19) | (dfProv["Cod_Tip"]== 1) | (dfProv["Cod_Tip"]== 14) | (dfProv["Cod_Tip"]== 15) | (dfProv["Cod_Tip"]== 21) | (dfProv["Cod_Tip"]== 13) | (dfProv["Cod_Tip"]== 22) | (dfProv["Cod_Tip"]== 16) ) & (dfProv["Fascia"]==sezP) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfR.drop(columns=["Cod_Tip"],inplace=True)
        dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)
        
        dfC=dfProv[((dfProv["Cod_Tip"]== 5) | (dfProv["Cod_Tip"]== 9) | (dfProv["Cod_Tip"]== 17) | (dfProv["Cod_Tip"]== 23)) & (dfProv["Fascia"]==sezP) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfC.drop(columns=["Cod_Tip"],inplace=True)
        dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)
        
        dfT=dfProv[((dfProv["Cod_Tip"]== 6) | (dfProv["Cod_Tip"]== 18)) & (dfProv["Fascia"]==sezP) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfT.drop(columns=["Cod_Tip"],inplace=True)
        dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)
        
        dfP=dfProv[((dfProv["Cod_Tip"]== 8) | (dfProv["Cod_Tip"]== 7) | (dfProv["Cod_Tip"]== 10)) & (dfProv["Fascia"]==sezP) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfP.drop(columns=["Cod_Tip"],inplace=True)
        dfP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)
       
    
    if(scelta=="cmp"):
        if sezP=="Tutto":
            titlep="Prezzo medio  Compravendita Immobili per Province"
        elif sezP=="B":
            titlep="Prezzo medio  Compravendita Immobili in zona Centrale per Province"
        elif sezP=="C":
            titlep="Prezzo medio  Compravendita Immobili in zona  Semi Centrale per Province"
        elif sezP=="D":
            titlep="Prezzo medio  Compravendita Immobili in zona Periferica per Province"
        elif sezP=="E":
            titlep="Prezzo medio  Compravendita Immobili in Zona Suburbana per Province"
        elif sezP=="R":
            titlep="Prezzo medio Compravendita Immobili in zona Extraurbana  per Province"    
        # Bar plot della Regione divisa per provincia Compravendita
        fig2 = go.Figure(data=[
            go.Bar(name='Residenziale', x=dfR["Prov"], y=dfR["ComprR"].round(2)),
            go.Bar(name='Commerciale', x=dfC["Prov"], y=dfC["ComprC"].round(2)),
            go.Bar(name='Terziario', x=dfT["Prov"], y=dfT["ComprT"].round(2)),
            go.Bar(name='Produttivo', x=dfP["Prov"], y=dfP["ComprP"].round(2)) 
        ])
    else:

        if sezP=="Tutto":
            titlep="Prezzo medio Locazione Immobili per Province"
        elif sezP=="B":
            titlep="Prezzo medio  Compravendita Immobili in zona Centrale per Province"
        elif sezP=="C":
            titlep="Prezzo medio Locazione Immobili in zona Centrale per Province"
        elif sezP=="D":
            titlep="Prezzo medio Locazione Immobili in zona Periferica per Province"
        elif sezP=="E":
            titlep="Prezzo medio Locazione Immobili in Zona Suburbana per Province"
        elif sezP=="R":
            titlep="Prezzo medio Locazione Immobili in zona Extraurbana per Province"  
        # Bar plot della Regione divisa per provincia Locazione
        fig2 = go.Figure(data=[
            go.Bar(name='Residenziale', x=dfR["Prov"], y=dfR["LocR"].round(2)),
            go.Bar(name='Commerciale', x=dfC["Prov"], y=dfC["LocC"].round(2)),
            go.Bar(name='Terziario', x=dfT["Prov"], y=dfT["LocT"].round(2)),
            go.Bar(name='Produttivo', x=dfP["Prov"], y=dfP["LocP"].round(2)) 
        ])

# Change the bar mode
    fig2.update_layout(barmode='group',xaxis=dict(title='Province della regione '+ Region,titlefont=dict(color='black',family='Trebuchet MS',size=20),tickfont=dict(color='black',family='Trebuchet MS',size=15)),yaxis=dict(title='Prezzo medio al (m²)',titlefont=dict(color='black',family='Trebuchet MS',size=20),ticksuffix='€',tickfont=dict(color='black',family='Trebuchet MS',size=15)),title=titlep,titlefont=dict(color='black',family='Trebuchet MS',size=18))
    fig2.update_traces(texttemplate='%{y:.2s}€', textposition='inside')

# Mappa
    dfMappaProv=pd.DataFrame()

    if scletaProv=="Tutti":
        dfMappaProv=ProDiv[ProDiv["Regione"]==Region]
        Text="Tutti gli Edifici"
    elif scletaProv=="R":
        dfMappaProv=dfProv[(dfProv["Cod_Tip"]== 20) | (dfProv["Cod_Tip"]== 19) | (dfProv["Cod_Tip"]== 1) | (dfProv["Cod_Tip"]== 14) | (dfProv["Cod_Tip"]== 15) | (dfProv["Cod_Tip"]== 21) | (dfProv["Cod_Tip"]== 13) | (dfProv["Cod_Tip"]== 22) | (dfProv["Cod_Tip"]== 16) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfMappaProv.drop(columns=["Cod_Tip"],inplace=True)
        Text="Edifici Residenziali"
    elif scletaProv=="C":
        dfMappaProv=dfProv[(dfProv["Cod_Tip"]== 5) | (dfProv["Cod_Tip"]== 9) | (dfProv["Cod_Tip"]== 17) | (dfProv["Cod_Tip"]== 23) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfMappaProv.drop(columns=["Cod_Tip"],inplace=True)
        Text="Edifici Commerciali"
    elif scletaProv=="T":
        dfMappaProv=dfProv[(dfProv["Cod_Tip"]== 6) | (dfProv["Cod_Tip"]== 18) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfMappaProv.drop(columns=["Cod_Tip"],inplace=True)
        Text="Edifici Terziari"
    elif scletaProv=="P":
        dfMappaProv=dfProv[(dfProv["Cod_Tip"]== 8) | (dfProv["Cod_Tip"]== 7) | (dfProv["Cod_Tip"]== 10) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfMappaProv.drop(columns=["Cod_Tip"],inplace=True)
        Text="Edifici Produttivi"
    if(scelta=="cmp"):
        # Chroplet map Province della Regione selezionata
        mappa = go.Figure(data=go.Choropleth(
            geojson=gprov, 
            z=dfMappaProv["Compr"],
            text=dfMappaProv["Compr"],
            locations=dfMappaProv["Prov"], 
            featureidkey="properties.prov_name",
            colorscale ="Blues",
            colorbar_tickprefix = '€',
            colorbar_title = 'Prezzo Medio<br>Compravendita al (m²) €',
            colorbar_title_font_color='black',
            colorbar_tickfont_color='black',
            hovertemplate='Prezzo Medio: %{text:.2f}€ <br>%{location}' + '<extra></extra>'
        ))
    else:
        # Chroplet map Province della Regione selezionata
        mappa = go.Figure(data=go.Choropleth(
            geojson=gprov, 
            z=dfMappaProv["Loc"],
            text=dfMappaProv["Loc"],
            locations=dfMappaProv["Prov"], 
            featureidkey="properties.prov_name",
            colorscale ="Blues",
            colorbar_tickprefix = '€',
            colorbar_title = 'Prezzo Medio<br> Locazione al (m²) €',
            colorbar_title_font_color='black',
            colorbar_tickfont_color='black',
            hovertemplate='Prezzo Medio: %{text:.2f}€ <br>%{location}' + '<extra></extra>'
        ))

    mappa.update_geos(fitbounds="locations", visible=False,center=None, projection_scale=3)
    mappa.update_layout(margin={"r":0,"t":0,"l":0,"b":0},dragmode=False)

    return fig,fig2,mappa,ListC,ListC[0],Region,Text

############################### GRAFICO COMUNI ###################
@app.callback(
    Output("graph4", "children"), 
    Output("coms","children"),
    Input("Reg", "value"), 
    Input("scelta","value"))
def displayGraph(Reg,scelta):
    lista_colori= [
    '#FF5733',  # Arancione acceso
    '#006400',  # Verde scuro
    '#1E90FF',  # Blu acceso
    '#FF1493',  # Rosa acceso
    '#32CD32',  # Giallo acceso
    '#8B4513',  # Marrone acceso
    '#9400D3',  # Viola acceso
    '#DC143C',  # Rosso acceso
    '#00FA9A',  # Verde acqua acceso
    '#4682B4',  # Blu acciaio acceso
    '#D2691E',  # Cioccolato acceso
    '#8B008B',  # Viola scuro acceso
    '#FF6347'   # Rosso corallo acceso
    ]
    Region2=Reg
    ### GRAFICO COMUNI
    List=ListaComm[ListaComm["Regione"]==Region2]["Comune_descrizione"].to_list()
    ## Ricontrollo la regione perchè ci possono essere due comuni con lo stesso nome in regioni diverse
    Comm=dfRc[dfRc["Regione"]==Region2].query("Comune_descrizione in @List")
    Prov=Comm["Prov"].unique()
    maxC=Comm["ComprR"].max()
    maxL=Comm["LocR"].max()
    graphs=[]
    
    dictcolor=dict(zip(Prov,lista_colori[:len(Prov)]))
    

    
    for i in range(len(Prov)):
        nodi_tick=[]
        dfP=dfRc[dfRc["Prov"]==Prov[i]]
        Lis=dfRc[dfRc["Prov"]==Prov[i]]["Comune_descrizione"].tolist()

        ###Valle D'Aosta
        if Prov[i]=="Valle d'Aosta/Vallée d'Aoste":
            if scelta=="cmp":
                x=dfP[dfP["Comune_descrizione"]=="AOSTA"]["ComprR"].item()
            else:
                x=dfP[dfP["Comune_descrizione"]=="AOSTA"]["LocR"].item()
            y=dfP[dfP["Comune_descrizione"]=="AOSTA"]["Comune_descrizione"].item()
            text="Aosta"
        ###Bolzano-Bozen
        elif Prov[i]=="Bolzano/Bozen":
            if scelta=="cmp":
                x=dfP[dfP["Comune_descrizione"]=="BOLZANO .BOZEN."]["ComprR"].item()
            else:
                x=dfP[dfP["Comune_descrizione"]=="BOLZANO .BOZEN."]["LocR"].item()
            y=dfP[dfP["Comune_descrizione"]=="BOLZANO .BOZEN."]["Comune_descrizione"].item()
            text="Bolzano"
        ### Massa Carrara
        elif Prov[i]=="Massa-Carrara":
            if scelta=="cmp":
                x=dfP[dfP["Comune_descrizione"]=="MASSA"]["ComprR"].item()
            else:
                x=dfP[dfP["Comune_descrizione"]=="MASSA"]["LocR"].item()
            y=dfP[dfP["Comune_descrizione"]=="MASSA"]["Comune_descrizione"].item()
            text="Massa"
        ### Verbano Cusio Ossola
        elif Prov[i]=="Verbano-Cusio-Ossola":
            if scelta=="cmp":
                x=dfP[dfP["Comune_descrizione"]=="VERBANIA"]["ComprR"].item()
            else:
                x=dfP[dfP["Comune_descrizione"]=="VERBANIA"]["LocR"].item()
            y=dfP[dfP["Comune_descrizione"]=="VERBANIA"]["Comune_descrizione"].item()
            text="Verbania"
        ### PESARO E URBINO
        elif Prov[i]=="Pesaro e Urbino":
            if scelta=="cmp":
                x=dfP[dfP["Comune_descrizione"]=="PESARO"]["ComprR"].item()
            else:
                x=dfP[dfP["Comune_descrizione"]=="PESARO"]["LocR"].item()

            y=dfP[dfP["Comune_descrizione"]=="PESARO"]["Comune_descrizione"].item()
            text="Pesaro"
        #### FORLI CESENA
        elif Prov[i]=="Forlì-Cesena":
            if scelta=="cmp":
                x=dfP[dfP["Comune_descrizione"]=="FORLI`"]["ComprR"].item()
            else:
                x=dfP[dfP["Comune_descrizione"]=="FORLI`"]["LocR"].item()
            y=dfP[dfP["Comune_descrizione"]=="FORLI`"]["Comune_descrizione"].item()
            text="Forlì"
        else:
            if scelta=="cmp":
                x=dfP[dfP["Comune_descrizione"]==Prov[i].upper()]["ComprR"].item()
            else:
                x=dfP[dfP["Comune_descrizione"]==Prov[i].upper()]["LocR"].item()
            y=dfP[dfP["Comune_descrizione"]==Prov[i].upper()]["Comune_descrizione"].item()
            text=Prov[i]
        
        
        linea=[]
        for j in range(0,len(Lis)):
            if(Lis[j]==y):
                linea.append(x)
                nodi_tick.append(y)
            else:
                linea.append(0)
                nodi_tick.append(" ")
        if(scelta=="cmp"):
            title="Prezzo medio per la Compravendita degli Immobili Residenziali per i Comuni della Regione "
            fig3 = px.scatter(dfP,x="ComprR",y="Comune_descrizione",color="Prov",labels={"Prov":"Provincia","ComprR":"Prezzo Medio","Comune_descrizione":"Comune"},color_discrete_map=dictcolor)
            fig3.update_yaxes(tickvals=nodi_tick)
            fig3.update_layout(xaxis=dict(title='Prezzo medio al (m²)',titlefont=dict(size=20, color='black'),range=[0,maxC +100],tickfont=dict(size=14, color='black')),yaxis=dict(title="Comuni Prov. di " + Prov[i],titlefont=dict(size=20, color='black'),tickfont=dict(size=14, color='black')))
            xreg=dfR[dfR["Regione"]==Region2]["ComprR"].item()
        else:
            title="Prezzo medio per la Locazione degli Immobili Residenziali per i Comuni della Regione "
            fig3 = px.scatter(dfP,x="LocR",y="Comune_descrizione",color="Prov",labels={"Prov":"Provincia","LocR":"Prezzo Medio","Comune_descrizione":"Comune"},color_discrete_map=dictcolor)
            fig3.update_yaxes(tickvals=nodi_tick)
            fig3.update_layout(xaxis=dict(title='Prezzo medio al (m²)',titlefont=dict(size=20, color='black'),range=[0,maxL+3],tickfont=dict(size=14, color='black')),yaxis=dict(title="Provincia Prov. di "+Prov[i],titlefont=dict(size=20, color='black'),tickfont=dict(size=14, color='black')))
            xreg=dfR[dfR["Regione"]==Region2]["LocR"].item()
    
        fig3.add_vline(x=xreg, line_width=3, line_dash="dash", line_color="black",annotation_text="Media Regionale: "+str(round(xreg,2)) +"€") # Da cambiare
        fig3.update_xaxes(ticksuffix="€")

        
        """
        fig3.add_annotation(
            x=x,
            y=y,
            text=text,
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-10,
            font=dict(size=13)
        )
        """
        graphs.append(dcc.Graph(figure=fig3))
    return graphs,title + " " + Region2
    

##### GRAFICO SINGOLO COMUNE ####################################

@app.callback(
    Output("Com", "children"), 
    Output("BoxP","figure"),
    Output("DotP","figure"),
    Input("CommD","value"),
    Input("scelta","value"))
def display_BarPlot(Comm,scelta):
    Comu=Comm
    Prov=ListaComm[ListaComm["Comune_descrizione"]==Comu]["Prov"].item()
    x=["Residenziale","Commerciale","Terziario", "Produttivo"]
    if scelta=="cmp":
        title="Prezzo medio Compravendita immobili comune di "
        if len(dfRc[dfRc["Comune_descrizione"]==Comu]["ComprR"].tolist())==0:
            Res=0
            Resmin=0
        else:
            Res=dfRc[dfRc["Comune_descrizione"]==Comu]["ComprR"].item()
            Resmin=dfRc[dfRc["Comune_descrizione"]==Comu]["Compr_min"].item()
        if len(dfCc[dfCc["Comune_descrizione"]==Comu]["ComprC"].tolist())==0:
            Comm=0
            Commmin=0
        else:
            Comm=dfCc[dfCc["Comune_descrizione"]==Comu]["ComprC"].item()
            Commmin=dfCc[dfCc["Comune_descrizione"]==Comu]["Compr_min"].item()
        if len(dfTc[dfTc["Comune_descrizione"]==Comu]["ComprT"].tolist())==0:
            Terz=0
            Terzmin=0
        else:
            Terz=dfTc[dfTc["Comune_descrizione"]==Comu]["ComprT"].item()
            Terzmin=dfTc[dfTc["Comune_descrizione"]==Comu]["Compr_min"].item()

        if len(dfPc[dfPc["Comune_descrizione"]==Comu]["ComprP"].tolist())==0:
            Prod=0
            Prodmin=0
        else:
            Prod=dfPc[dfPc["Comune_descrizione"]==Comu]["ComprP"].item()
            Prodmin=dfPc[dfPc["Comune_descrizione"]==Comu]["Compr_min"].item()
    else:
        title="Prezzo medio Locazione immobili comune di "
        if len(dfRc[dfRc["Comune_descrizione"]==Comu]["LocR"].tolist())==0:
            Res=0
            Resmin=0
        else:
            Res=dfRc[dfRc["Comune_descrizione"]==Comu]["LocR"].item()
            Resmin=dfRc[dfRc["Comune_descrizione"]==Comu]["Loc_min"].item()
        if len(dfCc[dfCc["Comune_descrizione"]==Comu]["LocC"].tolist())==0:
            Comm=0
            Commmin=0
        else:
            Comm=dfCc[dfCc["Comune_descrizione"]==Comu]["LocC"].item()
            Commmin=dfCc[dfCc["Comune_descrizione"]==Comu]["Loc_min"].item()

        if len(dfTc[dfTc["Comune_descrizione"]==Comu]["LocT"].tolist())==0:
            Terz=0
            Terzmin=0
        else:
            Terz=dfTc[dfTc["Comune_descrizione"]==Comu]["LocT"].item()
            Terzmin=dfTc[dfTc["Comune_descrizione"]==Comu]["Loc_min"].item()

        if len(dfPc[dfPc["Comune_descrizione"]==Comu]["LocP"].tolist())==0:
            Prod=0
            Prodmin=0
        else:
            Prod=dfPc[dfPc["Comune_descrizione"]==Comu]["LocP"].item()
            Prodmin=dfPc[dfPc["Comune_descrizione"]==Comu]["Loc_min"].item()
            
    y=[round(Res,2),round(Comm,2),round(Terz,2),round(Prod,2)]
    # bar plot
    fig4 = go.Figure(data=[go.Bar(
            x=x, y=y,
            textposition='auto',
        )])
    # Change the bar mode
    fig4.update_layout(barmode='group',xaxis=dict(title='Tipo di Immobile',tickfont=dict(color='black',family='Trebuchet MS',size=15),titlefont=dict(color='black',family='Trebuchet MS',size=20)),yaxis=dict(title='Prezzo medio al (m²)',ticksuffix='€',tickfont=dict(color='black',family='Trebuchet MS',size=15),titlefont=dict(color='black',family='Trebuchet MS',size=20)),title=title +Comu + " in prov. di "+ Prov,titlefont=dict(color='black',family='Trebuchet MS',size=20))
    fig4.update_traces(texttemplate='%{y:.2s}€', textposition='inside') 
    
    x=["Residenziale","Commerciale","Terziario", "Produttivo"]
    y=[(Resmin,Res),(Commmin,Comm),(Terzmin,Terz),(Prodmin,Prod)]
    # scatter plot with error
    fig5=go.Figure(data=[
        go.Scatter(
        x=[interval[0], interval[1]],
        y=[element, element],
        mode='lines+markers',
        name=element,
        error_x=dict(
            type='data',
            symmetric=False,
            array=[interval[1] - interval[0]],
            arrayminus=[0]
        )
    ) for element, interval in zip(x, y)    
    ])
    fig5.update_layout(
                xaxis=dict(title='Prezzo minimo e massimo medio al (m²)',ticksuffix='€',tickfont=dict(color='black',family='Trebuchet MS',size=15),titlefont=dict(color='black',family='Trebuchet MS',size=20)),
                yaxis=dict(title='Tipo di Immobile',tickfont=dict(color='black',family='Trebuchet MS',size=15),titlefont=dict( color='black',family='Trebuchet MS',size=20)),
                showlegend=True,title="Prezzo minimo e massimo medio immobili del Comune di "+Comu + " in prov. di "+ Prov,titlefont=dict(color='black',family='Trebuchet MS',size=20)) 
    return "Comune di: " + Comu,fig4,fig5


@app.callback(
    Output("Comm2", "figure"), 
    Input("CommD","value"),
    Input("scelta","value"))
def display_BarPlot(Comm,scelta):
    dfCom=dfRcfasc[dfRcfasc['Comune_descrizione']==Comm]
    x=['Centrale','Semicentrale','Periferica','Urbana','Extraurbana']
    if scelta=='cmp':
        title="Prezzi di Compravendita Immobili Residenziali comune di "
        if dfCom[dfCom['Fascia']=='B']['ComprR'].tolist()==0:
            dfB=0
        else:
            dfB=dfCom[dfCom['Fascia']=='B']['ComprR'].item()
        if len(dfCom[dfCom['Fascia']=='C']['ComprR'].tolist())==0:
            dfC=0
        else:
            dfC=dfCom[dfCom['Fascia']=='C']['ComprR']
          
        if len(dfCom[dfCom['Fascia']=='D']['ComprR'].tolist())==0:
            dfD=0
        else:
           
            dfD=dfCom[dfCom['Fascia']=='D']['ComprR'].item()
        if len(dfCom[dfCom['Fascia']=='E']['ComprR'].tolist())==0:
            dfE=0
        else:
            dfE=dfCom[dfCom['Fascia']=='E']['ComprR'].item()
        if len(dfCom[dfCom['Fascia']=='R']['ComprR'].tolist())==0:
            dfR=0
        else:
            dfR=dfCom[dfCom['Fascia']=='R']['ComprR'].item()
    else:
        title="Prezzi di Locazione Immobili Residenziali "
        if len(dfCom[dfCom['Fascia']=='B']['LocR'].tolist())==0:
            dfB=0
        else:
            dfB=dfCom[dfCom['Fascia']=='B']['LocR'].item()
        if len(dfCom[dfCom['Fascia']=='C']['LocR'].tolist())==0:
            dfC=0
        else:
            dfC=dfCom[dfCom['Fascia']=='C']['LocR'].item()
        if len(dfCom[dfCom['Fascia']=='D']['LocR'].tolist())==0:
            dfD=0
        else:
            dfD=dfCom[dfCom['Fascia']=='D']['LocR'].item()
        if len(dfCom[dfCom['Fascia']=='E']['LocR'].tolist())==0:
            dfE=0
        else:
            dfE=dfCom[dfCom['Fascia']=='E']['LocR'].item()
        if len(dfCom[dfCom['Fascia']=='R']['LocR'].tolist())==0:
            dfR=0
        else:
            dfR=dfCom[dfCom['Fascia']=='R']['LocR'].item()
    
    y=[round(dfB,2),round(dfC,2),round(dfD,2),round(dfE,2),round(dfR,2)]
    fig=go.Figure(data=[go.Bar(
            x=x, y=y,
        )])
    fig.update_layout(xaxis=dict(title='Zona di Riferimento',titlefont=dict(color='black',family='Trebuchet MS',size=20),tickfont=dict(color='black',family='Trebuchet MS',size=15)),yaxis=dict(title='Prezzo medio al (m²)',titlefont=dict(color='black',family='Trebuchet MS',size=20),ticksuffix='€',tickfont=dict(color='black',family='Trebuchet MS',size=15)),title=title +Comm ,titlefont=dict(color='black',family='Trebuchet MS',size=20))
    fig.update_traces(texttemplate='%{y:.2s}€', textposition='inside') 
    return fig
    
if __name__ == "__main__":
    app.run_server(debug=False,port=8052)




