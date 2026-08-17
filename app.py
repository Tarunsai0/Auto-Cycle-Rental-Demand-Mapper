import gradio as gr
import pandas as pd
import joblib

# Load model and data
model_pipeline = joblib.load("cycle_demand_model.pkl")

station_analysis = pd.read_csv("final_station_analysis.csv")
redistribution = pd.read_csv("final_bike_redistribution.csv")

stations = station_analysis["start_station"].unique().tolist()


def convert_to_demand_level(value):
    if value < 1.5:
        return "Low"
    elif value < 2.5:
        return "Medium"
    else:
        return "High"


def predict_demand(
    start_station,
    start_hour,
    day_of_week,
    temperature,
    is_weekend,
    is_peak_hour,
    previous_day_demand,
    previous_demand
):

    input_data = pd.DataFrame({
        "start_hour": [start_hour],
        "day_of_week": [day_of_week],
        "is_weekend": [is_weekend],
        "is_peak_hour": [is_peak_hour],
        "temperature_c": [temperature],
        "previous_day_demand": [previous_day_demand],
        "previous_demand": [previous_demand],
        "start_station": [start_station]
    })

    prediction = model_pipeline.predict(input_data)[0]

    demand_level = convert_to_demand_level(prediction)

    selected_station = station_analysis[
        station_analysis["start_station"] == start_station
    ]

    if not selected_station.empty:
        station_info = selected_station.iloc[0]

        avg_bikes = round(
            station_info["avg_bikes_available"], 2
        )

        net_flow = int(station_info["net_flow"])

        shortage_score = round(
            station_info["shortage_score"], 2
        )

    else:
        avg_bikes = "N/A"
        net_flow = "N/A"
        shortage_score = "N/A"

    return (
        round(prediction, 2),
        demand_level,
        avg_bikes,
        net_flow,
        shortage_score
    )


with gr.Blocks(title="Auto Cycle-Rental Demand Mapper") as demo:

    gr.Markdown(
        """
        # 🚲 Auto Cycle-Rental Demand Mapper

        ### Machine Learning System for Cycle Demand Prediction
        Predict cycle demand and identify stations requiring bike redistribution.
        """
    )

    with gr.Row():

        with gr.Column():

            start_station = gr.Dropdown(
                choices=stations,
                label="Start Station",
                value=stations[0]
            )

            start_hour = gr.Slider(
                minimum=0,
                maximum=23,
                value=8,
                step=1,
                label="Start Hour"
            )

            day_of_week = gr.Slider(
                minimum=0,
                maximum=6,
                value=1,
                step=1,
                label="Day of Week (0 = Monday)"
            )

            temperature = gr.Number(
                value=28,
                label="Temperature (°C)"
            )

        with gr.Column():

            is_weekend = gr.Radio(
                choices=[0, 1],
                value=0,
                label="Is Weekend?"
            )

            is_peak_hour = gr.Radio(
                choices=[0, 1],
                value=1,
                label="Is Peak Hour?"
            )

            previous_day_demand = gr.Number(
                value=1,
                label="Previous Day Demand"
            )

            previous_demand = gr.Number(
                value=1,
                label="Previous Demand"
            )

    predict_button = gr.Button(
        "🚀 Predict Demand",
        variant="primary"
    )

    gr.Markdown("## 📊 Prediction Result")

    with gr.Row():

        predicted_demand = gr.Number(
            label="Predicted Demand"
        )

        demand_level = gr.Textbox(
            label="Demand Level"
        )

    gr.Markdown("## 📍 Station Status")

    with gr.Row():

        avg_bikes = gr.Number(
            label="Average Bikes Available"
        )

        net_flow = gr.Number(
            label="Net Flow"
        )

        shortage_score = gr.Number(
            label="Shortage Score"
        )

    predict_button.click(
        fn=predict_demand,
        inputs=[
            start_station,
            start_hour,
            day_of_week,
            temperature,
            is_weekend,
            is_peak_hour,
            previous_day_demand,
            previous_demand
        ],
        outputs=[
            predicted_demand,
            demand_level,
            avg_bikes,
            net_flow,
            shortage_score
        ]
    )

    gr.Markdown("## 🚚 Recommended Bike Redistribution")

    redistribution_table = gr.Dataframe(
        value=redistribution,
        label="Recommended Bike Movement",
        interactive=False
    )


demo.launch()
