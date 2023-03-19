import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


election = pd.read_csv('president_county_candidate.csv')


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div((

    html.Div([
        html.Div([
            html.Div([
                html.H3('US Election 2020', style = {'margin-bottom': '0px', 'color': 'black'}),
            ])
        ], className = "create_container1 four columns", id = "title"),

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}),


    html.Div([
        html.Div([
            html.P('Select State:', className = 'fix_label', style = {'color': 'black'}),
            dcc.RadioItems(id = 'radio_items',
                           labelStyle = {"display": "inline-block"},
                           value = 'Delaware',
                           options = [{'label': i, 'value': i} for i in election['state'].unique()],
                           style = {'text-align': 'center'}, className = 'dcc_compon'),
            html.P('Select County:', className = 'fix_label', style = {'color': 'black', 'margin-top': '30px'}),
            dcc.Dropdown(id = 'select_county',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         placeholder = 'Select Countries',
                         options = [], className = 'dcc_compon')

        ], className = "create_container2 five columns"),




        html.Div([
            dcc.Graph(id = 'bar_chart',
                      config = {'displayModeBar': 'hover'}),

        ], className = "create_container2 seven columns"),

    ], className = "row flex-display"),

), id= "mainContainer", style={"display": "flex", "flex-direction": "column"})

@app.callback(
    Output('select_county', 'options'),
    Input('radio_items', 'value'))
def get_county_options(radio_items):
    election1 = election[election['state'] == radio_items]
    return [{'label': k, 'value': k} for k in election1['county'].unique()]

@app.callback(
    Output('select_county', 'value'),
    Input('select_county', 'options'))
def get_county_value(select_county):
    return [k['value'] for k in select_county][2]


@app.callback(Output('bar_chart', 'figure'),
              [Input('radio_items', 'value')],
              [Input('select_county', 'value')])
def update_graph(radio_items, select_county):
    election2 = election.groupby(['state', 'county', 'candidate', 'won'])['total_votes'].sum().reset_index()
    election3 = election2[(election2['state'] == radio_items) & (election2['county'] == select_county)]



    return {
        'data':[go.Bar(
                    x=election3['candidate'],
                    y=election3['total_votes'],
                    text = election3['total_votes'],
                    texttemplate = 'Total votes: ' + '%{text:.2s}',
                    textposition = 'auto',
                    marker = dict(
                    color = election3['total_votes'],
                    colorscale = 'phase',
                    showscale = False),

                  hoverinfo='text',
                  hovertext=
                  '<b>State</b>: ' + election3['state'].astype(str) + '<br>' +
                  '<b>County</b>: ' + election3['county'] + '<br>' +
                  '<b>Candidate</b>: ' + election3['candidate'].astype(str) + '<br>' +
                  '<b>Total Votes</b>: ' + [f'{x:,.0f}' for x in election3['total_votes']] + '<br>' +
                  '<b>Won</b>: ' + election3['won'].astype(str) + '<br>'


              )],


        'layout': go.Layout(
            barmode = 'group',
             plot_bgcolor='#F2F2F2',
             paper_bgcolor='#F2F2F2',
             title={
                'text': 'State (' + (radio_items) + ')' + ' ' + ':' + ' ' + 'County (' + (select_county) + ')',

                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'rgb(50, 50, 50)',
                        'size': 15},

             hovermode='x',

             xaxis=dict(title='<b>Candidate</b>',
                        color='rgb(50, 50, 50)',
                        showline=True,
                        showgrid=True,
                        linecolor='rgb(50, 50, 50)',
                        linewidth=1,


                ),

             yaxis=dict(title='<b>Total Votes</b>',
                        color='rgb(50, 50, 50)',
                        showline=False,
                        showgrid=True,
                        linecolor='rgb(50, 50, 50)',

                ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'rgb(50, 50, 50)'),

            uniformtext_mode = 'hide',
            uniformtext_minsize = 15,



                 )

    }


if __name__ == '__main__':
    app.run_server(debug=True)