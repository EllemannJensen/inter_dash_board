import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

#read in the data
df = pd.read_csv ('https://raw.githubusercontent.com/EllemannJensen/inter_dash_board/main/data/Sales_funnel.csv', sep=';')
#pivo = pd.pivot_table(df, index=['Name'], columns=["Status"], values=['Anzahl'], aggfunc=sum, fill_value=0)


# get all the managers for the dropdown 
m_options = df["Manager"].unique()

# create the app and layout
app = dash.Dash()

#colors = {
   # 'background': '#111111',
   # 'text': '#7FDBFF'
#}(style={'backgroundColor': colors['background']}, 

app.layout = html.Div(children=[
    html.H1("Monatsreport Sales Funnel"),

        html.Div(children='''
        Bitte Manager wählen:
    '''),
    
    html.Div(
        [
            dcc.Dropdown(
                id="Manager",
                options=[{
                    'label': i,
                    'value': i
                } for i in m_options],
                value='Alle Manager'),
        ],
        
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])


# wrapper for the update_graph
@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Manager', 'value')])
    
# drop down filter
def update_graph(Manager):
    if Manager == "Alle Manager":
        df_plot = df.copy()
    else:
        df_plot = df[df['Manager']== Manager]


#make a pivot table
    pi = pd.pivot_table(
        df_plot,
        index=['Kundenname'],
        columns=["Status"],
        values=['Anzahl'],
        aggfunc=sum,
        fill_value=0)

# plot the items: Trace= Abgelehnt, Gewonnen; Angebot and Ausstehend
    trace1 = go.Bar(x=pi.index, y=pi[('Anzahl', 'Abgelehnt')], name='Abgelehnt')
    trace2 = go.Bar(x=pi.index, y=pi[('Anzahl', 'Ausstehend')], name='Ausstehend')
    trace3 = go.Bar(x=pi.index, y=pi[('Anzahl', 'Angebot')], name='Angebot')
    trace4 = go.Bar(x=pi.index, y=pi[('Anzahl', 'Gewonnen')], name='Gewonnen')

#return dictionary
    return {
        'data': [trace1, trace2, trace3, trace4],
        'layout':
        go.Layout(
            title='Kundenstatus: {}'.format(Manager),
            barmode='stack')
    }

# run app
if __name__ == '__main__':
    app.run_server(debug=True)