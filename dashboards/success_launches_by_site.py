import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import requests

# URL del endpoint
url = "https://api.spacexdata.com/v3/launches"

# Obtener los datos del endpoint
response = requests.get(url)
data = response.json()

# Procesar los datos
launches = pd.DataFrame(data)
launches['launch_success'] = launches['launch_success'].fillna(False)
launches['launch_site'] = launches['launch_site'].apply(lambda x: x['site_name'])

# Calcular las tasas de éxito por sitio
site_success_rate = launches.groupby('launch_site').agg(
    total_launches=('flight_number', 'count'),
    successful_launches=('launch_success', 'sum')
).reset_index()
site_success_rate['success_rate'] = (site_success_rate['successful_launches'] /
                                     site_success_rate['total_launches']) * 100

# Crear el dashboard
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("SpaceX Launch Site Success Rates", style={"textAlign": "center"}),
    dcc.Graph(id="success-pie-chart"),
])

# Callback para actualizar el gráfico
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("success-pie-chart", "id")
)
def update_pie_chart(_):
    fig = px.pie(
        site_success_rate,
        names="launch_site",
        values="success_rate",
        title="Launch Site Success Rate",
        hole=0.4
    )
    return fig

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)