EnergyConsumptionPrediction
This repository contains a dataset and tools for predicting energy consumption of a data server located at the Information Technology Center (CTI) of Escuela Superior Politécnica del Litoral (ESPOL). The dataset spans 245 days of high-frequency monitoring (1 Hz) of variables such as voltage, current, active power, frequency, power factor, CPU/GPU/RAM usage, and temperatures, collected from an HP Z440 workstation using an ESP32-based system.
Features

Dataset: Comprehensive energy consumption data for time-series analysis.
Prediction Models: Includes Matlab scripts for linear regression-based energy forecasting, with potential for advanced models like LSTM, XGBoost, or Transformers.
Applications: Optimize energy usage in data centers, support green IT initiatives, and reduce operational costs.
Visualization: Time-series plots for analyzing energy consumption patterns.

Repository Structure

data/: Contains the energy consumption dataset (CSV/MAT format).
src/: Matlab scripts for data processing and prediction models.
PlotData: Visualizations of monitored variables (e.g., power, CPU usage).

Getting Started

Clone the repository: git clone https://github.com/vasanza/EnergyConsumptionPrediction.git
Place the dataset in the data/ folder.
Run Matlab scripts in src/ for preprocessing and prediction.
Explore advanced models (e.g., LSTM, XGBoost) using Python for enhanced accuracy.

Requirements

Matlab (for provided scripts) or Python (for advanced models).
Libraries: TensorFlow, PyTorch, XGBoost, scikit-learn (optional for advanced models).
Recommended: GPU for deep learning models.

Citation
Please cite the dataset if used: IEEE DataPort - Data Server Energy Consumption Dataset.
License
This project is licensed under the MIT License.
