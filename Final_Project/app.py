# -*- coding: utf-8 -*-

"""DATA 608 Final Project
   Ahsanul Choudhury"""


""" Raw Data was collected from source, cleaned and manipulated in R and uploaded
 to GitHub. Please find the accompanying final.rmd file to review data manipulation.
"""

   
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

# Load Bootstrap CSS and its components.
app.css.append_css({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
})

app.css.append_css({
    "external_url": 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.scripts.append_script({
    "external_url": "https://code.jquery.com/jquery-3.2.1.min.js"
})

app.scripts.append_script({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
})


# Load cleaned data from GitHub
df = pd.read_csv('https://raw.githubusercontent.com/choudhury1023/DATA-608/master/Final_Project/df1.csv')

df1 = pd.read_csv('https://raw.githubusercontent.com/choudhury1023/DATA-608/master/Final_Project/2016_typef.csv')

df2 = pd.read_csv('https://raw.githubusercontent.com/choudhury1023/DATA-608/master/Final_Project/compare.csv')

# Plotly United States Choropleth Map

for col in df.columns:
    df[col] = df[col].astype(str)

df['text'] = df['state'] + '<br>' +\
    df['hate crimes']

scl = [[0.0, 'rgb(255,204,204)'],[0.2, 'rgb(255,153,153)'],[0.4, 'rgb(255,102,102)'],\
            [0.6, 'rgb(255,51,51)'],[0.8, 'rgb(255,0,0)'],[1.0, 'rgb(204,0,0)']]


data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = df['code'],
        z = df['hate crimes'].astype(float),
        locationmode = 'USA-states',
        text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "Incident <br> Reported")
        ) ]

layout = dict(
        title = 'Total Number of Hate Crimes Reported by States<br>in 2016<br>(Hover Over Map)',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data, layout=layout )


# Pie Chart

state_select = df1['state'].unique()

app.config['suppress_callback_exceptions']=True

@app.callback(
    dash.dependencies.Output('pie', 'figure'),
    [dash.dependencies.Input('state', 'value')
     ])
     

def update_figure(state):
    if state == "all states":
        df_plot = df1.copy()
    else:
        df_plot = df1[df1['state'] == state]

        label= df_plot['variable']
        values =df_plot['value']
        trace = go.Pie(labels=label, values=values)

        return{
            'data': [trace],
        'layout':
        go.Layout(
            title='2016 Hate Crimes by Type {} <br> (Use the Dropdown Menu Above <br> to Change State)'.format(state))           
            }

# Bar Plot

change_select = df2["change"].unique()
app.config['suppress_callback_exceptions']=True


@app.callback(
    dash.dependencies.Output('bar-graph', 'figure'),
    [dash.dependencies.Input('change', 'value')
     ])


def update_graph(change):
    if change == "all change":
        df_plot1 = df2.copy()
    else:
        df_plot1 = df2[df2['change'] == change]

         

    trace1 = go.Bar(x=df_plot1['state'], y=df_plot1['avg_hatecrimes_per_100k_fbi_2010to2015'], name='Avg Annual Hate Crimes <br> Per 100k 2010-2015')
    trace2 = go.Bar(x=df_plot1['state'], y=df_plot1['avg_hatecrimes_per_100k_fbi_2016'], name='Hate Crimes Per 100k 2016')

    return{
        'data' : [trace1, trace2],
        'layout' :
        go.Layout(
            barmode='grouped'
            )}



# App Layout

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Hate Crimes in US',  className='text-center')
            ], className="col-md-12")
        ], className="row"),

    html.Div([
        html.Div([
            dcc.Graph(
                id='us-map',
                figure= fig)
            ],className="col-md-7"),
        html.Div([
            dcc.Dropdown(
                id='state',
                options=[{'label': i,
                          'value': i
                          } for i in state_select],
                value='Alabama'),
            dcc.Graph(id='pie')
            ],className="col-md-5")
        ], className="row"),
    html.Div([
        html.Div([
        html.H6('Comparison of Hate Crimes per 100,000 Population Between 2010-2015 Annual Average and 2016 by States',  className='text-center')
        ], className="col-md-12")
        ], className="row"),
    html.Div([
        html.Div([
            dcc.RadioItems(
                id="change",
                options=[{
                    'label': i,
                    'value': i
                    } for i in change_select],
                value='all change'),
            dcc.Graph(id='bar-graph')
            ],className="col-md-12")
        ], className="row"),
    html.Div([
    html.Div([
        dcc.Markdown('''
###### *Data Sources:*

[FBI 2016 Hate Crime Statistics](https://ucr.fbi.gov/hate-crime/2016/tables/table-11).

[2010-2015 Hate Crime Data FBI - FiveThirtyEight](https://github.com/fivethirtyeight/data/blob/master/hate-crimes/hate_crimes.csv).

[2016 US State Population Data](https://www.census.gov/data/datasets/2016/demo/popest/state-total.html)


###### *GitHub Link for Code:*

[Ahsanul Choudhury Data 608 Fall 2017 Final Project](https://github.com/choudhury1023/DATA-608/tree/master/Final_Project)
''')
               ],className="col-md-12")
        ], className="row")    
    ], className="container-fluid")
                    
            
if __name__ == '__main__':
    app.run_server(debug=True)


""" References:
     https://plot.ly/python/choropleth-maps/
     http://pbpython.com/plotly-dash-intro.html
     https://timothyrenner.github.io/datascience/2017/08/10/finding-bigfoot-with-dash-part-3.html
"""

