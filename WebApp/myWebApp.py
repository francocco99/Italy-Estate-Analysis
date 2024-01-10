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
dfRc=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ][["Comune_descrizione","Compr","Loc","Compr_min","Loc_min"]].groupby("Comune_descrizione").mean("Compr,Loc").reset_index()
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
    html.H3('Seleziona il tipo di Dato:',style={ 'text-align': 'center'}),
     dcc.RadioItems(
        id='sceltaMappa', 
        options=[
        {'label': 'Compravendita', 'value': 'cmp'},
        {'label': 'Locazione', 'value': 'loc'}],
        value="cmp",
        style={ 'text-align': 'center',"margin-top": "20px"},
        inline=True
    ),
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
    html.H1(id='Title',style={ 'text-align': 'center'}),
    dcc.Graph(id='graph2'),
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
            html.H2('Regione',style={'text-align': 'center'}),
            html.H3('Scegli la zona',style={'text-align': 'center'}),
            dcc.RadioItems(
                id='sezR', 
                options=[{'label':'Tutte le Zone','value':'Tutto'},
                {'label': 'Zona Centrale & Semiceltrale', 'value': 'C'},
                {'label': 'Periferica', 'value': 'D'},
                {'label': 'Suburbana', 'value': 'E'},
                {'label': 'Extraurbana', 'value': 'R'}],
                value="Tutto",
                style={ 'text-align': 'center',"margin-bottom": "40px"},
                inline=True
            ),
            dcc.Graph(id='graph')
        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
        html.Div([
            html.H2('Provincia',style={'text-align': 'center'}),
            dcc.Tabs(id="table-1",value="table-box",children=[
                dcc.Tab(label="Box Plot Province", value="table-box",children=[        
                    dcc.RadioItems(
                        id='sezP', 
                        options=[{'label':'Tutte le Zone','value':'Tutto'},
                        {'label': 'Zona Centrale & Semiceltrale', 'value': 'C'},
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
                    dcc.Graph(id='mappaProv')      
                ])
            ])

        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}
        ),
    ], className="row"),
    html.H2('Comuni',style={'text-align': 'center'}),
    dcc.Graph(id="graph4"),
    html.H3("Seleziona il comune",style={'text-align': 'center'}),
    dcc.Dropdown(id='CommD',value="ABBATEGGIO"),
    html.H2(id="Com",style={'text-align': 'center'}),
    dcc.Tabs(id="table-2",value="table-dot",children=[
        dcc.Tab(label="Dot Plot Comune", value="table-dot",children=[        
            dcc.Graph(id='DotP')
        ]),
        dcc.Tab(label="Box Plot Comune", value="table-box", children=[
            dcc.Graph(id='BoxP')      
        ])
    ]),

])

############################# MAPPA  REGIONI ##############################
@app.callback(
    Output("graph2", "figure"),
    Output("Title","children"), 
    Input("graph2", "clickData"),
    Input("Tipo", "value"),
    Input("sceltaMappa","value"))
def display_choropleth(clickData,Tipo,scelta):
    dfMappa=pd.DataFrame()
    dfMappa["Regione"]=dfRegion["Regione"]
    
    if Tipo=="Tutti":
        Title="Prezzo di tutti gli Immobili"
        if scelta=="cmp":
            dfMappa["Value"]=dfRegion["Compr"]
        else:
            dfMappa["Value"]=dfRegion["Loc"]
    elif Tipo=="R":
        Title="Prezzo Immobili Residenziali"
        if scelta=="cmp":
            dfMappa["Value"]=dfTI2["ComprR"]
        else:
            dfMappa["Value"]=dfTI2["LocR"]
    elif Tipo=="C":
        Title="Prezzo Immobili Commerciali"
        if scelta=="cmp":
            dfMappa["Value"]=dfTI2["ComprC"]
        else:
            dfMappa["Value"]=dfTI2["LocC"]
    elif Tipo=="T":
        Title="Prezzo Immobili Terziari"
        if scelta=="cmp":
            dfMappa["Value"]=dfTI2["ComprT"]
        else:
            dfMappa["Value"]=dfTI2["LocT"]
    elif Tipo=="P":
        Title="Prezzo Immobili Produttivi"
        if scelta=="cmp":
            dfMappa["Value"]=dfTI2["ComprP"]
        else:
            dfMappa["Value"]=dfTI2["LocP"]
    
    if scelta=="cmp":
        title='Prezzo Medio<br>Compravendita al (m²)  €'
    else:
        title='Prezzo Medio<br>Locazione al (m²) €'

    figm = go.Figure(data=go.Choropleth(
    geojson=gj, 
    z=dfMappa["Value"],
    text=dfMappa["Value"],
    locations=dfMappa["Regione"], 
    featureidkey="properties.name",
    colorscale ="Blues",
    colorbar_tickprefix = '€',
    colorbar_title = title,
    ))
    figm.update_geos(fitbounds="locations", visible=False,center=None, projection_scale=3)
    figm.update_layout(margin={"r":0,"t":0,"l":0,"b":0},dragmode=False)
    if clickData:
        location=clickData["points"][0]["location"]
        figm.update_traces(selectedpoints=[list(dfTI2["Regione"]).index(location)], 
                              selected=dict(marker=dict(opacity=0.8)))
        
    return figm,Title




################ CLICK ON MAP ################################
@app.callback(
    Output("graph", "figure"), 
    Output("graph3","figure"),
    Output("mappaProv","figure"),
    Output("CommD","options"),
    Output("nameProv","children"),
    Input("scelta","value"),
    Input("graph2", "clickData"),
    Input("Reg", "value"),
    Input("sezR","value"),
    Input("sezP","value"))
def display_BarPlot2(scelta,clickData,Reg,sezR,sezP):
 
    global OldClick
    global OldReg
    global Region
    if clickData is None:
        OldClick=0
        Region=Reg
        OldReg=Reg
    elif OldClick==0:
        Region=clickData["points"][0]["location"].upper()
        OldClick=clickData["points"][0]["location"].upper()
        
    elif (OldClick!=Reg) & (OldReg!=Reg):
        Region=Reg
        OldReg=Reg
    else:
        Region=clickData["points"][0]["location"].upper()
        OldClick=clickData["points"][0]["location"].upper()

    x=["Residenziale","Commerciale","Terziario", "Produttivo"]

    
        # Prezzi Compravendita
    if sezR=="Tutto":
        if(scelta=="cmp"):
            title="Prezzo medio Compravendita Immobili Regione " + Region
            y=[dfTI[dfTI["Regione"]==Region]["ComprR"].item(),dfTI[dfTI["Regione"]==Region]["ComprC"].item(),dfTI[dfTI["Regione"]==Region]["ComprT"].item(),dfTI[dfTI["Regione"]==Region]["ComprP"].item()]
        else:
            title="Prezzo medio Locazione  Regione " + Region
            y=[dfTI[dfTI["Regione"]==Region]["LocR"].item(),dfTI[dfTI["Regione"]==Region]["LocC"].item(),dfTI[dfTI["Regione"]==Region]["LocT"].item(),dfTI[dfTI["Regione"]==Region]["LocP"].item()]
    elif sezR=="C":
        
        dfR=df[((df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ) &  ((df["Fascia"]=="C") | (df["Fascia"]=="B")) ][["Regione","Compr","Loc"]].groupby("Regione").mean().reset_index()
        dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)
        
        dfC=df[((df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23)) &  ((df["Fascia"]=="C") | (df["Fascia"]=="B")) ][["Regione","Compr","Loc"]].groupby("Regione").mean().reset_index()
        dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)
        
        dfT=df[((df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18)) &  ((df["Fascia"]=="C") | (df["Fascia"]=="B")) ][["Regione","Compr","Loc"]].groupby("Regione").mean().reset_index()
        dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)
        
        dfP=df[((df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10)) &  ((df["Fascia"]=="C") | (df["Fascia"]=="B")) ][["Regione","Compr","Loc"]].groupby("Regione").mean().reset_index()
        dfP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)

        if(scelta=="cmp"):
            title="Prezzo medio Compravendita Immobili in zona Centrale Regione " + Region
            y=[dfR[dfR["Regione"]==Region]["ComprR"].item(),dfC[dfC["Regione"]==Region]["ComprC"].item(),dfT[dfT["Regione"]==Region]["ComprT"].item(),dfP[dfP["Regione"]==Region]["ComprP"].item()]
        else:
            title="Prezzo medio Locazione Immobili in zona Centrale Regione " + Region
            y=[dfR[dfR["Regione"]==Region]["LocR"].item(),dfC[dfC["Regione"]==Region]["LocC"].item(),dfT[dfT["Regione"]==Region]["LocT"].item(),dfP[dfP["Regione"]==Region]["LocP"].item()]
    else:
        dfR=df[((df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ) &  (df["Fascia"]==sezR) ][["Regione","Compr","Loc"]].groupby("Regione").mean().reset_index()
        dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)
    
        dfC=df[((df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23)) & (df["Fascia"]==sezR) ][["Regione","Compr","Loc"]].groupby("Regione").mean().reset_index()
        dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)
    
        dfT=df[((df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18)) &  (df["Fascia"]==sezR) ][["Regione","Compr","Loc"]].groupby("Regione").mean().reset_index()
        dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)
   
        dfP=df[((df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10)) &  (df["Fascia"]==sezR) ][["Regione","Compr","Loc"]].groupby("Regione").mean().reset_index()
        dfP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)
        if(scelta=="cmp"):
            if sezR=="D":
                title="Prezzo medio Compravendita Immobili in zona Periferica Regione " + Region
            elif sezR=="E":
                title="Prezzo medio Compravendita Immobili in Zona Suburbana Regione " + Region
            elif sezR=="R":
                title="Prezzo medio Compravendita Immobili in zona Extraurbana Regione " + Region
            if len(dfR[dfR["Regione"]==Region]["ComprR"].tolist())==0:
                Res=0
            else: 
                Res=dfR[dfR["Regione"]==Region]["ComprR"].item()

            if len(dfC[dfR["Regione"]==Region]["ComprC"].tolist())==0:
                Com=0
            else: 
                Com=dfC[dfR["Regione"]==Region]["ComprC"].item()

            if len(dfT[dfT["Regione"]==Region]["ComprT"].tolist())==0:
                Ter=0
            else: 
                Ter=dfT[dfT["Regione"]==Region]["ComprT"].item()
                
            if len(dfP[dfP["Regione"]==Region]["ComprP"].tolist())==0:
                Pro=0
            else: 
                Pro=dfP[dfP["Regione"]==Region]["ComprP"].item()
                

            y=[Res,Com,Ter,Pro]
        else:
            if sezR=="D":
                title="Prezzo medio Locazione Immobili in zona Periferica Regione " + Region
            elif sezR=="E":
                title="Prezzo medio Locazione Immobili in Zona Suburbana Regione " + Region
            elif sezR=="R":
                title="Prezzo medio Locazione Immobili in zona Extraurbana Regione " + Region
            
            if len(dfR[dfR["Regione"]==Region]["LocR"].tolist())==0:
                Res=0
            else: 
                Res=dfR[dfR["Regione"]==Region]["LocR"].item()

            if len(dfC[dfC["Regione"]==Region]["LocC"].tolist())==0:
                Com=0
            else: 
                Com=dfC[dfC["Regione"]==Region]["LocC"].item()

            if len(dfT[dfT["Regione"]==Region]["LocT"].tolist())==0:
                Ter=0
            else: 
                Ter=dfT[dfT["Regione"]==Region]["LocT"].item()
                
            if len(dfP[dfP["Regione"]==Region]["LocP"].tolist())==0:
                Pro=0
            else: 
                Pro=dfP[dfP["Regione"]==Region]["LocP"].item()
            y=[Res,Com,Ter,Pro]
        # Prezzi Locazione
        # Bar plot Regione divio per tipo di edificio
    fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
            
        )])
    # Change the bar mode
    fig.update_layout(barmode='group',xaxis=dict(title='Tipo di Immobile'),yaxis=dict(title='Prezzo medio al (m²)'),title=title)
    fig.update_traces(texttemplate='%{text:.2s}€', textposition='inside')

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
    elif sezP=="C":
        dfR=dfProv[((dfProv["Cod_Tip"]== 20) | (dfProv["Cod_Tip"]== 19) | (dfProv["Cod_Tip"]== 1) | (dfProv["Cod_Tip"]== 14) | (dfProv["Cod_Tip"]== 15) | (dfProv["Cod_Tip"]== 21) | (dfProv["Cod_Tip"]== 13) | (dfProv["Cod_Tip"]== 22) | (dfProv["Cod_Tip"]== 16) ) & ((dfProv["Fascia"]=="C") | (dfProv["Fascia"]=="B")) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfR.drop(columns=["Cod_Tip"],inplace=True)
        dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)
        
        dfC=dfProv[((dfProv["Cod_Tip"]== 5) | (dfProv["Cod_Tip"]== 9) | (dfProv["Cod_Tip"]== 17) | (dfProv["Cod_Tip"]== 23)) &  ((dfProv["Fascia"]=="C") | (dfProv["Fascia"]=="B")) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfC.drop(columns=["Cod_Tip"],inplace=True)
        dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)
        
        dfT=dfProv[((dfProv["Cod_Tip"]== 6) | (dfProv["Cod_Tip"]== 18)) &  ((dfProv["Fascia"]=="C") | (dfProv["Fascia"]=="B")) ].groupby("Prov").mean("Compr,Loc").reset_index()
        dfT.drop(columns=["Cod_Tip"],inplace=True)
        dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)
        
        dfP=dfProv[((dfProv["Cod_Tip"]== 8) | (dfProv["Cod_Tip"]== 7) | (dfProv["Cod_Tip"]== 10)) &  ((dfProv["Fascia"]=="C") | (dfProv["Fascia"]=="B")) ].groupby("Prov").mean("Compr,Loc").reset_index()
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
        elif sezP=="C":
            titlep="Prezzo medio  Compravendita Immobili in zona Centrale per Province"
        elif sezP=="D":
            titlep="Prezzo medio  Compravendita Immobili in zona Periferica per Province"
        elif sezP=="E":
            titlep="Prezzo medio  Compravendita Immobili in Zona Suburbana per Province"
        elif sezP=="R":
            titlep="Prezzo medio Compravendita Immobili in zona Extraurbana  per Province"    
        # Bar plot della Regione divisa per provincia Compravendita
        fig2 = go.Figure(data=[
            go.Bar(name='Residenziale', x=dfR["Prov"], y=dfR["ComprR"],text=dfR["ComprR"]),
            go.Bar(name='Commerciale', x=dfC["Prov"], y=dfC["ComprC"],text=dfC["ComprC"]),
            go.Bar(name='Terziario', x=dfT["Prov"], y=dfT["ComprT"],text=dfT["ComprT"]),
            go.Bar(name='Produttivo', x=dfP["Prov"], y=dfP["ComprP"],text=dfP["ComprP"]) 
        ])
    else:

        if sezP=="Tutto":
            titlep="Prezzo medio Locazione Immobili per Province"
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
            go.Bar(name='Residenziale', x=dfR["Prov"], y=dfR["LocR"],text=dfR["LocR"]),
            go.Bar(name='Commerciale', x=dfC["Prov"], y=dfC["LocC"],text=dfC["LocC"]),
            go.Bar(name='Terziario', x=dfT["Prov"], y=dfT["LocT"],text=dfT["LocT"]),
            go.Bar(name='Produttivo', x=dfP["Prov"], y=dfP["LocP"],text=dfP["LocP"]) 
        ])

# Change the bar mode
    fig2.update_layout(barmode='group',xaxis=dict(title='Province della regione '+ Region),yaxis=dict(title='Prezzo medio al (m²)'),title=titlep)
    fig2.update_traces(texttemplate='%{text:.2s}€', textposition='inside')
# Mappa
    Prov=ProDiv[ProDiv["Regione"]==Region]
    if(scelta=="cmp"):
        # Chroplet map Province della Regione selezionata
        mappa = go.Figure(data=go.Choropleth(
            geojson=gprov, 
            z=Prov["Compr"],
            text=Prov["Compr"],
            locations=Prov["Prov"], 
            featureidkey="properties.prov_name",
            colorscale ="Blues",
            colorbar_tickprefix = '€',
            colorbar_title = 'Prezzo Medio<br>Compravendita al (m²) €',
        ))
    else:
        # Chroplet map Province della Regione selezionata
        mappa = go.Figure(data=go.Choropleth(
            geojson=gprov, 
            z=Prov["Loc"],
            text=Prov["Loc"],
            locations=Prov["Prov"], 
            featureidkey="properties.prov_name",
            colorscale ="Blues",
            colorbar_tickprefix = '€',
            colorbar_title = 'Prezzo Medio<br> Locazione al (m²) €',
        ))

    mappa.update_geos(fitbounds="locations", visible=False,center=None, projection_scale=3)
    mappa.update_layout(margin={"r":0,"t":0,"l":0,"b":0},dragmode=False)
    return fig,fig2,mappa,ListC,Region


############################### GRAFICO COMUNI ###################
@app.callback(
    Output("graph4", "figure"), 
    Input("graph2", "clickData"),
    Input("Reg", "value"), 
    Input("scelta","value"))
def displayGraph(clickData,Reg,scelta):
    global OldClick2
    global OldReg2
    global Region2
    if clickData is None:
        OldClick2=0
        Region2=Reg
        OldReg2=Reg
    elif OldClick==0:
        Region2=clickData["points"][0]["location"].upper()
        OldClick2=clickData["points"][0]["location"].upper()
        
    elif (OldClick2!=Reg) & (OldReg2!=Reg):
        Region2=Reg
        OldReg2=Reg
    else:
        Region2=clickData["points"][0]["location"].upper()
        OldClick2=clickData["points"][0]["location"].upper()
    ### GRAFICO COMUNI
    List=ListaComm[ListaComm["Regione"]==Region2]["Comune_descrizione"].to_list()
    ## Ricontrollo la regione perchè ci possono essere due comuni con lo stesso nome in regioni diverse
    Comm=Commtot[Commtot["Regione"]==Region2].query("Comune_descrizione in @List")
    if(scelta=="cmp"):
        title="Prezzo medio per la Compravendita degli Immobili per i Comuni della Regione "
        fig3 = px.scatter(Comm,x="Compr_max",y="Comune_descrizione",color="Prov",labels={"Prov":"Province"})
        xreg=dfRegionUp[dfRegionUp["Regione"]==Region2]["Compr"].item()
    else:
        title="Prezzo medio per la Locazione degli Immobili per i Comuni della Regione "
        fig3 = px.scatter(Comm,x="Loc_max",y="Comune_descrizione",color="Prov",labels={"Prov":"Province"})
        xreg=dfRegionUp[dfRegionUp["Regione"]==Region2]["Loc"].item()
    
    fig3.add_vline(x=xreg, line_width=3, line_dash="dash", line_color="blue",annotation_text="Media Regionale: "+str(round(xreg,2)) +"€")
    fig3.update_xaxes(ticksuffix="€")
    fig3.update_layout(title=title+Region,xaxis=dict(title='Prezzo medio al (m²)'),yaxis=dict(title='Comuni'),height=700)
    return fig3
    

##### GRAFICO SINGOLO COMUNE ####################################

@app.callback(
    Output("Com", "children"), 
    Output("BoxP","figure"),
    Output("DotP","figure"),
    Input("graph4", "clickData"),
    Input("CommD","value"),
    Input("scelta","value"))
def display_BarPlot(clickData,Comm,scelta):
    global OldClick3
    global Oldcom
    global Comu
    if clickData is None:
        OldClick3=0
        Comu=Comm
        Oldcom=Comm
    elif OldClick3==0:
        Comu=clickData["points"][0]['y'].upper()
        OldClick3=clickData["points"][0]['y'].upper()
        
    elif (OldClick3!=Comm) & (Oldcom!=Comm):
        Comu=Comm
        Oldcom=Comm
    else:
        Comu=clickData["points"][0]['y'].upper()
        OldClick3=clickData["points"][0]['y'].upper()
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
            
    y=[Res,Comm,Terz,Prod]
    # bar plot
    fig4 = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
        )])
    # Change the bar mode
    fig4.update_layout(barmode='group',xaxis=dict(title='Tipo di Immobile'),yaxis=dict(title='Prezzo medio al (m²)'),title=title +Comu + " in prov. di "+ Prov)
    fig4.update_traces(texttemplate='%{text:.2s}€', textposition='inside') 
    
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
                xaxis=dict(title='Prezzo minimo e massimo medio al (m²)',ticksuffix='€'),
                yaxis=dict(title='Tipo di Immobile'),
                showlegend=True,title="Prezzo minimo e massimo medio immobili del Comune di "+Comu + " in prov. di "+ Prov) 
    return "Comune di: " + Comu,fig4,fig5

if __name__ == "__main__":
    app.run_server(debug=False)








