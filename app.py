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

# Słownik kolorów dla każdego województwa
# Pierwsze 8 kolorów wybranych zostało z poniższej palety:
# https://colorbrewer2.org/#type=qualitative&scheme=Pastel2&n=8
# Pozostałe 8 z poniższej:
# https://colorbrewer2.org/#type=qualitative&scheme=Set1&n=8
# Ze względu na 16 wartości, zdecydowano się na połączenie dwóch palet
colors = {
        'Dolnoslaskie':         'rgb(179,226,205)',
        'Kujawsko-Pomorskie':   'rgb(253,205,172)',
        'Lubelskie':            'rgb(203,213,232)',
        'Lubuskie':             'rgb(244,202,228)',
        'Lodzkie':              'rgb(230,245,201)',
        'Malopolskie':          'rgb(255,242,174)',
        'Mazowieckie':          'rgb(241,226,204)',
        'Opolskie':             'rgb(204,204,204)',
        'Podkarpackie':         'rgb(228,26,28)',
        'Podlaskie':            'rgb(55,126,184)',
        'Pomorskie':            'rgb(77,175,74)',
        'Slaskie':              'rgb(152,78,163)',
        'Swietokrzyskie':       'rgb(255,127,0)',
        'Warminsko-Mazurskie':  'rgb(255,255,51)',
        'Wielkopolskie':        'rgb(166,86,40)',
        'Zachodniopomorskie':   'rgb(247,129,191)'
}

# Słownik kolorów dla każdego zanieczyszczenia
# Kolory wybrano z poniższej palety:
# https://colorbrewer2.org/#type=qualitative&scheme=Set3&n=7
pollution_colors = {
        'tlenki_azotu':         'rgb(141,211,199)',
        'tlenek_wegla':         'rgb(255,255,179)',
        'podtlenek_azotu':      'rgb(190,186,218)',
        'dwutlenek_siarki':     'rgb(251,128,114)',
        'dwutlenek_wegla':      'rgb(128,177,211)',
        'metan':                'rgb(253,180,98)',
        'nie_zorganizowana':    'rgb(179,222,105)'
}

# Słownik mapowania wartości w DataFrame na poprawną nazwę województwa
voivodeships = {
        'Dolnoslaskie':         'Dolnośląskie',
        'Kujawsko-Pomorskie':   'Kujawsko-Pomorskie',
        'Lubelskie':            'Lubelskie',
        'Lubuskie':             'Lubuskie',
        'Lodzkie':              'Łódzkie',
        'Malopolskie':          'Małopolskie',
        'Mazowieckie':          'Mazowieckie',
        'Opolskie':             'Opolskie',
        'Podkarpackie':         'Podkarpackie',
        'Podlaskie':            'Podlaskie',
        'Pomorskie':            'Pomorskie',
        'Slaskie':              'Śląskie',
        'Swietokrzyskie':       'Świętokrzyskie',
        'Warminsko-Mazurskie':  'Warmińsko-Mazurskie',
        'Wielkopolskie':        'Wielkopolskie',
        'Zachodniopomorskie':   'Zachodniopomorskie'
}

# Słownik mapowania kolumn w DataFrame na poprawną nazwę zanieczyszczenia
pollutions = {
        'tlenki_azotu':         'Tlenki azotu',
        'tlenek_wegla':         'Tlenek węgla',
        'podtlenek_azotu':      'Podtlenek azotu',
        'dwutlenek_siarki':     'Dwutlenek siarki',
        'dwutlenek_wegla':      'Dwutlenek węgla',
        'metan':                'Metan',
        'nie_zorganizowana':    'Nie zorganizowana'
}


# Lista wartości wpojewództw dla dropdown box
voivodeship_select_labels = [
        {'label': 'Dolnośląskie',           'value': 'Dolnoslaskie'},
        {'label': 'Kujawsko-Pomorskie',     'value': 'Kujawsko-Pomorskie'},
        {'label': 'Lubelskie',              'value': 'Lubelskie'},
        {'label': 'Lubuskie',               'value': 'Lubuskie'},
        {'label': 'Łódzkie',                'value': 'Lodzkie'},
        {'label': 'Małopolskie',            'value': 'Malopolskie'},
        {'label': 'Mazowieckie',            'value': 'Mazowieckie'},
        {'label': 'Opolskie',               'value': 'Opolskie'},
        {'label': 'Podkarpackie',           'value': 'Podkarpackie'},
        {'label': 'Podlaskie',              'value': 'Podlaskie'},
        {'label': 'Pomorskie',              'value': 'Pomorskie'},
        {'label': 'Śląskie',                'value': 'Slaskie'},
        {'label': 'Świętokrzyskie',         'value': 'Swietokrzyskie'},
        {'label': 'Warmińsko-Mazurskie',    'value': 'Warminsko-Mazurskie'},
        {'label': 'Wielkopolskie',          'value': 'Wielkopolskie'},
        {'label': 'Zachodniopomorskie',     'value': 'Zachodniopomorskie'}   
]

# Lista wartości zanieczyszceń dla dropdown box
pollution_select_labels = [
        {'label': 'Dwutlenek węgla',    'value': 'dwutlenek_wegla'},
        {'label': 'Tlenek węgla',       'value': 'tlenek_wegla'},
        {'label': 'Tlenki azotu',       'value': 'tlenki_azotu'},
        {'label': 'Podtlenek azotu',    'value': 'podtlenek_azotu'},
        {'label': 'Dwutlenek siarki',   'value': 'dwutlenek_siarki'},
        {'label': 'Metan',              'value': 'metan'},
        {'label': 'Nie zorganizowana',  'value': 'nie_zorganizowana'}
]

# Wczytanie czcionki i stylów

external_stylesheets = ['https://fonts.googleapis.com/css?family=Raleway:400,700&display=swap', 'style.css']

# Stworzenie aplikacji
app = dash.Dash('Zanieczyszczenie powietrza a nowotwory', server=server, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

# Tworzenie widoku aplikacji
app.layout = html.Div([
    html.Header([
        html.H1('Zanieczyszczenie powietrza i nowotwory'),
        html.H3('Zależności pomiędzy zanieczyszczeniem powietrza a zgonami spowodowanymi nowotworami.'),
    ]),
    html.Div([
        html.Div([
            html.P('Zanieczyszczenie powietrza jest problemem globalnym. Międzynarodowa Organizacja Pracy definiuje je jako "wszelkie skażenie powietrza przez substancje, które są szkodliwe dla zdrowia lub niebezpieczne z innych przyczyn, bez względu na ich postać fizyczną". Spalanie paliw kopalnych, działalność rolnicza czy eksploatacja górnicza to tylko kilka przykładów, które przyczyniają się do zwiększania zanieczyszczenia powietrza. Substancje, które mają na nie wpływ to dwutlenek węgla, dwutlenek siarki, tlenki azotu i inne.'),

            html.P('Poniżej znajduje się analiza zanieczyszczenia środowiska w Polsce w latach 1998 - 2017 w podziale na województwa. Zestawiono te informacje z liczbą zgonów w każdym województwie spowodowanych nowotworem. Pod uwagę zostały wzięte wszystkie rodzaje choroby.', style={'margin-top': '20px'})
        ], className='text_container'),
        
        html.Div([
            html.H2('Wybierz zanieczyszczenie:', className='selection_title'),
            html.Div(dcc.Dropdown(
                id='pollution_selector',
                options=pollution_select_labels,
                value='dwutlenek_wegla'
            ),  style={
                        'width': '20%'
                },
                className='dcc_component'
            )
        ]),
        html.Div([
            dcc.Graph(
                id='scatter',
                style={
                    'width': '50%', 
                    'margin': '20px auto'
                }
            )
        ]),
        html.Div([
            html.H2('Wybierz rok:', className='selection_title'),
            html.Div(dcc.Slider(
                id='year_selector',
                min=df['Rok'].min(),
                max=df['Rok'].max(),
                marks={str(year): str(year) for year in df['Rok'].unique()},
                value=df['Rok'].min(),
                step=None
            ),  style={
                        'width': '49%'
                },
                className='dcc_component'
            )
        ]),
        html.Div([
            html.H2('Wybierz zanieczyszczenie:', className='selection_title'),
            html.Div(dcc.Dropdown(
                id='pollution_selector_bar',
                options=pollution_select_labels,
                value='dwutlenek_wegla'
            ),  style={
                        'width': '20%'
                },
                className='dcc_component'
            )
        ], style={'margin-top': '60px'}),
        html.Div([
            html.Div([
                html.H2('Wybierz województwo:', className='radio_title'),
                html.Div(dcc.RadioItems(
                    id='voivodeship_selector',
                    options= voivodeship_select_labels,
                    value='Dolnoslaskie',
                    labelStyle={'display': 'block'},
                    inputStyle={"margin-right": "5px"}
                ))
            ],  style={
                        'width': '20%', 
                        'padding': '0px 20px 20px 20px', 
                        'display': 'inline-block',
                        'margin-right': '0'
                }
            ),
                
            html.Div(
                dcc.Graph(
                    id='bar'
                ), style={
                           'width': '50%', 
                           'display': 'inline-block', 
                           'padding': '0 20', 
                           'margin-left': '0'
               }
            )
        ], className='container'),
                
        html.Div([
            html.H2('Wybierz zanieczyszczenie:', className='selection_title'),
            html.Div(dcc.Dropdown(
                id='pollution_selector_line',
                options=pollution_select_labels,
                value='dwutlenek_wegla'
            ),  style={
                        'width': '20%'
                },
                className='dcc_component'
            )
        ], style={'margin-top': '60px'}),
                
        html.Div([
            html.Div([
                html.H2('Wybierz województwa do porównania:', className='radio_title'),
                html.Div([
                    html.Div(dcc.RadioItems(
                        id='voivodeship_selector_compare_1',
                        options= voivodeship_select_labels,
                        value='Dolnoslaskie',
                        labelStyle={'display': 'block'},
                        inputStyle={"margin-right": "5px"}
                    ), className='dcc_radio_component'),
                    
                    html.Div(dcc.RadioItems(
                        id='voivodeship_selector_compare_2',
                        options= voivodeship_select_labels,
                        value='Zachodniopomorskie',
                        labelStyle={'display': 'block'},
                        inputStyle={"margin-right": "5px"}
                    ), className='dcc_radio_component'),
                ], style={
                            'display': 'flex', 
                            'justify-content': 'center'
                    }
                )
            ],  style={
                        'width': '40%', 
                        'padding': '0px 20px 20px 20px', 
                        'margin-right': '0'
                }
            ),
                
            html.Div(
                dcc.Graph(
                    id='line'
                ), style={
                            'width': '50%',
                            'display': 'inline-block', 
                            'padding': '0 20', 
                            'margin-left': '0'
                }
            )
        ], className='container'),
                
        html.Div([
            html.Div([
                html.H2('Wybierz województwo:', className='selection_title'),
                html.Div(dcc.Dropdown(
                    id='voivodeship_selector_pie',
                    options= voivodeship_select_labels,
                    value='Dolnoslaskie'
                ),  style={
                            'width': '70%'
                    },
                    className='dcc_component'
                )
            ], style={
                        'width': '20%', 
                        'display': 'inline-block', 
                        'padding': '0 20', 
                        'margin-left': '0'
                }
            )
        ], className='container', style={'margin-top': '60px'}),
        html.Div([
            dcc.Graph(
                id='pie',
                style={
                        'width': '50%', 
                        'margin': '20px auto'
                }
            )
        ]),
        html.Div([
            html.H2('Wybierz rok:', className='selection_title'),
            html.Div(dcc.Slider(
                id='year_selector_pie',
                min=df['Rok'].min(),
                max=df['Rok'].max(),
                marks={str(year): str(year) for year in df['Rok'].unique()},
                value=df['Rok'].min(),
                step=None
            ),  style={
                        'width': '49%'
                },
                className='dcc_component'
            )
        ]),
    ]),
])


                
# Callback dla wykresu scatterplot
@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('year_selector', 'value'),
    dash.dependencies.Input('pollution_selector', 'value')],
    dash.dependencies.State('pollution_selector', 'options'))
def update_graph(year_value, pollution_value, pollution_opt):
    
    # Przygotowanie DataFrame
    df_scatter = df[df['Rok'] == year_value]
    # Pobranie wyświetlanego tekstu z Dropdown Boxa
    pollution_label_name = [option['label'] for option in pollution_opt if option['value'] == pollution_value]
    
    # Przypisanie danych do wykresu
    fig = px.scatter(
            df_scatter,
            x='Zgony_per_100k',
            y=pollution_value,
            size='populacja',
            color='Nazwa',
            color_discrete_map=colors,
            custom_data=[voivodeships]
        )
    
    # Przygotowanie tekstu do wyświetlenia onHover
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b> <br><br>Zgony: %{x} <br>Zanieczyszczenie: %{y} <br>Populacja: %{marker.size:,}<extra></extra>')
    # Dodanie tutyłu dla osi X
    fig.update_xaxes(title='Liczba zgonów spowodowanych nowotworem na 100 000 mieszkańców', type='linear')
    # Dodanie tutyłu dla osi Y
    fig.update_yaxes(title=pollution_label_name[0] + ' [T]', type='linear')
    # Dodanie ramki dla punktów na wykresie
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    # Ukrycie legendy
    fig.update_layout(showlegend=False)

    return fig


# Callback dla wykresu Bar Chart
@app.callback(
    dash.dependencies.Output('bar', 'figure'),
    [dash.dependencies.Input('voivodeship_selector', 'value'),
    dash.dependencies.Input('pollution_selector_bar', 'value')],
    dash.dependencies.State('pollution_selector_bar', 'options'))
def update_bar_graph(voivodeship_value, pollution_value, pollution_opt):
    
    # Przygotowanie DataFrame
    df_bar = df[df['Nazwa'] == voivodeship_value]
    # Pobranie wyświetlanego tekstu z Dropdown Boxa
    pollution_label_name = [option['label'] for option in pollution_opt if option['value'] == pollution_value]
    
    # Przypisanie danych do wykresu
    fig = px.bar (
            df_bar,
            x='Rok',
            y=pollution_value,
            color='Nazwa',
            color_discrete_map=colors
        )
    
    # Przygotowanie tekstu do wyświetlenia onHover
    fig.update_traces(hovertemplate='Rok: %{x} <br>Zanieczyszczenie: %{y} <extra></extra>')
    # Dodanie tutyłu dla osi X
    fig.update_xaxes(title='Rok', type='linear')
    # Dodanie tutyłu dla osi Y
    fig.update_yaxes(title=pollution_label_name[0] + ' [T]', type='linear')
    # Ukrycie legendy
    fig.update_layout(showlegend=False)

    return fig


# Callback dla wykresu Line Chart
@app.callback(
    dash.dependencies.Output('line', 'figure'),
    [dash.dependencies.Input('voivodeship_selector_compare_1', 'value'),
    dash.dependencies.Input('voivodeship_selector_compare_2', 'value'),
    dash.dependencies.Input('pollution_selector_line', 'value')],
    dash.dependencies.State('pollution_selector_line', 'options'))
def update_line_graph(voivodeship_value_1, voivodeship_value_2, pollution_value, pollution_opt):
    
    # Przygotowanie DataFrame
    df_line = df.loc[(df['Nazwa'] == voivodeship_value_1) | (df['Nazwa'] == voivodeship_value_2)]
    # Pobranie wyświetlanego tekstu z Dropdown Boxa
    pollution_label_name = [option['label'] for option in pollution_opt if option['value'] == pollution_value]
    
    # Przypisanie danych do wykresu
    fig = px.line(
            df_line,
            x='Rok',
            y=pollution_value,
            color='Nazwa',
            color_discrete_map=colors
        )
    
    # Przygotowanie tekstu do wyświetlenia onHover
    fig.update_traces(mode="markers+lines", hovertemplate='Rok: %{x} <br>Zanieczyszczenie: %{y} <extra></extra>')
    fig.update_layout(hovermode="x")
    # Dodanie tutyłu dla osi X
    fig.update_xaxes(title='Rok', type='linear')
    # Dodanie tutyłu dla osi Y
    fig.update_yaxes(title=pollution_label_name[0] + ' [T]', type='linear')
    # Zmiana nazwy legendy
    fig.update_layout(legend_title_text='Zanieczyszczenie')

    return fig


# Callback dla wykresu Pie Chart
@app.callback(
    dash.dependencies.Output('pie', 'figure'),
    [dash.dependencies.Input('voivodeship_selector_pie', 'value'),
    dash.dependencies.Input('year_selector_pie', 'value')],
    dash.dependencies.State('voivodeship_selector_pie', 'options'))
def update_pie_graph(voivodeship_value, year_selector, voivodeship_opt):
    
    # Przygotowanie DataFrame
    df_pie = df.loc[(df['Nazwa'] == voivodeship_value) & (df['Rok'] == year_selector)]
    # Ograniczenie do kolumn z wartościami zanieczyszczeń
    df_slice = df_pie.loc[:, 'tlenki_azotu':'nie_zorganizowana']
    # Transpozycja
    df_pie_transpose = df_slice.transpose()
    # Utworzenie kolumny indeksu
    df_pie_transpose = df_pie_transpose.reset_index()
    # Zmiana nazw kolumn
    df_pie_transpose = df_pie_transpose.rename(columns={df_pie_transpose.columns[0]: 'Zanieczyszczenie',  df_pie_transpose.columns[1]: 'Wartosc'})
    
    # Przypisanie danych do wykresu
    fig = px.pie(
            df_pie_transpose,
            values='Wartosc',
            names=pollutions,
            labels=[pollutions],
            color='Zanieczyszczenie',
            color_discrete_map=pollution_colors
        )
    
    # Przygotowanie tekstu do wyświetlenia onHover
    fig.update_traces(hovertemplate='Wartość: %{value} <br>Zanieczyszczenie: %{label} <extra></extra>')

    return fig
                

if __name__ == '__main__':
    app.run_server()
