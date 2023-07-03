from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

class DataCleaner:
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.DataFrame()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.filename, sep=',')
            self.df.dropna(inplace=True)  # Drop rows with missing values
        except pd.errors.ParserError as e:
            print(f"Erro ao ler o arquivo CSV: {e}")
            # Faça o tratamento de erro adequado.

    def validate_data(self):
        # Verificar colunas inválidas
        required_columns = [
            "ID", "Country of Origin", "Farm Name", "Lot Number", "Mill", "ICO Number",
            "Company", "Altitude", "Region", "Producer", "Number of Bags", "Bag Weight",
            "In-Country Partner", "Harvest Year", "Grading Date", "Owner", "Variety",
            "Status", "Processing Method", "Aroma", "Flavor", "Aftertaste", "Acidity",
            "Body", "Balance", "Uniformity", "Clean Cup", "Sweetness", "Overall",
            "Defects", "Total Cup Points", "Moisture Percentage", "Category One Defects",
            "Quakers", "Color", "Category Two Defects", "Expiration", "Certification Body",
            "Certification Address", "Certification Contact"
        ]
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            print(f"Colunas ausentes no arquivo CSV: {missing_columns}")
            # Faça o tratamento de erro adequado.

        # Verificar valores ausentes
        if self.df.isnull().values.any():
            print("Existem valores ausentes no arquivo CSV.")
            # Faça o tratamento de erro adequado.

    def clean_data(self):
        # Realize a limpeza de dados específica, se necessário
        pass

    def convert_date_column(self, column, formats):
        for fmt in formats:
            try:
                self.df[column] = pd.to_datetime(self.df[column], format=fmt)
                break
            except ValueError:
                continue

app = Dash(__name__)

# Load the data and perform data cleaning/validation
filename = 'df_arabica_clean.csv'
cleaner = DataCleaner(filename)
cleaner.load_data()
cleaner.validate_data()
cleaner.clean_data()
df_cleaned = cleaner.df
opcoes = list(df_cleaned["Farm Name"].unique())
opcoes.append("All Farms")

# Create the initial figure for the bar graph
fig_cf = px.bar(df_cleaned, x='Farm Name', y='Region')

# Define the Dash layout
app.layout = html.Div(
    children=[
        dcc.Graph(figure=fig_cf),  # Display the bar graph
        html.Div(children='Coffee Analysis'),
        dcc.Dropdown(options=[{'label': i, 'value': i} for i in opcoes], value='All Farms', id='farm-dropdown'),
        dcc.Graph(id='farm-region-chart')  # Display the updated bar graph based on the selected farm
    ]
)

# Define the callback to update the bar graph based on the selected farm
@app.callback(
    Output('farm-region-chart', 'figure'),
    Input('farm-dropdown', 'value')
)
def update_bar_graph(selected_farm):
    if selected_farm == 'All Farms':
        filtered_df = df_cleaned
    else:
        filtered_df = df_cleaned[df_cleaned['Farm Name'] == selected_farm]
    
    fig = px.pie(filtered_df, names='Harvest Year', values='Acidity', color='Farm Name')
    return fig

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
