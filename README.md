# Sales Forecasting Dashboard

A web-based dashboard for uploading sales data, generating forecasts, and analyzing trends and seasonality using Python (Flask) and JavaScript (Chart.js).

## Overview

This project provides an interactive dashboard to:
- Upload CSV files containing sales data with 'ds' (date) and 'y' (sales) columns.
- Generate sales forecasts with customizable parameters (forecast days, seasonality mode, confidence interval).
- Visualize forecasted sales, trends, and seasonality components.
- Identify outliers and provide summary statistics and key insights.

The dashboard is built with a Flask backend for data processing and a responsive frontend using HTML, CSS (Tailwind), and Chart.js for visualizations.

## Features

- **Data Upload**: Upload CSV files to analyze sales data.
- **Forecast Generation**: Generate forecasts with options for 7, 30, 90, or 180 days, additive or multiplicative seasonality, and 80%, 95%, or 99% confidence intervals.
- **Visualizations**: Display forecasted sales, trend, and seasonality components using interactive charts.
- **Insights**: View summary statistics, peak sales day, growth rate, outliers, and correlations.
- **Downloads**: Export forecasts as CSV, charts as PNG, or a summary report as PDF.
- **Dark Mode**: Toggle between light and dark themes.
- **Responsive Design**: Works on desktop and mobile devices.

## Prerequisites

- Python 3.x
- Node.js (for frontend dependencies, if needed)
- Required Python packages:
  - `flask`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `pytz`
  - `flask-cors`
  - `reportlab`

Install dependencies using:
```bash
pip install flask pandas numpy matplotlib pytz flask-cors reportlab
A modern web browser (Chrome, Firefox, Edge, etc.)
Installation
Clone the repository:
bash
git clone <repository-url>
cd sales-forecasting-dashboard
Install the required Python packages:
bash

pip install -r requirements.txt
(Note: Create a requirements.txt file with the listed packages if not already present.)
Ensure the index.html file is in a templates folder and the Flask app (app.py) is in the project root.
Run the Flask application:

bash
python app.py
Open your browser and navigate to http://localhost:5000.

Usage
Upload Data:
Click the "Upload Sales Data (CSV)" input and select a CSV file.
The CSV must contain 'ds' (date in YYYY-MM-DD format) and 'y' (sales) columns.

Configure Forecast:
Select the forecast period (7, 30, 90, or 180 days).
Choose the seasonality mode (additive or multiplicative).
Set the confidence interval (80%, 95%, or 99%).
Optionally save preferences for future use.

Generate Forecast:
Click "Generate Forecast" to process the data.
Wait for the progress bar to complete, then view the results.

Explore Tabs:
Data Preview: View the uploaded data table.
Forecast: See charts for forecasted sales, trend, and seasonality.
Insights: Check summary statistics, key insights, outliers, and a seasonality/trend plot.
Download Outputs:
Download the forecast as a CSV file.
Save charts as a PNG image.
Export a PDF report with summary statistics.

Sample Data
A sample CSV file (sales_data_50_with_outliers.csv) is included for testing. It contains 50 days of sales data with 3 outliers.

Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your changes. Ensure to:

Follow the existing code style.
Add tests or documentation for new features.
Update the README if necessary.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or support, please open an issue on the repository or contact the maintainer at su.karthikeyan17@gmail.com.

Acknowledgments
Flask for the backend framework.
Chart.js for interactive charts.
Tailwind CSS for responsive styling.
AOS for animations.
