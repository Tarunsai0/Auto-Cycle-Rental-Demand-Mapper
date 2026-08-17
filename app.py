import streamlit as st
import pandas as pd
import joblib




st.set_page_config(
    page_title="Auto Cycle-Rental Demand Mapper",
    page_icon="🚲",
    layout="wide"
)




st.title("🚲 Auto Cycle-Rental Demand Mapper")

st.write(
    "Machine Learning system for cycle demand prediction "
    "and bike redistribution."
)



model_pipeline = joblib.load("cycle_demand_model.pkl")

station_analysis = pd.read_csv(
    "final_station_analysis.csv"
)

redistribution = pd.read_csv(
    "final_bike_redistribution.csv"
)


stations = station_analysis[
    "start_station"
].unique().tolist()




def convert_to_demand_level(value):

    if value < 1.5:
        return "Low"

    elif value < 2.5:
        return "Medium"

    else:
        return "High"



st.header("🔮 Predict Cycle Demand")


col1, col2 = st.columns(2)


with col1:

    start_station = st.selectbox(
        "Select Start Station",
        stations
    )

    start_hour = st.slider(
        "Start Hour",
        min_value=0,
        max_value=23,
        value=8
    )

    day_of_week = st.slider(
        "Day of Week",
        min_value=0,
        max_value=6,
        value=1,
        help="0 = Monday, 6 = Sunday"
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        max_value=50.0,
        value=28.0
    )


with col2:

    is_weekend = st.selectbox(
        "Is Weekend?",
        [0, 1]
    )

    is_peak_hour = st.selectbox(
        "Is Peak Hour?",
        [0, 1]
    )

    previous_day_demand = st.number_input(
        "Previous Day Demand",
        min_value=0.0,
        value=1.0
    )

    previous_demand = st.number_input(
        "Previous Demand",
        min_value=0.0,
        value=1.0
    )




if st.button(
    "🚀 Predict Demand",
    use_container_width=True
):

    input_data = pd.DataFrame({

        "start_hour": [start_hour],

        "day_of_week": [day_of_week],

        "is_weekend": [is_weekend],

        "is_peak_hour": [is_peak_hour],

        "temperature_c": [temperature],

        "previous_day_demand": [
            previous_day_demand
        ],

        "previous_demand": [
            previous_demand
        ],

        "start_station": [
            start_station
        ]
    })


    try:

        prediction = model_pipeline.predict(
            input_data
        )[0]


        demand_level = convert_to_demand_level(
            prediction
        )


        st.success(
            "Prediction completed successfully!"
        )


       
        

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Predicted Demand",
                round(prediction, 2)
            )


        with col2:

            st.metric(
                "Demand Level",
                demand_level
            )



        selected_station = station_analysis[
            station_analysis["start_station"]
            == start_station
        ]


        if not selected_station.empty:

            station_info = selected_station.iloc[0]


            st.subheader(
                "📍 Current Station Status"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Average Bikes Available",
                    round(
                        station_info[
                            "avg_bikes_available"
                        ],
                        2
                    )
                )


            with col2:

                st.metric(
                    "Net Flow",
                    int(
                        station_info[
                            "net_flow"
                        ]
                    )
                )


            with col3:

                st.metric(
                    "Shortage Score",
                    round(
                        station_info[
                            "shortage_score"
                        ],
                        2
                    )
                )


    except Exception as e:

        st.error(
            "Prediction failed."
        )

        st.exception(e)




st.header(
    "📊 Station Demand Analysis"
)


selected_station_view = st.selectbox(
    "View Station Details",
    stations,
    key="station_analysis"
)


selected = station_analysis[
    station_analysis["start_station"]
    == selected_station_view
]


st.dataframe(
    selected,
    use_container_width=True
)




st.header(
    "🚚 Recommended Bike Redistribution"
)


st.write(
    "Recommended movement of bikes from surplus "
    "stations to stations with higher shortage pressure."
)


st.dataframe(
    redistribution,
    use_container_width=True
)
