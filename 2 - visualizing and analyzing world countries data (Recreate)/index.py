import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

tabs_styles = {'display': 'flex',
               'flex-direction': 'row'}

tab_style = {'color': '#AEAEAE',
             'backgroundColor': '#010914',
             'fontSize': '1vw',
             'padding': '1.3vh',
             'border-bottom': '1px solid white'}

selected_tab_style = {'color': '#F4F4F4',
                      'padding': '1.3vh',
                      'backgroundColor': '#566573',
                      'fontSize': '1vw',
                      'fontWeight': 'bold',
                      'border-top': '1px solid white',
                      'border-left': '1px solid white',
                      'border-right': '1px solid white'}

life_expectancy = dcc.Graph(id='line_chart1',
                            config={'displayModeBar': False}),
populations = dcc.Graph(id='line_chart2',
                        config={'displayModeBar': False}),
gdp_per_capt = dcc.Graph(id='line_chart3',
                         config={'displayModeBar': False})

life_expectancy_bar = dcc.Graph(id='line_chart4',
                                config={'displayModeBar': False}),
populations_bar = dcc.Graph(id='line_chart5',
                            config={'displayModeBar': False}),
gdp_per_capt_bar = dcc.Graph(id='line_chart6',
                             config={'displayModeBar': False})

df = pd.read_csv('data.csv')

app = dash.Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}])
server = app.server

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H5('World Countries Information 1952 - 2007', className='title_text'),

                html.Div([
                    html.P('Select Continent:', className='fix_label'),
                    dcc.Dropdown(id='select_continent',
                                 multi=False,
                                 clearable=True,
                                 disabled=False,
                                 style={'display': True},
                                 value='Asia',
                                 placeholder='Select Continent',
                                 options=[{'label': c, 'value': c}
                                          for c in df['continent'].unique()],
                                 className='dcc_component'
                                 )
                ], className='title_dropdown_column'),

                html.Div([
                    html.P('Select Countries:', className='fix_label'),
                    dcc.Dropdown(id='select_countries',
                                 multi=False,
                                 clearable=True,
                                 disabled=False,
                                 style={'display': True},
                                 placeholder='Select Continent',
                                 options=[],
                                 className='dcc_component'
                                 )
                ], className='title_dropdown_column')
            ], className='adjusts_drop_lists')
        ], className='title_container twelve columns')
    ], className='row display_flex'),

    html.Div([
        html.Div([
            dcc.Tabs(value='populations', children=[
                dcc.Tab(life_expectancy,
                        label='Life Expectancy',
                        value='life_expectancy',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        className='font_size'),
                dcc.Tab(populations,
                        label='Population',
                        value='populations',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        className='font_size'),
                dcc.Tab(gdp_per_capt,
                        label='gdpPercap',
                        value='gdppercap',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        className='font_size')
            ], style=tabs_styles, colors={'border': None,
                                          'primary': None,
                                          'background': None})

        ], className='create_container1 six columns'),
        html.Div([
            html.Div([
                html.Div(id='text1'),
                html.Div(id='text2'),
                html.Div(id='text3')
            ], className='text_columns')
        ], className='create_container2 two columns'),
        html.Div([
            dcc.Tabs(value='populations', children=[
                dcc.Tab(life_expectancy_bar,
                        label='Life Expectancy',
                        value='life_expectancy',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        className='font_size'),
                dcc.Tab(populations_bar,
                        label='Population',
                        value='populations',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        className='font_size'),
                dcc.Tab(gdp_per_capt_bar,
                        label='gdpPercap',
                        value='gdppercap',
                        style=tab_style,
                        selected_style=selected_tab_style,
                        className='font_size')
            ], style=tabs_styles, colors={'border': None,
                                          'primary': None,
                                          'background': None})

        ], className='create_container3 four columns'),
    ], className='row display_flex')

], className='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(Output('select_countries', 'options'),
              [Input('select_continent', 'value')])
def get_list_countries(select_continent):
    df1 = df[df['continent'] == select_continent]
    return [{'label': i, 'value': i} for i in df1['country'].unique()]


@app.callback(Output('select_countries', 'value'),
              [Input('select_countries', 'options')])
def get_country_value(select_countries):
    return [k['value'] for k in select_countries][0]


@app.callback(Output('line_chart1', 'figure'),
              [Input('select_continent', 'value')],
              [Input('select_countries', 'value')])
def display_chart(select_continent, select_countries):
    df1 = df.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    df2 = df1[(df1['continent'] == select_continent) & (df1['country'] == select_countries)]
    return {
        'data': [go.Scatter(
            x=df2['year'],
            y=df2['lifeExp'],
            mode='text+markers+lines',
            text=df2['lifeExp'],
            texttemplate='%{text:.0f}',
            textposition='top center',
            line=dict(width=3, color='#38D56F'),
            marker=dict(color='#38D56F', size=10, symbol='circle',
                        line=dict(width=2, color='#38D56F')),
            textfont=dict(
                family="sans-serif",
                size=12,
                color='white'),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + df2['country'].astype(str) + '<br>' +
            '<b>Year</b>: ' + df2['year'].astype(str) + '<br>' +
            '<b>Continent</b>: ' + df2['continent'].astype(str) + '<br>' +
            '<b>Life Expectancy</b>: ' + [f'{x:,.0f} year' for x in df2['lifeExp']] + '<br>'

        )],
        'layout': go.Layout(
            plot_bgcolor='#010914',
            paper_bgcolor='#010914',
            title={
                'text': 'Life Expectancy in' + ' ' + str(select_countries),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#38D56F',
                'size': 17},

            hovermode='closest',
            margin=dict(t=15, r=0),
            xaxis=dict(title='<b>Years</b>',
                       visible=True,
                       color='white',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')),
            yaxis=dict(title='<b>Life Expectancy</b>',
                       visible=True,
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')

                       ),
        )
    }


@app.callback(Output('line_chart2', 'figure'),
              [Input('select_continent', 'value')],
              [Input('select_countries', 'value')])
def display_chart(select_continent, select_countries):
    df1 = df.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    df2 = df1[(df1['continent'] == select_continent) & (df1['country'] == select_countries)]
    return {
        'data': [go.Scatter(
            x=df2['year'],
            y=df2['pop'],
            mode='text+markers+lines',
            text=df2['pop'],
            texttemplate='%{text:.2s}',
            textposition='top center',
            line=dict(width=3, color='#9A38D5'),
            marker=dict(color='#9A38D5', size=10, symbol='circle',
                        line=dict(width=2, color='#9A38D5')),
            textfont=dict(
                family="sans-serif",
                size=12,
                color='white'),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + df2['country'].astype(str) + '<br>' +
            '<b>Year</b>: ' + df2['year'].astype(str) + '<br>' +
            '<b>Continent</b>: ' + df2['continent'].astype(str) + '<br>' +
            '<b>Population</b>: ' + [f'{x:,.0f}' for x in df2['pop']] + '<br>'

        )],
        'layout': go.Layout(
            plot_bgcolor='#010914',
            paper_bgcolor='#010914',
            title={
                'text': 'Population in' + ' ' + str(select_countries),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#9A38D5',
                'size': 17},

            hovermode='closest',
            margin=dict(t=15, r=0),
            xaxis=dict(title='<b>Years</b>',
                       visible=True,
                       color='white',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')),
            yaxis=dict(title='Population</b>',
                       visible=True,
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')

                       ),
        )
    }


@app.callback(Output('line_chart3', 'figure'),
              [Input('select_continent', 'value')],
              [Input('select_countries', 'value')])
def display_chart(select_continent, select_countries):
    df1 = df.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    df2 = df1[(df1['continent'] == select_continent) & (df1['country'] == select_countries)]
    return {
        'data': [go.Scatter(
            x=df2['year'],
            y=df2['gdpPercap'],
            mode='text+markers+lines',
            text=df2['gdpPercap'],
            texttemplate='%{text:.0f}',
            textposition='top center',
            line=dict(width=3, color='#FFA07A'),
            marker=dict(color='#FFA07A', size=10, symbol='circle',
                        line=dict(width=2, color='#FFA07A')),
            textfont=dict(
                family="sans-serif",
                size=12,
                color='white'),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + df2['country'].astype(str) + '<br>' +
            '<b>Year</b>: ' + df2['year'].astype(str) + '<br>' +
            '<b>Continent</b>: ' + df2['continent'].astype(str) + '<br>' +
            '<b>gdpPercap</b>: ' + [f'{x:,.0f}' for x in df2['gdpPercap']] + '<br>'

        )],
        'layout': go.Layout(
            plot_bgcolor='#010914',
            paper_bgcolor='#010914',
            title={
                'text': 'gdpPercap in' + ' ' + str(select_countries),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#FFA07A',
                'size': 17},

            hovermode='closest',
            margin=dict(t=15, r=0),
            xaxis=dict(title='<b>Years</b>',
                       visible=True,
                       color='white',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')),
            yaxis=dict(title='gdpPercap</b>',
                       visible=True,
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')

                       ),
        )
    }


@app.callback(Output('text1', 'children'),
              [Input('select_continent', 'value')])
def display_chart(select_continent):
    df1 = df.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    df2 = df1[df1['continent'] == select_continent].nlargest(1, columns=['pop'])
    top_continent = df2['continent'].iloc[0]
    top_country = df2['country'].iloc[0]
    top_pop = df2['pop'].iloc[0]

    return [
        html.H6('Top country by population in' + ' ' + top_continent,
                style={'textAlign': 'center',
                       'line-height': '1',
                       'color': '#006fe6',
                       'margin-top': '15px'}),
        html.P('Country:' + ' ' + top_country,
               style={'textAlign': 'center',
                      'color': 'orange',
                      'fontSize': 15,
                      'margin-top': '20px'}),
        html.P('Population:' + ' ' + '{0:,.0f}'.format(top_pop),
               style={'textAlign': 'center',
                      'color': 'orange',
                      'fontSize': 15,
                      'margin-top': '-10px'})
    ]


@app.callback(Output('text2', 'children'),
              [Input('select_continent', 'value')])
def display_chart(select_continent):
    df1 = df.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    df2 = df1[df1['continent'] == select_continent].nlargest(1, columns=['lifeExp'])
    top_continent = df2['continent'].iloc[0]
    top_country = df2['country'].iloc[0]
    top_pop = df2['lifeExp'].iloc[0]

    return [
        html.H6('Top country by Life expectancy in' + ' ' + top_continent,
                style={'textAlign': 'center',
                       'line-height': '1',
                       'color': '#006fe6',
                       'margin-top': '15px'}),
        html.P('Country:' + ' ' + top_country,
               style={'textAlign': 'center',
                      'color': 'orange',
                      'fontSize': 15,
                      'margin-top': '20px'}),
        html.P('Life expectancy:' + ' ' + '{0:,.0f}'.format(top_pop),
               style={'textAlign': 'center',
                      'color': 'orange',
                      'fontSize': 15,
                      'margin-top': '-10px'})
    ]


@app.callback(Output('text3', 'children'),
              [Input('select_continent', 'value')])
def display_chart(select_continent):
    df1 = df.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    df2 = df1[df1['continent'] == select_continent].nlargest(1, columns=['gdpPercap'])
    top_continent = df2['continent'].iloc[0]
    top_country = df2['country'].iloc[0]
    top_pop = df2['gdpPercap'].iloc[0]

    return [
        html.H6('Top country by gdpPercap in' + ' ' + top_continent,
                style={'textAlign': 'center',
                       'line-height': '1',
                       'color': '#006fe6',
                       'margin-top': '15px'}),
        html.P('Country:' + ' ' + top_country,
               style={'textAlign': 'center',
                      'color': 'orange',
                      'fontSize': 15,
                      'margin-top': '20px'}),
        html.P('gdpPercap:' + ' ' + '{0:,.0f}'.format(top_pop),
               style={'textAlign': 'center',
                      'color': 'orange',
                      'fontSize': 15,
                      'margin-top': '-10px'})
    ]


@app.callback(Output('line_chart4', 'figure'),
              [Input('select_continent', 'value')])
def display_chart(select_continent):
    df1 = df.groupby(['country', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    df2 = df1[df1['continent'] == select_continent].nlargest(10, columns=['lifeExp'])
    return {
        'data': [go.Bar(
            x=df2['lifeExp'],
            y=df2['country'],
            text=df2['lifeExp'],
            texttemplate='%{text:.0f}',
            textposition='auto',
            orientation='h',
            marker=dict(color='#38D56F'),
            textfont=dict(
                family="sans-serif",
                size=12,
                color='white'),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + df2['country'].astype(str) + '<br>' +
            '<b>Continent</b>: ' + df2['continent'].astype(str) + '<br>' +
            '<b>Life Expectancy</b>: ' + [f'{x:,.0f} year' for x in df2['lifeExp']] + '<br>'

        )],
        'layout': go.Layout(
            plot_bgcolor='#010914',
            paper_bgcolor='#010914',
            title={
                'text': 'Top countries by Life Expectancy in' + ' ' + str(select_continent),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#38D56F',
                'size': 17},

            hovermode='closest',
            margin=dict(t=35, r=0, l=130),
            xaxis=dict(title='<b>Life Expectancy</b>',
                       visible=True,
                       color='white',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')),
            yaxis=dict(title='<b></b>',
                       autorange='reversed',
                       visible=True,
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')

                       ),
        )
    }


@app.callback(Output('line_chart5', 'figure'),
              [Input('select_continent', 'value')])
def display_chart(select_continent):
    df1 = df.groupby(['country', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    df2 = df1[df1['continent'] == select_continent].nlargest(10, columns=['pop'])
    return {
        'data': [go.Bar(
            x=df2['pop'],
            y=df2['country'],
            text=df2['pop'],
            texttemplate='%{text:.2s}',
            textposition='auto',
            orientation='h',
            marker=dict(color='#9A38D5'),
            textfont=dict(
                family="sans-serif",
                size=12,
                color='white'),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + df2['country'].astype(str) + '<br>' +
            '<b>Continent</b>: ' + df2['continent'].astype(str) + '<br>' +
            '<b>Population</b>: ' + [f'{x:,.0f}' for x in df2['pop']] + '<br>'

        )],
        'layout': go.Layout(
            plot_bgcolor='#010914',
            paper_bgcolor='#010914',
            title={
                'text': 'Top countries by Population in' + ' ' + str(select_continent),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#9A38D5',
                'size': 17},

            hovermode='closest',
            margin=dict(t=35, r=0, l=130),
            xaxis=dict(title='<b>Population</b>',
                       visible=True,
                       color='white',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')),
            yaxis=dict(title='<b></b>',
                       autorange='reversed',
                       visible=True,
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')

                       ),
        )
    }


@app.callback(Output('line_chart6', 'figure'),
              [Input('select_continent', 'value')])
def display_chart(select_continent):
    df1 = df.groupby(['country', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    df2 = df1[df1['continent'] == select_continent].nlargest(10, columns=['gdpPercap'])
    return {
        'data': [go.Bar(
            x=df2['gdpPercap'],
            y=df2['country'],
            text=df2['gdpPercap'],
            texttemplate='%{text:,.0f}',
            textposition='auto',
            orientation='h',
            marker=dict(color='#FFA07A'),
            textfont=dict(
                family="sans-serif",
                size=12,
                color='white'),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + df2['country'].astype(str) + '<br>' +
            '<b>Continent</b>: ' + df2['continent'].astype(str) + '<br>' +
            '<b>gdpPercap</b>: ' + [f'{x:,.0f}' for x in df2['gdpPercap']] + '<br>'

        )],
        'layout': go.Layout(
            plot_bgcolor='#010914',
            paper_bgcolor='#010914',
            title={
                'text': 'Top countries by gdpPercap in' + ' ' + str(select_continent),

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#FFA07A',
                'size': 17},

            hovermode='closest',
            margin=dict(t=35, r=0, l=130),
            xaxis=dict(title='<b>gdpPercap</b>',
                       visible=True,
                       color='white',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')),
            yaxis=dict(title='<b></b>',
                       autorange='reversed',
                       visible=True,
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white')

                       ),
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
