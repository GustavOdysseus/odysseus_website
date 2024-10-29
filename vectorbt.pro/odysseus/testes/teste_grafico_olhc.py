import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import vectorbtpro as vbt
import duckdb

# Configuração inicial
DB_PATH = "forex_market.duckdb"
BLOCK_SIZE = 10000  # Tamanho do bloco de candles a ser carregado

# Carregar os primeiros 'n' registros
def load_data(symbol, start_idx, block_size):
    data = vbt.DuckDBData.from_duckdb(symbol, connection=DB_PATH)
    return data.get().iloc[start_idx:start_idx+block_size]

# Criar a aplicação Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Visualização de Gráfico OHLC com Carregamento Dinâmico"),
    
    # Alternar entre temas
    html.Label("Escolha o Tema:"),
    dcc.RadioItems(
        id='theme-switch',
        options=[
            {'label': 'Claro', 'value': 'plotly'},
            {'label': 'Escuro', 'value': 'plotly_dark'}
        ],
        value='plotly',  # Tema padrão
        labelStyle={'display': 'inline-block'}
    ),
    
    # Gráfico OHLC
    dcc.Graph(id="ohlc-graph", config={"scrollZoom": True}),
    
    # Botão para carregar mais dados
    html.Button('Carregar Mais Dados', id='load-more', n_clicks=0),
    
    # Armazenar o índice de carregamento dos dados
    dcc.Store(id='data-store', data={'start_idx': 0, 'block_size': BLOCK_SIZE})
])

# Atualizar gráfico quando novos dados forem carregados ou tema for alterado
@app.callback(
    Output('ohlc-graph', 'figure'),
    [Input('load-more', 'n_clicks'),
     Input('theme-switch', 'value'),
     Input('data-store', 'data')]
)
def update_graph(n_clicks, theme, store_data):
    start_idx = store_data['start_idx']
    block_size = store_data['block_size']

    # Carregar os dados (simbolicamente usando AUDCAD)
    df = load_data('AUDCAD', start_idx, block_size)

    # Construir o gráfico OHLC
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='OHLC'
    )])

    # Aplicar o tema escolhido
    fig.update_layout(template=theme)
    
    fig.update_layout(title=f'Dados de AUDCAD - Candles {start_idx} até {start_idx + block_size}',
                      xaxis_rangeslider_visible=False)

    return fig

# Atualizar o índice de carregamento ao clicar no botão
@app.callback(
    Output('data-store', 'data'),
    [Input('load-more', 'n_clicks')],
    [dash.dependencies.State('data-store', 'data')]
)
def load_more_data(n_clicks, store_data):
    start_idx = store_data['start_idx'] + BLOCK_SIZE
    store_data['start_idx'] = start_idx
    return store_data

if __name__ == '__main__':
    app.run_server(debug=True)
