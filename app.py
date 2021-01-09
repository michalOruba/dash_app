import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas as pd
import os
import plotly.express as px

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

df = pd.read_csv('DANEOczyszczone.tsv', sep='\t')

colors = {
        'Dolnoslaskie': 'rgb(179,226,205)',
        'Kujawsko-Pomorskie': 'rgb(253,205,172)',
        'Lubelskie': 'rgb(203,213,232)',
        'Lubuskie': 'rgb(244,202,228)',
        'Lodzkie': 'rgb(230,245,201)',
        'Malopolskie': 'rgb(255,242,174)',
        'Mazowieckie': 'rgb(241,226,204)',
        'Opolskie': 'rgb(204,204,204)',
        'Podkarpackie': 'rgb(228,26,28)',
        'Podlaskie': 'rgb(55,126,184)',
        'Pomorskie': 'rgb(77,175,74)',
        'Slaskie': 'rgb(152,78,163)',
        'Swietokrzyskie': 'rgb(255,127,0)',
        'Warminsko-Mazurskie': 'rgb(255,255,51)',
        'Wielkopolskie': 'rgb(166,86,40)',
        'Zachodniopomorskie': 'rgb(247,129,191)'
}

pollution_colors = {
    'tlenki_azotu': 'rgb(141,211,199)',
    'tlenek_wegla': 'rgb(255,255,179)',
    'podtlenek_azotu': 'rgb(190,186,218)',
    'dwutlenek_siarki': 'rgb(251,128,114)',
    'dwutlenek_wegla': 'rgb(128,177,211)',
    'metan': 'rgb(253,180,98)',
    'nie_zorganizowana': 'rgb(179,222,105)'
}

    
voivodeships = {
        'Dolnoslaskie': 'Dolnośląskie',
        'Kujawsko-Pomorskie': 'Kujawsko-Pomorskie',
        'Lubelskie': 'Lubelskie',
        'Lubuskie': 'Lubuskie',
        'Lodzkie': 'Łódzkie',
        'Malopolskie': 'Małopolskie',
        'Mazowieckie': 'Mazowieckie',
        'Opolskie': 'Opolskie',
        'Podkarpackie': 'Podkarpackie',
        'Podlaskie': 'Podlaskie',
        'Pomorskie': 'Pomorskie',
        'Slaskie': 'Śląskie',
        'Swietokrzyskie': 'Świętokrzyskie',
        'Warminsko-Mazurskie': 'Warmińsko-Mazurskie',
        'Wielkopolskie': 'Wielkopolskie',
        'Zachodniopomorskie': 'Zachodniopomorskie'
}

pollutions = {
    'tlenki_azotu': 'Tlenki azotu',
    'tlenek_wegla': 'Tlenek węgla',
    'podtlenek_azotu': 'Podtlenek azotu',
    'dwutlenek_siarki': 'Dwutlenek siarki',
    'dwutlenek_wegla': 'Dwutlenek węgla',
    'metan': 'Metan',
    'nie_zorganizowana': 'Nie zorganizowana'
}

external_stylesheets = ['https://fonts.googleapis.com/css?family=Raleway:400,700&display=swap', 'style.css']

app = dash.Dash('Zanieczyszczenie powietrza a nowotwory', server=server, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.Header([
        html.H1('Zanieczyszczenie powietrza a nowotwory'),
        html.H3('Zależności pomiędzy zanieczyszczeniem środowiska a zgonami spowodowanymi nowotworami.'),    
    ]), 
    html.Div([
        html.Div([
            html.H2('Wybierz zanieczyszczenie:', style={'text-align': 'center', 'margin-top': '20px'}),
            html.Div(dcc.Dropdown(
                id='pollution_selector',
                options=[
                    {'label': 'Dwutlenek węgla', 'value': 'dwutlenek_wegla'},
                    {'label': 'Tlenek węgla', 'value': 'tlenek_wegla'},
                    {'label': 'Tlenki azotu', 'value': 'tlenki_azotu'},
                    {'label': 'Podtlenek azotu', 'value': 'podtlenek_azotu'},
                    {'label': 'Dwutlenek siarki', 'value': 'dwutlenek_siarki'},
                    {'label': 'Metan', 'value': 'metan'},
                    {'label': 'Nie zorganizowana', 'value': 'nie_zorganizowana'}
                ],
                value='dwutlenek_wegla'
            ),  style={
                        'width': '20%', 
                        'padding': '0px 20px 20px 20px', 
                        'margin': '20px auto'})
        ]),
        html.Div([
            dcc.Graph(
                id='scatter',
                style={'width': '50%', 'margin': '20px auto'}
            )
        ]),
        html.Div([
            html.H2('Wybierz rok:', style={'text-align': 'center', 'margin-top': '20px'}),
            html.Div(dcc.Slider(
                id='year_selector',
                min=df['Rok'].min(),
                max=df['Rok'].max(),
                marks={str(year): str(year) for year in df['Rok'].unique()},
                value=df['Rok'].min(),
                step=None
            ),  style={
                        'width': '49%', 
                        'padding': '0px 20px 20px 20px', 
                        'margin': '20px auto'})
        ]),
        html.Div([
            html.H2('Wybierz zanieczyszczenie:', style={'text-align': 'center', 'margin-top': '20px'}),
            html.Div(dcc.Dropdown(
                id='pollution_selector_bar',
                options=[
                    {'label': 'Dwutlenek węgla', 'value': 'dwutlenek_wegla'},
                    {'label': 'Tlenek węgla', 'value': 'tlenek_wegla'},
                    {'label': 'Tlenki azotu', 'value': 'tlenki_azotu'},
                    {'label': 'Podtlenek azotu', 'value': 'podtlenek_azotu'},
                    {'label': 'Dwutlenek siarki', 'value': 'dwutlenek_siarki'},
                    {'label': 'Metan', 'value': 'metan'},
                    {'label': 'Nie zorganizowana', 'value': 'nie_zorganizowana'}
                ],
                value='dwutlenek_wegla'
            ),  style={
                        'width': '20%', 
                        'padding': '0px 20px 20px 20px', 
                        'margin': '20px auto'})
        ], style={'margin-top': '60px'}),
        html.Div([
            html.Div([
                html.H2('Wybierz województwo:', style={'text-align': 'center', 'margin': '20px 0'}),
                html.Div(dcc.RadioItems(
                    id='voivodeship_selector',
                    options=[
                        {'label': 'Dolnośląskie', 'value': 'Dolnoslaskie'},
                        {'label': 'Kujawsko-Pomorskie', 'value': 'Kujawsko-Pomorskie'},
                        {'label': 'Lubelskie', 'value': 'Lubelskie'},
                        {'label': 'Lubuskie', 'value': 'Lubuskie'},
                        {'label': 'Łódzkie', 'value': 'Lodzkie'},
                        {'label': 'Małopolskie', 'value': 'Malopolskie'},
                        {'label': 'Mazowieckie', 'value': 'Mazowieckie'},
                        {'label': 'Opolskie', 'value': 'Opolskie'},
                        {'label': 'Podkarpackie', 'value': 'Podkarpackie'},
                        {'label': 'Podlaskie', 'value': 'Podlaskie'},
                        {'label': 'Pomorskie', 'value': 'Pomorskie'},
                        {'label': 'Śląskie', 'value': 'Slaskie'},
                        {'label': 'Świętokrzyskie', 'value': 'Swietokrzyskie'},
                        {'label': 'Warmińsko-Mazurskie', 'value': 'Warminsko-Mazurskie'},
                        {'label': 'Wielkopolskie', 'value': 'Wielkopolskie'},
                        {'label': 'Zachodniopomorskie', 'value': 'Zachodniopomorskie'}
                    ],
                    value='Dolnoslaskie',
                    labelStyle={'display': 'block'},
                    inputStyle={"margin-right": "5px"}
                ))
            ],  style={
                        'width': '20%', 
                        'padding': '0px 20px 20px 20px', 
                        'display': 'inline-block',
                        'margin-right': '0'}),
                
            html.Div(
                dcc.Graph(
                    id='bar'
            ), style={'width': '50%', 'display': 'inline-block', 'padding': '0 20', 'margin-left': '0'})
        ], className='container'),
                
        html.Div([
            html.H2('Wybierz zanieczyszczenie:', style={'text-align': 'center', 'margin-top': '20px'}),
            html.Div(dcc.Dropdown(
                id='pollution_selector_line',
                options=[
                    {'label': 'Dwutlenek węgla', 'value': 'dwutlenek_wegla'},
                    {'label': 'Tlenek węgla', 'value': 'tlenek_wegla'},
                    {'label': 'Tlenki azotu', 'value': 'tlenki_azotu'},
                    {'label': 'Podtlenek azotu', 'value': 'podtlenek_azotu'},
                    {'label': 'Dwutlenek siarki', 'value': 'dwutlenek_siarki'},
                    {'label': 'Metan', 'value': 'metan'},
                    {'label': 'Nie zorganizowana', 'value': 'nie_zorganizowana'}
                ],
                value='dwutlenek_wegla'
            ),  style={
                        'width': '20%', 
                        'padding': '0px 20px 20px 20px', 
                        'margin': '20px auto'})
        ], style={'margin-top': '60px'}),
        html.Div([
            html.Div([
                html.H2('Wybierz województwa do porównania:', style={'text-align': 'center', 'margin': '20px 0'}),
                html.Div([
                    html.Div(dcc.RadioItems(
                        id='voivodeship_selector_compare_1',
                        options=[
                            {'label': 'Dolnośląskie', 'value': 'Dolnoslaskie'},
                            {'label': 'Kujawsko-Pomorskie', 'value': 'Kujawsko-Pomorskie'},
                            {'label': 'Lubelskie', 'value': 'Lubelskie'},
                            {'label': 'Lubuskie', 'value': 'Lubuskie'},
                            {'label': 'Łódzkie', 'value': 'Lodzkie'},
                            {'label': 'Małopolskie', 'value': 'Malopolskie'},
                            {'label': 'Mazowieckie', 'value': 'Mazowieckie'},
                            {'label': 'Opolskie', 'value': 'Opolskie'},
                            {'label': 'Podkarpackie', 'value': 'Podkarpackie'},
                            {'label': 'Podlaskie', 'value': 'Podlaskie'},
                            {'label': 'Pomorskie', 'value': 'Pomorskie'},
                            {'label': 'Śląskie', 'value': 'Slaskie'},
                            {'label': 'Świętokrzyskie', 'value': 'Swietokrzyskie'},
                            {'label': 'Warmińsko-Mazurskie', 'value': 'Warminsko-Mazurskie'},
                            {'label': 'Wielkopolskie', 'value': 'Wielkopolskie'},
                            {'label': 'Zachodniopomorskie', 'value': 'Zachodniopomorskie'}
                        ],
                        value='Dolnoslaskie',
                        labelStyle={'display': 'block'},
                        inputStyle={"margin-right": "5px"}
                    ), style={'width': '40%', 'display': 'inline-block', 'padding': '0 20', 'margin-right': '0'}),
                    
                    html.Div(dcc.RadioItems(
                        id='voivodeship_selector_compare_2',
                        options=[
                            {'label': 'Dolnośląskie', 'value': 'Dolnoslaskie'},
                            {'label': 'Kujawsko-Pomorskie', 'value': 'Kujawsko-Pomorskie'},
                            {'label': 'Lubelskie', 'value': 'Lubelskie'},
                            {'label': 'Lubuskie', 'value': 'Lubuskie'},
                            {'label': 'Łódzkie', 'value': 'Lodzkie'},
                            {'label': 'Małopolskie', 'value': 'Malopolskie'},
                            {'label': 'Mazowieckie', 'value': 'Mazowieckie'},
                            {'label': 'Opolskie', 'value': 'Opolskie'},
                            {'label': 'Podkarpackie', 'value': 'Podkarpackie'},
                            {'label': 'Podlaskie', 'value': 'Podlaskie'},
                            {'label': 'Pomorskie', 'value': 'Pomorskie'},
                            {'label': 'Śląskie', 'value': 'Slaskie'},
                            {'label': 'Świętokrzyskie', 'value': 'Swietokrzyskie'},
                            {'label': 'Warmińsko-Mazurskie', 'value': 'Warminsko-Mazurskie'},
                            {'label': 'Wielkopolskie', 'value': 'Wielkopolskie'},
                            {'label': 'Zachodniopomorskie', 'value': 'Zachodniopomorskie'}
                        ],
                        value='Zachodniopomorskie',
                        labelStyle={'display': 'block'},
                        inputStyle={"margin-right": "5px"}
                    ), style={'width': '40%', 'display': 'inline-block', 'padding': '0 20', 'margin-left': '0'})
                ], style={'display': 'flex', 'justify-content': 'center'})
            ],  style={
                        'width': '40%', 
                        'padding': '0px 20px 20px 20px', 
                        'margin-right': '0'}),
                
            html.Div(
                dcc.Graph(
                    id='line'
            ), style={'width': '50%', 'display': 'inline-block', 'padding': '0 20', 'margin-left': '0'})
        ], className='container'),
                
        html.Div([
            html.Div([
                html.H2('Wybierz województwo:', style={'text-align': 'center', 'margin-top': '20px'}),
                html.Div(dcc.Dropdown(
                    id='voivodeship_selector_pie',
                    options=[
                        {'value': 'Dolnoslaskie', 'label': 'Dolnośląskie'},
                        {'value': 'Kujawsko-Pomorskie', 'label': 'Kujawsko-Pomorskie'},
                        {'value': 'Lubelskie', 'label': 'Lubelskie'},
                        {'value': 'Lubuskie', 'label': 'Lubuskie'},
                        {'value': 'Lodzkie', 'label': 'Łódzkie'},
                        {'value': 'Malopolskie', 'label': 'Małopolskie'},
                        {'value': 'Mazowieckie', 'label': 'Mazowieckie'},
                        {'value': 'Opolskie', 'label': 'Opolskie'},
                        {'value': 'Podkarpackie', 'label': 'Podkarpackie'},
                        {'value': 'Podlaskie', 'label': 'Podlaskie'},
                        {'value': 'Pomorskie', 'label': 'Pomorskie'},
                        {'value': 'Slaskie', 'label': 'Śląskie'},
                        {'value': 'Swietokrzyskie', 'label': 'Świętokrzyskie'},
                        {'value': 'Warminsko-Mazurskie', 'label': 'Warmińsko-Mazurskie'},
                        {'value': 'Wielkopolskie', 'label': 'Wielkopolskie'},
                        {'value': 'Zachodniopomorskie', 'label': 'Zachodniopomorskie'}
                    ],
                    value='Dolnoslaskie'
                ),  style={
                            'width': '70%', 
                            'padding': '0px 20px 20px 20px', 
                            'margin': '20px auto'})
            ], style={'width': '20%', 'display': 'inline-block', 'padding': '0 20', 'margin-left': '0'})
        ], className='container', style={'margin-top': '60px'}),
        html.Div([
            dcc.Graph(
                id='pie',
                style={'width': '50%', 'margin': '20px auto'}
            )
        ]),
        html.Div([
            html.H2('Wybierz rok:', style={'text-align': 'center', 'margin-top': '20px'}),
            html.Div(dcc.Slider(
                id='year_selector_pie',
                min=df['Rok'].min(),
                max=df['Rok'].max(),
                marks={str(year): str(year) for year in df['Rok'].unique()},
                value=df['Rok'].min(),
                step=None
            ),  style={
                        'width': '49%', 
                        'padding': '0px 20px 20px 20px', 
                        'margin': '20px auto'})
        ]),
    ]),
])


                
               
@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('year_selector', 'value'),
      dash.dependencies.Input('pollution_selector', 'value')],
      dash.dependencies.State('pollution_selector', 'options'))
def update_graph(year_value, xaxis_column_name, pollution_opt):
    
    dff_scatter = df[df['Rok'] == year_value]
    fig = px.scatter(
            dff_scatter,
            x='Zgony_per_100k',
            y=xaxis_column_name,
            size='populacja',
            color='Nazwa',
            color_discrete_map=colors,
            custom_data=[voivodeships]
        )
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b> <br><br>Zgony: %{x} <br>Zanieczyszczenie: %{y} <br>Populacja: %{marker.size:,}<extra></extra>')
    
    label_name = [option['label'] for option in pollution_opt if option['value'] == xaxis_column_name]
    fig.update_xaxes(title='Liczba zgonów spowodowanych nowotworem na 100 000 mieszkańców', type='linear')
    fig.update_yaxes(title=label_name[0] + ' [T]', type='linear')
    
    fig.update_traces(marker=dict(line=dict(width=2,
                                        color='DarkSlateGrey')))
    

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_layout(showlegend=False)
    fig.show()

    return fig


@app.callback(
    dash.dependencies.Output('bar', 'figure'),
    [dash.dependencies.Input('voivodeship_selector', 'value'),
     dash.dependencies.Input('pollution_selector_bar', 'value')],
     dash.dependencies.State('pollution_selector_bar', 'options'))
def update_bar_graph(voivodeship_value, pollution_value, pollution_opt):
    
    dff_bar = df[df['Nazwa'] == voivodeship_value]
    label_name = [option['label'] for option in pollution_opt if option['value'] == pollution_value]
    
    fig = px.bar (
            dff_bar,
            x='Rok',
            y=pollution_value,
            color='Nazwa',
            color_discrete_map=colors
        )
    
    fig.update_traces(hovertemplate='Rok: %{x} <br>Zanieczyszczenie: %{y} <extra></extra>')
    
    fig.update_xaxes(title='Rok', type='linear')
    fig.update_yaxes(title=label_name[0] + ' [T]', type='linear')
    fig.update_layout(showlegend=False)
    

    return fig

@app.callback(
    dash.dependencies.Output('line', 'figure'),
    [dash.dependencies.Input('voivodeship_selector_compare_1', 'value'),
     dash.dependencies.Input('voivodeship_selector_compare_2', 'value'),
     dash.dependencies.Input('pollution_selector_line', 'value')],
    dash.dependencies.State('pollution_selector_line', 'options'))
def update_line_graph(voivodeship_value_1, voivodeship_value_2, pollution_value, pollution_opt):
    
    dff_line = df.loc[(df['Nazwa'] == voivodeship_value_1) | (df['Nazwa'] == voivodeship_value_2)]
    label_name = [option['label'] for option in pollution_opt if option['value'] == pollution_value]
    
    fig = px.line(
            dff_line,
            x='Rok',
            y=pollution_value,
            color='Nazwa',
            color_discrete_map=colors
        )
    fig.update_traces(mode="markers+lines", hovertemplate='Rok: %{x} <br>Zanieczyszczenie: %{y} <extra></extra>')
    fig.update_layout(hovermode="x")

    fig.update_xaxes(title='Rok', type='linear')
    fig.update_yaxes(title=label_name[0] + ' [T]', type='linear')
    fig.update_layout(legend_title_text='Zanieczyszczenie')

    return fig


@app.callback(
    dash.dependencies.Output('pie', 'figure'),
    [dash.dependencies.Input('voivodeship_selector_pie', 'value'),
     dash.dependencies.Input('year_selector_pie', 'value')],
    dash.dependencies.State('voivodeship_selector_pie', 'options'))
def update_pie_graph(voivodeship_value, year_selector, voivodeship_opt):
    
    dff_pie = df.loc[(df['Nazwa'] == voivodeship_value) & (df['Rok'] == year_selector)]
    dff_slice = dff_pie.loc[:, 'tlenki_azotu':'nie_zorganizowana']
    dff_pie_transpose = dff_slice.transpose()
    dff_pie_transpose = dff_pie_transpose.reset_index()
    dff_pie_transpose = dff_pie_transpose.rename(columns={'index': 'Zanieczyszczenie',  dff_pie_transpose.columns[1]: 'Wartosc'})
    
    fig = px.pie(
            dff_pie_transpose,
            values='Wartosc',
            names=pollutions,
            labels=[pollutions],
            color='Zanieczyszczenie',
            color_discrete_map=pollution_colors
        )
    fig.update_traces(hovertemplate='Wartość: %{value} <br>Zanieczyszczenie: %{label} <extra></extra>')

    # fig.update_xaxes(title='Rok', type='linear')
    # fig.update_yaxes(title=label_name[0] + ' [T]', type='linear')
    # fig.update_layout(legend_title_text='Zanieczyszczenie')

    return fig
                

if __name__ == '__main__':
    app.run_server()
