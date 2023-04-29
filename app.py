from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
from db import get_table_data
import plotly.express as px


app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    # Retrieve data from the four tables
    temp_data = get_table_data('"CM_HAM_DO_AI1/Temp_value"')
    ph_data = get_table_data('"CM_HAM_PH_AI1/pH_value"')
    do_data = get_table_data('"CM_PID_DO/Process_DO"')
    pressure_data = get_table_data('"CM_PRESSURE/Output"')

    # Create line charts using Plotly
    temp_chart = go.Scatter(
        x=temp_data['time'],
        y=temp_data['value'],
        name='Temperature'
    )

    ph_chart = go.Scatter(
        x=ph_data['time'],
        y=ph_data['value'],
        name='pH'
    )

    do_chart = go.Scatter(
        x=do_data['time'],
        y=do_data['value'],
        name='Distilled Oxygen'
    )

    pressure_chart = go.Scatter(
        x=pressure_data['time'],
        y=pressure_data['value'],
        name='Pressure'
    )

    # Combine charts into a single figure
    fig = go.Figure(
        data=[temp_chart, ph_chart, do_chart, pressure_chart],
        layout=go.Layout(title='Process Data')
    )

    # Convert the Plotly figure to an HTML string
    chart_html = fig.to_html(full_html=False)

    # Create a line chart for each series using Plotly
    data = {'Temperature': temp_data,
    'pH': ph_data,
    'Distilled Oxygen': do_data,
    'Pressure': pressure_data}
    charts = {}
    for series, df in data.items():
        fig = px.line(df, x='time', y='value')
        fig.update_layout(
            title=f'{series} over time',
            xaxis_title='Time',
            yaxis_title=series
        )
        charts[series] = fig.to_html()
    # Pass the start_time and end_time variables to the HTML template
    start_time = '00:00'
    end_time = '06:00'
    # Render the HTML template with the chart HTML
    return render_template('dashboard.html', charts=charts, start_time=start_time, end_time=end_time)


@app.route('/')
def index():
    message = "Good Morning!"
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
