import dash
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html, Input, Output, State
import pandas as pd

app = dash.Dash(__name__)

# Example data for the hours table
data = {
    'Ítem': ['1', '2', '3', '4'],
    'Documento': ['Documento 1', 'Documento 2', 'Documento 3', 'Documento 4'],
    'Lider': [3, 3, 0, 0],
    'Ing': [24, 24, 4, 5],
    'Aux': [3, 2, 4, 2],
    'Control': [2, 2, 3, 2]
}
df = pd.DataFrame(data)

# Example financial breakdown data
financial_data = {
    'Descripción': ['Lider', 'Ingeniero', 'Auxiliar', 'Control de Calidad'],
    'Cant': [0, 0, 0, 0],
    'Valor Unitario Sugerido': [80000, 50000, 25000, 35000],
    'Valor Unitario Seleccionado': [56250, 56250, 56250, 37500],
    'Valor Total': [0, 0, 0, 0]  # This will be updated dynamically
}
financial_df = pd.DataFrame(financial_data)

# Costos Administrativos Extra data
extra_costs_data = {
    'Ítem': ['1', '2', '3'],
    'Descripción': ['Tiquetes', 'Viáticos', 'Administrativos'],
    'Cant': [0, 0, 0],
    'Valor Unitario': [50000, 50000, 50000],
    'Valor Total': [0, 0, 0]  # This will be updated dynamically
}
extra_costs_df = pd.DataFrame(extra_costs_data)

#ccosto por documento

costo_por_documento = {
    'item': ['1', '2', '3','4'],
    'Documento': ['Documento 1', 'Documento 2', 'Documento 3', 'Documento 4'],
    'Porcentaje' : [20,30,40,10],
    'costo' : [0,0,0,0]
}

costo_documento_df=pd.DataFrame(costo_por_documento)

# Layout
app.layout = dbc.Container([

    html.H1('Registro de Horas Hombre por Documento', style={'textAlign': 'center'}),
    
    html.H2('1) Registra los documentos'),

    dash_table.DataTable(
        id='table-editable',
        columns=[
            {"name": 'Ítem', "id": 'Ítem', "editable": True},
            {"name": 'Documento', "id": 'Documento', "editable": True},
            {"name": 'Lider', "id": 'Lider', "editable": True},
            {"name": 'Ing', "id": 'Ing', "editable": True},
            {"name": 'Aux', "id": 'Aux', "editable": True},
            {"name": 'Control', "id": 'Control', "editable": True},
        ],
        data=df.to_dict('records'),
        editable=True,
        style_cell={'textAlign': 'center'},
    ),
 
    html.Div(id='table-output'),

    html.H2('2) Total de horas'),

    # Financial breakdown section using DataTable
    dash_table.DataTable(
        id='financial-table',
        columns=[
            {"name": 'Descripción', "id": 'Descripción', "editable": False},
            {"name": 'Cant', "id": 'Cant', "editable": True},
            {"name": 'Valor Unitario Sugerido', "id": 'Valor Unitario Sugerido', "editable": False},
            {"name": 'Valor Unitario Seleccionado', "id": 'Valor Unitario Seleccionado', "editable": False},
            {"name": 'Valor Total', "id": 'Valor Total', "editable": False}
        ],
        data=financial_df.to_dict('records'),
        editable=True,
        style_cell={'textAlign': 'center'},
        style_table={'width': '100%'},
    ),
    
    
    html.H2('3) Costos administrativos extra'),
    dash_table.DataTable(
        id='extra-costs-table',
        columns=[
            {"name": 'Ítem', "id": 'Ítem', "editable": False},
            {"name": 'Descripción', "id": 'Descripción', "editable": False},
            {"name": 'Cant', "id": 'Cant', "editable": True},
            {"name": 'Valor Unitario', "id": 'Valor Unitario', "editable": True},
            {"name": 'Valor Total', "id": 'Valor Total', "editable": False}
        ],
        data=extra_costs_df.to_dict('records'),
        editable=True,
        style_cell={'textAlign': 'center'},
        style_table={'width': '100%'},
    ),
    
    html.H2('4) Costos por documento'),
    
    html.Div([
        html.Label('Costo total del proyecto incluido IVA:'),
        dcc.Input(id='input-total-costo', type='number', value=0, min=0, step=0.01, style={'margin-left': '10px'}),
    ], style={'marginBottom': '20px'}),
    
      # Costo por Documento Table
    dash_table.DataTable(
        id='costo-por-documento',
        columns=[
            {"name": 'Ítem', "id": 'item', "editable": False},
            {"name": 'Documento', "id": 'Documento', "editable": True},
            {"name": 'Porcentaje', "id": 'Porcentaje', "editable": True},
            {"name": 'Costo', "id": 'costo', "editable": False},
        ],
        data=costo_documento_df.to_dict('records'),
        editable=True,
        style_cell={'textAlign': 'center'},
        style_table={'width': '100%'},
    ),
    html.Div(id='total-costo-por-documento-output', style={'fontWeight': 'bold'}),

    
    html.Br(),
    html.Br(),
    html.Br(),
    
    
])

# Callback to update the hours table data and calculate totals
@app.callback(
    Output('table-editable', 'data'),
    [Input('table-editable', 'data')]
)
def update_table_data(data):
    # Convert the data into a DataFrame to process it
    updated_df = pd.DataFrame(data)
    
    # Remove any existing total row to avoid duplications
    updated_df = updated_df[updated_df['Ítem'] != 'Total']

    # Ensure numeric columns are properly converted to integers or floats
    numeric_columns = ['Lider', 'Ing', 'Aux', 'Control']
    for col in numeric_columns:
        updated_df[col] = pd.to_numeric(updated_df[col], errors='coerce').fillna(0)

    # Calculate the totals for the numeric columns
    total_row = pd.DataFrame({
        'Ítem': ['Total'],
        'Documento': [''],
        'Lider': [updated_df['Lider'].sum()],
        'Ing': [updated_df['Ing'].sum()],
        'Aux': [updated_df['Aux'].sum()],
        'Control': [updated_df['Control'].sum()]
    })
    
    # Concatenate the original dataframe with the updated total row
    updated_df = pd.concat([updated_df, total_row], ignore_index=True)
    
    return updated_df.to_dict('records')

# Callback to update the financial table when Cant is changed
@app.callback(
    Output('financial-table', 'data'),
    [Input('financial-table', 'data')]
)
def update_financial_table(financial_data):
    # Convert the financial data into a DataFrame
    financial_df = pd.DataFrame(financial_data)

    # Ensure "Cant" and "Valor Unitario Seleccionado" are numeric
    financial_df['Cant'] = pd.to_numeric(financial_df['Cant'], errors='coerce').fillna(0)
    financial_df['Valor Unitario Seleccionado'] = pd.to_numeric(financial_df['Valor Unitario Seleccionado'], errors='coerce').fillna(0)

    # Calculate "Valor Total" as 'Cant' * 'Valor Unitario Seleccionado'
    financial_df['Valor Total'] = financial_df['Cant'] * financial_df['Valor Unitario Seleccionado']

    return financial_df.to_dict('records')


# Callback to update the extra costs table when Cant is changed
@app.callback(
    Output('extra-costs-table', 'data'),
    [Input('extra-costs-table', 'data')]
)
def update_extra_costs_table(extra_costs_data):
    # Convert the extra costs data into a DataFrame
    extra_costs_df = pd.DataFrame(extra_costs_data)

    # Ensure "Cant" and "Valor Unitario" are numeric
    extra_costs_df['Cant'] = pd.to_numeric(extra_costs_df['Cant'], errors='coerce').fillna(0)
    extra_costs_df['Valor Unitario'] = pd.to_numeric(extra_costs_df['Valor Unitario'], errors='coerce').fillna(0)

    # Calculate "Valor Total" as 'Cant' * 'Valor Unitario'
    extra_costs_df['Valor Total'] = extra_costs_df['Cant'] * extra_costs_df['Valor Unitario']

    return extra_costs_df.to_dict('records')

# Callback to update the costo por documento when Porcentaje is changed and when total project cost is entered
@app.callback(
    Output('costo-por-documento', 'data'),
    [Input('costo-por-documento', 'data'),
     Input('input-total-costo', 'value')]
)
def update_costo_por_documento(costo_por_documento, total_project_cost):
    # Convert the data into a DataFrame
    costo_documento_df = pd.DataFrame(costo_por_documento)

    # Ensure 'Porcentaje' is numeric
    costo_documento_df['Porcentaje'] = pd.to_numeric(costo_documento_df['Porcentaje'], errors='coerce').fillna(0)

    # Update 'Costo' based on the 'Porcentaje'. The 'Costo' is calculated as 'Porcentaje' * total project cost
    if total_project_cost is None:
        total_project_cost = 0
    costo_documento_df['costo'] = (costo_documento_df['Porcentaje'] / 100) * total_project_cost

    return costo_documento_df.to_dict('records')

    

if __name__ == '__main__':
    app.run_server(debug=True)
