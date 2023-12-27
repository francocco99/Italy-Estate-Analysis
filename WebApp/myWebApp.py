from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
import plotly.graph_objects as go

df=pd.read_csv('../Valori.csv',sep=';',skiprows=1)

with open("../italy-with-regions_1458.geojson") as f:
    gj = json.load(f)
features = gj['features']

with open("../province-italia.json") as f:
    pI = json.load(f)
dfPV = pd.json_normalize(pI, meta=['nome','sigla','regione'])
dfPV.drop(columns=['regione'],inplace=True)
dfPV.columns = ['name', 'Prov']

df=pd.merge(df,dfPV,on='Prov')
df.drop(columns=['Prov'],inplace=True)
df = df.rename(columns={'name': 'Prov'})
df.drop(['Comune_ISTAT','Comune_cat','LinkZona','Stato_prev','Comune_amm','Sup_NL_compr','Sup_NL_loc','Unnamed: 21'],axis=1,inplace=True)
df["Loc_min"] = df["Loc_min"].replace(',', '.', regex=True)
df["Loc_max"] = df["Loc_max"].replace(',', '.', regex=True)
df["Loc_min"]=df["Loc_min"].astype(float)
df["Loc_max"]=df["Loc_max"].astype(float)

df["Compr_min"]=df["Compr_min"].astype(float)
df["Compr_max"]=df["Compr_max"].astype(float)
df["Compr_min"]=df["Compr_min"].fillna(0)
df["Compr_max"]=df["Compr_max"].fillna(0)

df["Loc_min"]=df["Loc_min"].fillna(0)
df["Loc_max"]=df["Loc_max"].fillna(0)

MeanCompr=[]
MeanLoc=[]
###  Inutilizzato per  ora ###################
for i in df.index:
    sumC=df['Compr_min'][i]+df['Compr_max'][i]
    sumL=df['Loc_min'][i]+df['Loc_max'][i]
    mcomp=sumC/2
    mloc=sumL/2

    MeanCompr.append(mcomp)
    MeanLoc.append(mloc)
##############################################
#df["Compr"]=MeanCompr
#df["Loc"]=MeanLoc



### DIVISO PER REGIONE
#df.drop(['Compr_min','Compr_max','Loc_min','Loc_max'],axis=1,inplace=True)
df.drop(['Compr_min','Loc_min'],axis=1,inplace=True)
df.rename(columns={"Compr_max": "Compr","Loc_max": "Loc"},inplace=True)
df.loc[df["Regione"]=="VALLE D'AOSTA/VALLE`E D'AOSTE","Regione"]="VALLE D'AOSTA"
df.loc[df["Regione"]=="TRENTINO-ALTO ADIGE","Regione"]="TRENTINO-ALTO ADIGE/SUDTIROL"
df.loc[df["Regione"]=="FRIULI-VENEZIA GIULIA","Regione"]="FRIULI VENEZIA GIULIA"


regions=df["Regione"].unique().tolist()
regionsMap= ['Piemonte', 'Trentino-alto adige/sudtirol', 'Lombardia', 'Puglia', 'Basilicata', 
           'Friuli venezia giulia', 'Liguria', "Valle d'aosta", 'Emilia-romagna',
           'Molise', 'Lazio', 'Veneto', 'Sardegna', 'Sicilia', 'Abruzzo',
           'Calabria', 'Toscana', 'Umbria', 'Campania', 'Marche']
regions.sort()

regionsMap.sort()
dfR=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ].groupby("Regione").mean("Compr,Loc").reset_index()
dfR.drop(columns=["Cod_Tip"],inplace=True)
dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

dfC=df[(df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23) ].groupby("Regione").mean("Compr,Loc").reset_index()
dfC.drop(columns=["Cod_Tip"],inplace=True)
dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

dfT=df[(df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18) ].groupby("Regione").mean("Compr,Loc").reset_index()
dfT.drop(columns=["Cod_Tip"],inplace=True)
dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

dfP=df[(df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10) ].groupby("Regione").mean("Compr,Loc").reset_index()
dfP.drop(columns=["Cod_Tip"],inplace=True)
dfP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)


dfTI=pd.merge(dfR,dfC,on="Regione",how="inner")
dfTI=pd.merge(dfTI,dfT,on="Regione",how="inner")
dfTI=pd.merge(dfTI,dfP,on="Regione",how="inner")


dfTI2=dfTI.copy()
dfTI2["Regione"]=regionsMap


ListaProv=df.groupby(["Prov","Regione"]).mean("Compr,Loc").reset_index()
ListaProv=ListaProv.drop(columns=["Cod_Tip","Compr","Loc"])

#### DIVISO PER PROVINCIA
dfRp=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ].groupby("Prov").mean("Compr,Loc").reset_index()
dfRp.drop(columns=["Cod_Tip"],inplace=True)
dfRp.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

dfCp=df[(df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23) ].groupby("Prov").mean("Compr,Loc").reset_index()
dfCp.drop(columns=["Cod_Tip"],inplace=True)
dfCp.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

dfTp=df[(df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18) ].groupby("Prov").mean().reset_index()
dfTp.drop(columns=["Cod_Tip"],inplace=True)
dfTp.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

dfPp=df[(df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10) ].groupby("Prov").mean("Compr,Loc").reset_index()
dfPp.drop(columns=["Cod_Tip"],inplace=True)
dfPp.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)

dfTIp=pd.merge(dfRp,dfCp,on="Prov",how="inner")
dfTIp=pd.merge(dfTIp,dfTp,on="Prov",how="inner")
dfTIp=pd.merge(dfTIp,dfPp,on="Prov",how="inner")

#####

ListaComm=df.groupby(["Comune_descrizione","Prov","Regione"]).mean("Compr,Loc").reset_index()
ListaComm=ListaComm.drop(columns=["Cod_Tip","Compr","Loc"])
### DIVISO PER COMUNE
dfRc=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ].groupby("Comune_descrizione").mean("Compr,Loc").reset_index()
dfRc.drop(columns=["Cod_Tip"],inplace=True)
dfRc.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

dfCc=df[(df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23) ].groupby("Comune_descrizione").mean("Compr,Loc").reset_index()
dfCc.drop(columns=["Cod_Tip"],inplace=True)
dfCc.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

dfTc=df[(df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18) ].groupby("Comune_descrizione").mean("Compr,Loc").reset_index()
dfTc.drop(columns=["Cod_Tip"],inplace=True)
dfTc.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

dfPc=df[(df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10) ].groupby("Comune_descrizione").mean("Compr,Loc").reset_index()
dfPc.drop(columns=["Cod_Tip"],inplace=True)
dfPc.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)

dfTIc=pd.merge(dfRc,dfCc,on="Comune_descrizione",how="inner")
dfTIc=pd.merge(dfTIc,dfTc,on="Comune_descrizione",how="inner")
dfTIc=pd.merge(dfTIc,dfPc,on="Comune_descrizione",how="inner")


## COMUNE non diviso

Commtot=df.groupby(["Comune_descrizione","Prov","Regione"]).mean("Compr,Loc").reset_index()
Commtot=Commtot.drop(columns=["Cod_Tip"])
####



app = Dash(__name__, external_stylesheets=[])
div_style = {
    'backgroundColor': '#f2f2f2',  # Grigio
    'borderRadius': '15px',  # Bordi arrotondati
    'padding': '20px'  # Padding interno
}

# Contenuto del div
div_content = html.Div(
    [
        html.H3('Dataset OMI(Osservatorio sul mercato Immobiliare)',style={'font-family': 'sans-serif'}),
        html.P(["il Dataset contiene i dati relativi alle quotazioni immobiliari del secondo semestre del 2022. "
               "Per ogni zona territoriale delimitata di ciascun comune",html.Span("(Zona OMI)",style={'fontWeight': 'bold'}),
               ". Le quotazioni OMI, disponibili in un semestre, sono relative ai comuni censiti negli archivi catastali, , le quotazioni OMI non possono intendersi sostitutive della stima puntuale, in quanto forniscono indicazioni di valore di larga massima"
               "sono prensenti diversi dati",
               html.Ul([
            html.Li("intervallo minimo/massimo, per unità di superficie in euro a metro quadro"),
        ])],style={'font-family': 'sans-serif'}),
        # Puoi aggiungere altri componenti HTML qui
    ],
    style=div_style
)

app.layout =html.Div([
    html.H1('Analisi prezzi degli Immobili',style={ 'text-align': 'center','font-family': 'sans-serif'}),
    html.Div(div_content),
    html.H1('Prezzi degli Immobili',style={ 'text-align': 'center','font-family': 'sans-serif'}),
    dcc.RadioItems(
        id='Tipo', 
        options=[{'label': 'Residenziale', 'value': 'ComprR'},
        {'label': 'Commerciale', 'value': 'ComprC'},
        {'label': 'Terziaria', 'value': 'ComprT'},
        {'label': 'Produttiva', 'value': 'ComprP'}],
        value="ComprR",
        style={ 'text-align': 'center','font-family': 'sans-serif'},
        inline=True
    ),
    dcc.Graph(id='graph2'),
    html.P("Seleziona la Regione",style={ 'text-align': 'center','font-family': 'sans-serif'}),
    dcc.Dropdown(options=regions, value='ABRUZZO', id='Reg',style={'font-family': 'sans-serif'}),
    dcc.RadioItems(
        id='scelta', 
        options=[
        {'label': 'Compravendita', 'value': 'cmp'},
        {'label': 'Locazione', 'value': 'loc'}],
        value="cmp",
        style={ 'text-align': 'center','font-family': 'sans-serif'},
        inline=True
    ),
    html.H1(id="nameProv",style={'text-align': 'center','font-family': 'sans-serif'}),
    html.Div([
        html.Div([
            html.H2('Regione',style={'font-family': 'sans-serif','text-align': 'center'}),
            html.H3('Scegli la zona',style={'font-family': 'sans-serif','text-align': 'center'}),
            dcc.RadioItems(
                id='sezR', 
                options=[{'label':'Tutte le Zone','value':'Tutto'},
                {'label': 'Zona Centrale & Semiceltrale', 'value': 'C'},
                {'label': 'Periferica', 'value': 'D'},
                {'label': 'Suburbana', 'value': 'E'},
                {'label': 'Extraurbana', 'value': 'R'}],
                value="Tutto",
                style={ 'text-align': 'center','font-family': 'sans-serif'},
                inline=True
            ),
            #html.H2(id="ZonaStamp",style={'font-family': 'sans-serif','text-align': 'center'}),
            dcc.Graph(id='graph')
        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
        html.Div([
            html.H2('Provincia',style={'font-family': 'sans-serif','text-align': 'center'}),
            dcc.RadioItems(
                id='sezP', 
                options=[{'label':'Tutte le Zone','value':'Tutto'},
                {'label': 'Zona Centrale & Semiceltrale', 'value': 'C'},
                {'label': 'Periferica', 'value': 'D'},
                {'label': 'Suburbana', 'value': 'E'},
                {'label': 'Extraurbana', 'value': 'R'}],
                value="Tutto",
                style={ 'text-align': 'center','font-family': 'sans-serif'},
                inline=True
            ),
            dcc.Graph(id='graph3')
        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
    ], className="row"),
    html.H2('Comuni',style={'font-family': 'sans-serif','text-align': 'center'}),
    dcc.Graph(id="graph4"),
    html.P("Seleziona il comune",style={'font-family': 'sans-serif','text-align': 'center'}),
    dcc.RadioItems(
                id='sezC', 
                options=[{'label':'Tutte le Zone','value':'Tutto'},
                {'label': 'Zona Centrale & Semiceltrale', 'value': 'C'},
                {'label': 'Periferica', 'value': 'D'},
                {'label': 'Suburbana', 'value': 'E'},
                {'label': 'Extraurbana', 'value': 'R'}],
                value="Tutto",
                style={ 'text-align': 'center','font-family': 'sans-serif'},
                inline=True
    ),
    dcc.Dropdown(id='CommD',style={'font-family': 'sans-serif'}),
    html.H2(id="Com",style={'font-family': 'sans-serif','text-align': 'center'}),
    dcc.Graph(id="graph5")

])

############################# MAPPA ##############################
@app.callback(
    Output("graph2", "figure"), 
    Input("Tipo", "value"))

def display_choropleth(Tipo):
    df = dfTI2 
  
    geojson = gj
    fig = px.choropleth(
        df, geojson=geojson, color=Tipo,
        locations="Regione", featureidkey="properties.name",
        projection="mercator",labels={"ComprP":"Prezzi immobili Produttivi","ComprR":"Prezzi immobili Residenziali","ComprC":"Prezzi immobili Commerciali","ComprT":"Prezzi immobili Set. Terziario"},
        animation_frame=None,
        )
    fig.update_geos(fitbounds="locations", visible=False,center=None, projection_scale=3)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

################ CLICK ON MAP ################################
@app.callback(
    Output("graph", "figure"), 
    Output("graph3","figure"),
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

    x=["Residenziale","Commerciale","Terziaria", "Produttiva"]

    
        # Prezzi Compravendita
    if sezR=="Tutto":
        if(scelta=="cmp"):
            title="Prezzo medio Compravendita Immobili"
            y=[dfTI[dfTI["Regione"]==Region]["ComprR"].item(),dfTI[dfTI["Regione"]==Region]["ComprC"].item(),dfTI[dfTI["Regione"]==Region]["ComprT"].item(),dfTI[dfTI["Regione"]==Region]["ComprP"].item()]
        else:
            title="Prezzo medio Locazione Immobili"
            y=[dfTI[dfTI["Regione"]==Region]["LocR"].item(),dfTI[dfTI["Regione"]==Region]["LocC"].item(),dfTI[dfTI["Regione"]==Region]["LocT"].item(),dfTI[dfTI["Regione"]==Region]["LocP"].item()]
    elif sezR=="C":
        
        dfR=df[((df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ) &  ((df["Fascia"]=="C") | (df["Fascia"]=="B")) ].groupby("Regione").mean("Compr,Loc").reset_index()
        dfR.drop(columns=["Cod_Tip"],inplace=True)
        dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)
        
        dfC=df[((df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23)) &  ((df["Fascia"]=="C") | (df["Fascia"]=="B")) ].groupby("Regione").mean("Compr,Loc").reset_index()
        dfC.drop(columns=["Cod_Tip"],inplace=True)
        dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)
        
        dfT=df[((df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18)) &  ((df["Fascia"]=="C") | (df["Fascia"]=="B")) ].groupby("Regione").mean("Compr,Loc").reset_index()
        dfT.drop(columns=["Cod_Tip"],inplace=True)
        dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)
        
        dfP=df[((df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10)) &  ((df["Fascia"]=="C") | (df["Fascia"]=="B")) ].groupby("Regione").mean("Compr,Loc").reset_index()
        dfP.drop(columns=["Cod_Tip"],inplace=True)
        dfP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)

        if(scelta=="cmp"):
            title="Prezzo Medio di Compravendita Immobili in zona Centrale"
            y=[dfR[dfR["Regione"]==Region]["ComprR"].item(),dfC[dfC["Regione"]==Region]["ComprC"].item(),dfT[dfT["Regione"]==Region]["ComprT"].item(),dfP[dfP["Regione"]==Region]["ComprP"].item()]
        else:
            title="Prezzo Medio di Locazione Immobili in zona Centrale"
            y=[dfR[dfR["Regione"]==Region]["LocR"].item(),dfC[dfC["Regione"]==Region]["LocC"].item(),dfT[dfT["Regione"]==Region]["LocT"].item(),dfP[dfP["Regione"]==Region]["LocP"].item()]
    else:
        dfR=df[((df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ) &  (df["Fascia"]==sezR) ].groupby("Regione").mean("Compr,Loc").reset_index()
        dfR.drop(columns=["Cod_Tip"],inplace=True)
        dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)
    
        dfC=df[((df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23)) & (df["Fascia"]==sezR) ].groupby("Regione").mean("Compr,Loc").reset_index()
        dfC.drop(columns=["Cod_Tip"],inplace=True)
        dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)
    
        dfT=df[((df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18)) &  (df["Fascia"]==sezR) ].groupby("Regione").mean("Compr,Loc").reset_index()
        dfT.drop(columns=["Cod_Tip"],inplace=True)
        dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)
   
        dfP=df[((df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10)) &  (df["Fascia"]==sezR) ].groupby("Regione").mean("Compr,Loc").reset_index()
        dfP.drop(columns=["Cod_Tip"],inplace=True)
        dfP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)
        if(scelta=="cmp"):
            if sezR=="D":
                titlep="Prezzo Medio di Compravendita Immobili in zona Periferica"
            elif sezR=="E":
                titlep="Prezzo Medio di Compravendita Immobili in Zona Suburbana"
            elif sezR=="R":
                titlep="Prezzo Medio di Compravendita Immobili in zona Extraurbana"
            y=[dfR[dfR["Regione"]==Region]["ComprR"].item(),dfC[dfC["Regione"]==Region]["ComprC"].item(),dfT[dfT["Regione"]==Region]["ComprT"].item(),dfP[dfP["Regione"]==Region]["ComprP"].item()]
        else:
            if sezR=="D":
                titlep="Prezzo Medio di Locazione Immobili in zona Periferica"
            elif sezR=="E":
                titlep="Prezzo Medio di Locazione Immobili in Zona Suburbana"
            elif sezR=="R":
                titlep="Prezzo Medio di Locazione Immobili in zona Extraurbana"
            y=[dfR[dfR["Regione"]==Region]["LocR"].item(),dfC[dfC["Regione"]==Region]["LocC"].item(),dfT[dfT["Regione"]==Region]["LocT"].item(),dfP[dfP["Regione"]==Region]["LocP"].item()]
        # Prezzi Locazione
        
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
    dfTIpnew=dfTIp.query("Prov in @List")

    dfProv=df.query("Prov in @List")
    

    
    ### GRAFICO PROVINCIA
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
        dfR=dfProv[((dfProv["Cod_Tip"]== 20) | (dfProv["Cod_Tip"]== 19) | (dfProv["Cod_Tip"]== 1) | (dfProv["Cod_Tip"]== 14) | (dfProv["Cod_Tip"]== 15) | (dfProv["Cod_Tip"]== 21) | (dfProv["Cod_Tip"]== 13) | (dfProv["Cod_Tip"]== 22) | (dfProv["Cod_Tip"]== 16) ) & (dfProv["Fascia"]==sezR) ].groupby("Prov").mean("Compr,Loc").reset_index()
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
            titlep="Prezzo Medio di Compravendita Immobili per Province"
        elif sezP=="C":
            titlep="Prezzo Medio di Compravendita Immobili in zona Centrale per Province"
        elif sezP=="D":
            titlep="Prezzo Medio di Compravendita Immobili in zona Periferica per Province"
        elif sezP=="E":
            titlep="Prezzo Medio di Compravendita Immobili in Zona Suburbana per Province"
        elif sezP=="R":
            titlep="Prezzo Medio di Compravendita Immobili in zona Extraurbana  per Province"    

        fig2 = go.Figure(data=[
            go.Bar(name='Residenziale', x=dfR["Prov"], y=dfR["ComprR"],text=dfR["ComprR"]),
            go.Bar(name='Commerciale', x=dfC["Prov"], y=dfC["ComprC"],text=dfC["ComprC"]),
            go.Bar(name='Terziaria', x=dfT["Prov"], y=dfT["ComprT"],text=dfT["ComprT"]),
            go.Bar(name='Produttiva', x=dfP["Prov"], y=dfP["ComprP"],text=dfP["ComprP"]) 
        ])
    else:

        if sezP=="Tutto":
            titlep="Prezzo Medio di Locazione Immobili per Province"
        elif sezP=="C":
            titlep="Prezzo Medio di Locazione Immobili in zona Centrale per Province"
        elif sezP=="D":
            titlep="Prezzo Medio di Locazione Immobili in zona Periferica per Province"
        elif sezP=="E":
            titlep="Prezzo Medio di Locazione Immobili in Zona Suburbana per Province"
        elif sezP=="R":
            titlep="Prezzo Medio di Locazione Immobili in zona Extraurbana per Province"  
        fig2 = go.Figure(data=[
            go.Bar(name='Residenziale', x=dfR["Prov"], y=dfR["LocR"],text=dfR["LocR"]),
            go.Bar(name='Commerciale', x=dfC["Prov"], y=dfC["LocC"],text=dfC["LocC"]),
            go.Bar(name='Terziaria', x=dfT["Prov"], y=dfT["LocT"],text=dfT["LocT"]),
            go.Bar(name='Produttiva', x=dfP["Prov"], y=dfP["LocP"],text=dfP["LocP"]) 
        ])

# Change the bar mode
    fig2.update_layout(barmode='group',xaxis=dict(title='Province della regione '+ Region),yaxis=dict(title='Prezzo medio al (m²)'),title=titlep)
    fig2.update_traces(texttemplate='%{text:.2s}€', textposition='inside')
    return fig,fig2,ListC,Region


### DECIDERE COSA FARE ############################### GRAFICO COMUNI
@app.callback(
    Output("graph4", "figure"), 
    Input("graph2", "clickData"),
    Input("Reg", "value"), 
    Input("scelta","value")
)

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
    Comm=Commtot.query("Comune_descrizione in @List")
    if(scelta=="cmp"):
        fig3 = px.scatter(Comm,x="Compr",y="Comune_descrizione",color="Prov",labels={"Prov":"Province"})
    else:
        fig3 = px.scatter(Comm,x="Loc",y="Comune_descrizione",color="Prov",labels={"Prov":"Province"})
    
    fig3.update_yaxes(showticklabels=False)
    fig3.update_layout(title="Prezzo degli Immobili (Allzone) per i Comuni della Regione "+Region,xaxis=dict(title='Prezzo medio al (m²)'),yaxis=dict(title='Comuni'))
    return fig3


##### GRAFICO COMUNE ####################################

@app.callback(
    Output("Com", "children"), 
    Output("graph5","figure"),
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
   
    x=["Residenziale","Commerciale","Terziaria", "Produttiva"]
    if scelta=="cmp":
        if len(dfRc[dfRc["Comune_descrizione"]==Comu]["ComprR"].tolist())==0:
            Res=0
        else:
            Res=dfRc[dfRc["Comune_descrizione"]==Comu]["ComprR"].item()
        if len(dfCc[dfCc["Comune_descrizione"]==Comu]["ComprC"].tolist())==0:
            Comm=0
        else:
            Comm=dfCc[dfCc["Comune_descrizione"]==Comu]["ComprC"].item()
        if len(dfTc[dfTc["Comune_descrizione"]==Comu]["ComprT"].tolist())==0:
            Terz=0
        else:
            Terz=dfTc[dfTc["Comune_descrizione"]==Comu]["ComprT"].item()
        if len(dfPc[dfPc["Comune_descrizione"]==Comu]["ComprP"].tolist())==0:
            Prod=0
        else:
            Prod=dfPc[dfPc["Comune_descrizione"]==Comu]["ComprP"].item()
    else:
        if len(dfRc[dfRc["Comune_descrizione"]==Comu]["LocR"].tolist())==0:
            Res=0
        else:
            Res=dfRc[dfRc["Comune_descrizione"]==Comu]["LocR"].item()
        if len(dfCc[dfCc["Comune_descrizione"]==Comu]["LocC"].tolist())==0:
            Comm=0
        else:
            Comm=dfCc[dfCc["Comune_descrizione"]==Comu]["LocC"].item()
        if len(dfTc[dfTc["Comune_descrizione"]==Comu]["LocT"].tolist())==0:
            Terz=0
        else:
            Terz=dfTc[dfTc["Comune_descrizione"]==Comu]["LocT"].item()
        if len(dfPc[dfPc["Comune_descrizione"]==Comu]["LocP"].tolist())==0:
            Prod=0
        else:
            Prod=dfPc[dfPc["Comune_descrizione"]==Comu]["LocP"].item()
        
    y=[Res,Comm,Terz,Prod]
    fig4 = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
            #marker_color=colors
        )])
    # Change the bar mode
    fig4.update_layout(barmode='group')
    fig4.update_traces(texttemplate='%{text:.2s}€', textposition='inside') 
    return "Comune di: " + Comu,fig4

app.run_server(port=8052)









