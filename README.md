
# 🚲 Auto Cycle-Rental Demand Mapper
 Project Demo

[Open Google Colab Notebook](https://colab.research.google.com/drive/1jz1ZyQ4hBRmeDo4o6icEdAaq3UR4oHlK?usp=sharing)
An end-to-end Machine Learning project that predicts cycle rental demand at different stations and recommends how bikes should be redistributed between stations.

## 🎯 Problem Statement

In college cycle-sharing systems, bikes can become concentrated at some stations while other stations experience shortages.

This project uses historical rental data and Machine Learning to:

- Predict cycle rental demand
- Analyze station-level demand
- Identify potential shortage and surplus stations
- Recommend bike redistribution routes
- Provide an interactive Streamlit dashboard

## 📊 Dataset

The project uses a dataset containing 20,000 cycle-rental records.

Important features include:

- Rental ID
- Date
- Start time
- End time
- Start station
- End station
- Start hour
- Duration
- User type
- Weather
- Temperature
- Weekend indicator
- Bikes available at start
- Bikes available at end
- Demand level

## ⚙️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest
- Matplotlib
- Streamlit
- Joblib

## 🔧 Machine Learning Workflow

```text
Raw Rental Data
      ↓
Data Cleaning
      ↓
Feature Engineering
      ↓
Lag Features
      ↓
Station Encoding
      ↓
Train/Test Split
      ↓
Random Forest Regression
      ↓
Demand Prediction
      ↓
Station Analysis
      ↓
Shortage/Surplus Detection
      ↓
Bike Redistribution
