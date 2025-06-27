from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta
import pytz
from flask_cors import CORS
import matplotlib.pyplot as plt
import base64
from prophet import Prophet

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set IST timezone
IST = pytz.timezone('Asia/Kolkata')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        try:
            # Read CSV
            df = pd.read_csv(file)
            if 'ds' not in df.columns or 'y' not in df.columns:
                return jsonify({'error': 'CSV must contain "ds" (date) and "y" (sales) columns'}), 400
            
            # Convert ds to datetime
            df['ds'] = pd.to_datetime(df['ds'])
            
            # Forecast parameters from form
            forecast_days = int(request.form.get('forecast_days', 30))
            confidence_interval = float(request.form.get('confidence_interval', 0.95))
            
            # Use current date and time (3:00 PM IST, June 27, 2025) as base
            current_time = IST.localize(datetime(2025, 6, 27, 15, 0))
            last_date = df['ds'].max() if not df.empty else current_time
            
            # Prepare data for Prophet
            df_prophet = df.rename(columns={'ds': 'ds', 'y': 'y'})  # Ensure column names match Prophet's expectation
            
            # Initialize and fit Prophet model
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=True,
                interval_width=confidence_interval  # Sets the confidence interval (e.g., 0.95 for 95%)
            )
            model.fit(df_prophet)
            
            # Create future dataframe for forecasting
            future = model.make_future_dataframe(periods=forecast_days)
            forecast = model.predict(future)
            
            # Extract forecast data for the future period
            forecast_data = forecast.tail(forecast_days).reset_index(drop=True)
            forecast_data = forecast_data.rename(columns={
                'ds': 'date',
                'yhat': 'sales',
                'yhat_lower': 'lower',
                'yhat_upper': 'upper'
            })
            
            # Extract trend and seasonality components
            trend = forecast_data['trend'].values
            yearly = forecast_data['yearly'].values
            weekly = forecast_data['weekly'].values
            daily = forecast_data['daily'].values
            
            # Update forecast_data with components
            forecast_data = pd.DataFrame({
                'date': forecast_data['date'],
                'sales': forecast_data['sales'],
                'upper': forecast_data['upper'],
                'lower': forecast_data['lower'],
                'trend': trend,
                'yearly': yearly,
                'weekly': weekly,
                'daily': daily
            })
            
            # Generate components plot
            plt.figure(figsize=(6, 4))
            plt.plot(forecast_data['date'], trend, label='Trend', color='green')
            plt.plot(forecast_data['date'], yearly, label='Yearly Seasonality', color='pink')
            plt.plot(forecast_data['date'], weekly, label='Weekly Seasonality', color='orange')
            plt.plot(forecast_data['date'], daily, label='Daily Seasonality', color='purple')
            plt.title('Trend and Seasonality Components')
            plt.xlabel('Date')
            plt.ylabel('Value')
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save plot to a BytesIO buffer and encode as base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            components_plot = base64.b64encode(buffer.getvalue()).decode('utf-8')
            components_plot = f'data:image/png;base64,{components_plot}'
            plt.close()
            
            # Summary statistics (convert to native Python types)
            summary = {
                'avg_sales': float(df['y'].mean()) if not df.empty else 0.0,
                'median_sales': float(df['y'].median()) if not df.empty else 0.0,
                'std_sales': float(df['y'].std()) if not df.empty else 0.0,
                'max_sales': float(df['y'].max()) if not df.empty else 0.0,
                'min_sales': float(df['y'].min()) if not df.empty else 0.0,
                'total_records': int(len(df))
            }
            
            # Mock insights (using Prophet's peak day)
            peak_day = df.loc[df['y'].idxmax(), 'ds'].strftime('%Y-%m-%d') if not df.empty else current_time.strftime('%Y-%m-%d')
            outliers = df[df['y'] > df['y'].mean() + 3 * df['y'].std()].copy()
            outliers = outliers.rename(columns={'ds': 'date', 'y': 'sales'})  # Rename columns to match frontend
            insights = {
                'peak_day': peak_day,
                'growth_rate': float((forecast_data['sales'].iloc[-1] - forecast_data['sales'].iloc[0]) / forecast_data['sales'].iloc[0]) if not forecast_data.empty else 0.0,
                'outliers': outliers.to_dict('records') if not outliers.empty else [],
                'correlations': {'trend': 0.9}  # Mock correlation, could be refined with Prophet's trend fit
            }
            
            response = {
                'summary': summary,
                'forecast': forecast_data.to_dict('records'),
                'insights': insights,
                'components_plot': components_plot
            }
            return jsonify(response), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/download/csv')
def download_csv():
    current_time = IST.localize(datetime(2025, 6, 27, 15, 0))
    future_dates = [current_time + timedelta(days=i) for i in range(1, 31)]
    # Using Prophet-like forecast for consistency (mock data)
    forecast = np.linspace(100, 110, 30) + np.sin(np.linspace(0, 2 * np.pi, 30)) * 10
    df = pd.DataFrame({'date': future_dates, 'sales': forecast})
    output = io.StringIO()
    df.to_csv(output, index=False, date_format='%Y-%m-%d %H:%M:%S')
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        attachment_filename='forecast.csv'
    )

@app.route('/download/pdf')
def download_pdf():
    buffer = io.BytesIO()
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Sales Forecast Report")
    c.drawString(100, 730, f"Generated on: {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    c.drawString(100, 710, "Summary Statistics:")
    c.drawString(120, 690, f"Average Sales: 197.70")  # Mock data for demo
    c.drawString(120, 670, f"Median Sales: 109.00")
    c.drawString(120, 650, f"Max Sales: 1000.00")
    c.drawString(120, 630, f"Peak Day: 2025-06-10")
    c.showPage()
    c.save()
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        attachment_filename='forecast_report.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)