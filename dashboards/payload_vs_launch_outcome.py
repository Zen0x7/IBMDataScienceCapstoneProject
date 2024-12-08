import dash
from dash import dcc, html, Input, Output
import pandas as pd
import requests
import plotly.express as px

# Cargar datos desde la API de SpaceX
url = "https://api.spacexdata.com/v3/launches"
response = requests.get(url)
data = response.json()

# Extraer payload_mass_kg y normalizar datos
def extract_payload_mass(launch):
    payloads = launch.get("rocket", {}).get("second_stage", {}).get("payloads", [])
    return sum(p.get("payload_mass_kg", 0) for p in payloads if p.get("payload_mass_kg") is not None)

# Crear DataFrame con los datos necesarios
df = pd.DataFrame(data)
df["payload_mass_kg"] = df.apply(extract_payload_mass, axis=1)
df["launch_site"] = df["launch_site"].apply(lambda x: x.get("site_name", "Unknown"))
df["launch_success"] = df["launch_success"].map({True: "Success", False: "Failure"}).fillna("Unknown")

# Depuración: Mostrar una muestra del DataFrame
print("Muestra del DataFrame:")
print(df[["payload_mass_kg", "launch_site", "launch_success"]].head())

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Diseño de la aplicación
app.layout = html.Div([
    html.H1("SpaceX Launch Payload vs. Outcome"),
    dcc.RangeSlider(
        id='payload-slider',
        min=df['payload_mass_kg'].min(),
        max=df['payload_mass_kg'].max(),
        step=100,
        value=[df['payload_mass_kg'].min(), df['payload_mass_kg'].max()],
        marks={int(m): str(int(m)) for m in range(0, int(df['payload_mass_kg'].max()) + 1, 5000)}
    ),
    dcc.Graph(id="scatter-plot"),
])

# Callback para actualizar el gráfico
@app.callback(
    Output("scatter-plot", "figure"),
    Input("payload-slider", "value")
)
def update_scatter_plot(payload_range):
    filtered_df = df[
        (df['payload_mass_kg'] >= payload_range[0]) &
        (df['payload_mass_kg'] <= payload_range[1])
    ]
    fig = px.scatter(
        filtered_df,
        x='payload_mass_kg',
        y='launch_site',
        color='launch_success',
        title='Payload vs Launch Outcome',
        labels={'payload_mass_kg': 'Payload Mass (kg)', 'launch_site': 'Launch Site'},
    )
    return fig

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)