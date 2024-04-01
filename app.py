import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load your data
df = pd.read_csv('./heart2022.csv')
#external_stylesheets = ['./assets/app.css']
#, external_stylesheets=external_stylesheets

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Heart Diseases Correlations"),
    html.H2('Bar Graph'),
    html.Label('Select a State:'),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': i, 'value': i} for i in df['State'].unique()],
        value=df['State'].unique()[0]
    ),
    html.Label('Select Health Condition:'),
    dcc.RadioItems(
        id='column-radioitems',className='options',
        options=[{'label': i, 'value': i} for i in [
            'HadHeartAttack',
            'HadAngina',
            'HadStroke',
            'HadAsthma',
            'HadSkinCancer',
            'HadDepressiveDisorder',
            'HadKidneyDisease',
            'HadArthritis',
            'HadDiabetes'
        ]],
        value='HadHeartAttack',
        inline=True
    ),
    dcc.Graph(id='display-value'),
    html.H2('Circle Graph'),
    html.Label('Select Health Condition:'),
    dcc.Dropdown(
        id='health-condition-dropdown',
        options=[{'label': i, 'value': i} for i in [
            'HadHeartAttack',
            'HadAngina',
            'HadStroke',
            'HadAsthma',
            'HadSkinCancer',
            'HadDepressiveDisorder',
            'HadKidneyDisease',
            'HadArthritis',
            'HadDiabetes'
        ]],
        value='HadHeartAttack'
    ),
    html.Label(id='slider-output-container'),
    dcc.Slider(
        id='sleep-hours-slider',
        min=df['SleepHours'].min(),
        max=df['SleepHours'].max(),
        value=df['SleepHours'].min(),
        marks={str(hour): str(hour) for hour in df['SleepHours'].unique()},
        step=None
    ),
    dcc.Graph(id='pie-chart'),
    html.H2('Histogram'),
    html.Label('Select Difficulty:'),
    dcc.Dropdown(
        id='difficulty-dropdown',
        options=[{'label': i, 'value': i} for i in [
            'DifficultyConcentrating',
            'DifficultyWalking',
            'DifficultyDressingBathing',
            'DifficultyErrands'
        ]],
        value='DifficultyConcentrating'
    ),
    dcc.Graph(id='difficulty-histogram'),
    html.H2('Scatter Plot'),
    html.Label('Select Y-axis for Scatter Plot:'),
    dcc.RadioItems(
        id='scatter-yaxis-radioitems',
        options=[{'label': i, 'value': i} for i in ['WeightInKilograms', 'HeightInMeters']],
        value='WeightInKilograms',
        inline=True
    ),
    dcc.Graph(id='scatter-plot')
])

@app.callback(
    Output('display-value', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('column-radioitems', 'value')]
)
def update_histogram(selected_state, selected_column):
    filtered_df = df[df['State'] == selected_state]
    fig = px.histogram(filtered_df, x=selected_column, color=selected_column,
                       color_discrete_map={'True': 'blue', 'False': 'red'})
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('health-condition-dropdown', 'value'),
     Input('sleep-hours-slider', 'value')]
)
def update_pie_chart(selected_condition, selected_hours):
    filtered_df = df[df['SleepHours'] == selected_hours]
    fig = px.pie(filtered_df, names=selected_condition, title=f'Percentage of {selected_condition} for {selected_hours} hours of sleep')
    fig.update_traces(textinfo='label+percent', insidetextorientation='radial')
    return fig

@app.callback(
    Output('slider-output-container', 'children'),
    [Input('sleep-hours-slider', 'value')]
)
def update_slider_label(value):
    return f'Selected Sleep Hours: {value}'

@app.callback(
    Output('difficulty-histogram', 'figure'),
    [Input('difficulty-dropdown', 'value')]
)
def update_difficulty_histogram(selected_difficulty):
    fig = px.histogram(df, x='GeneralHealth', color=selected_difficulty, color_discrete_map={'True':'blue', 'False':'pink'}, barmode='group')
    return fig

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('scatter-yaxis-radioitems', 'value')]
)
def update_scatter_plot(selected_state, selected_yaxis):
    filtered_df = df[df['State'] == selected_state]
    fig = px.scatter(filtered_df, x='BMI', y=selected_yaxis)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)