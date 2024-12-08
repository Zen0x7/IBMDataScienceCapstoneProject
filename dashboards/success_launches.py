import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import requests

# Obtener datos de la API de SpaceX v3
url = 'https://api.spacexdata.com/v3/launches'
response = requests.get(url)
launches = response.json()

# Procesar los datos para obtener éxito y fallos
successes = sum(1 for launch in launches if launch['launch_success'])
failures = len(launches) - successes

# Crear DataFrame para el gráfico
data = {
    'Resultado': ['Successful', 'Failed'],
    'Cantidad': [successes, failures]
}
df = pd.DataFrame(data)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout
app.layout = html.Div([
    html.H1('SpaceX Launches', style={'textAlign': 'center'}),
    dcc.Graph(
        id='grafico-torta',
        figure=px.pie(
            df,
            values='Cantidad',
            names='Resultado',
            title='Distribution of successful and failed launches'
        )
    )
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)