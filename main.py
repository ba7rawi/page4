from dash import dcc, html
import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd 
import dash_daq as daq


df = pd.read_csv('EMSdataset.csv')
df_diff = df.drop(columns=['Date/time']).diff()
df_diff.insert(0, 'Date/time' ,df['Date/time'])
df_diff = df_diff.iloc[1:,:]
df = df_diff
df['Date/time'] = pd.to_datetime(df['Date/time'])
df['Date'] = pd.to_datetime(df['Date/time']).dt.date
df['day'] = df['Date/time'].dt.day

MIN_VAL, MAX_VAL = 0, 55000
COLOR_RANGES = {
    "green":[MIN_VAL,MAX_VAL],
    # "yellow":[MAX_VAL*0.6,MAX_VAL*0.8],
    # "red":[MAX_VAL*0.8,MAX_VAL]
    }

fontawesome_stylesheet = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(
    __name__,
    suppress_callback_exceptions = True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, fontawesome_stylesheet],
 
    )


def gauge(column):
    temp = df.copy()
    temp = temp[temp['Date/time'].dt.month_name() == 'June']
    val = temp[column].sum()
    return val, f'{column} sum is: {val}'

def grouped_barchart():
    animals=['Electrical', 'Water', 'Gas']
    generators = [g for g in df.columns if g.startswith('Gen')]    
    g_vals = df[generators].sum()
    fig = go.Figure(data=[
        go.Bar(name='cost center1', x=animals, y=g_vals[:3]),
        go.Bar(name='cost center2', x=animals, y=g_vals[3:6]),
        go.Bar(name='cost center3', x=animals, y=[500000, 600000, 700000]),
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    return fig


def multi_barcharts():
    temp = df.copy()
    slct_month = 'June'
    temp_m = temp[temp['Date/time'].dt.month_name() == slct_month]
    days = temp_m.day.unique()
    data = []
    col1 = "Generator1"
    col2="Generator2"
    data.append( go.Bar(name=col1, x=days, y=temp_m.groupby(['day'])[col1].sum()))
    fig = go.Figure()

    fig.add_bar(
        name=col1, 
        x=days, 
        y=temp_m.groupby(['day'])[col1].sum(),
        marker_color='rgb(71,192,190)',
    )
    fig.add_bar(
        name=col2, 
        x=days, 
        y=temp_m.groupby(['day'])[col2].sum(),
        marker_color='rgb(193,196,182)'
    )

    fig.add_trace(go.Scatter(
        x=days,
        y=temp_m.groupby(['day'])[col1].sum(),
        mode='lines+markers',
        marker_color = 'rgb(37,139,139)'
        
    ))

    fig.add_scatter(
        x=days,
        y=temp_m.groupby(['day'])[col2].sum(),
        mode='lines+markers',
        marker_color='rgb(149,146,129)'

    )
    # Change the bar mode
    fig.update_layout(
        xaxis=dict(
                title='Xaxis Name',
                tickmode='linear')
            )
    fig.update_layout(showlegend=False)


    return fig


app.layout = html.Div([
    dbc.Row([
        html.H1(id='gauges_app', children=['Generators energy demo'], style={'textAlign':'center', 'marginBottom':'5vh'}),
    ]),
    dbc.Row([
        dbc.Col([
            daq.Gauge(
                id='gauge1',
                color='green',
                # color={"gradient":True,"ranges":COLOR_RANGES},

                value=gauge('Generator1')[0],
                label=gauge('Generator1')[1],
                max=55000,
                min=0,

                
            )
        ], xs=12, sm=12, md=12, lg=4, xl=4, style={'paddingBottom':'5vh'}),
        dbc.Col([
            daq.Gauge(
                id='gauge2',
                color='green',
                # color={"gradient":True,"ranges":COLOR_RANGES},
                value=gauge('Generator2')[0],
                label=gauge('Generator2')[1],
                max=55000,
                min=0,
                
            )
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            daq.Gauge(
                id='gauge3',
                color='green',
                # color={"gradient":True,"ranges":COLOR_RANGES},
                value=gauge('Generator3')[0],
                label=gauge('Generator3')[1],
                max=55000,
                min=0,
                
            )
        ], xs=12, sm=12, md=12, lg=4, xl=4),

    ]),
    dbc.Row([
        dbc.Col([
            html.Label(id='l1', children=["Min. Power Demand"]),
        ]),
        dbc.Col([
            dcc.Input(id='i1', value="0.747 kW", disabled=True, className="form-control"),
        ]),
        dbc.Col([
            html.Label(id='l2', children=["Max. Power Demand"]),

        ]),
        dbc.Col([
            dcc.Input(id='i2', value="8.543 kW", disabled=True, className="form-control"),
        ]),
        dbc.Col([
            html.Label(id='l3', children=["Date Range"]),

        ]),
         dbc.Col([
            dcc.Input(id='i3', value="2021-06-01 - 2021-06-30", disabled=True, className="form-control"),
        ]),


    ], style={'marginBottom':'3vh'}),
    dbc.Row([
        dbc.Col([
            html.Label(id='l4', children=["Time of use"]),
        ]),
        dbc.Col([
            dcc.Input(id='i4', value="92:43 (HH:mm)", disabled=True, className="form-control"),
        ]),
         dbc.Col([
            html.Label(id='l5', children=["Usage percentage"]),

        ]),
        dbc.Col([
            dcc.Input(id='i5', value="11%", disabled=True, className="form-control"),
        ]),
        dbc.Col([
            html.Label(id='l6', children=["Reference"]),

        ]),
         dbc.Col([
            dcc.Input(id='i6', value="2021-05-01", disabled=True, className="form-control"),
        ]),

    ], style={'marginBottom':'3vh'}),
    dbc.Row([
        dcc.Graph(id='barchart', figure = multi_barcharts())
    ]),
    
], style={'padding':'5vh'})


if __name__ == '__main__':
    app.run_server(debug=True, threaded= True)
