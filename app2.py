from flask import Flask, render_template, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

# --- Fuzzy Logic System ---

# Define the Antecedents (Inputs)
precipitation = ctrl.Antecedent(np.arange(0, 101, 1), 'precipitation')
temperature = ctrl.Antecedent(np.arange(-20, 41, 1), 'temperature')
wind_speed = ctrl.Antecedent(np.arange(0, 61, 1), 'wind_speed')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')

# Define fuzzy sets for Precipitation
precipitation['none'] = fuzz.trimf(precipitation.universe, [0, 0, 10])
precipitation['light'] = fuzz.trimf(precipitation.universe, [5, 15, 25])
precipitation['moderate'] = fuzz.trimf(precipitation.universe, [20, 40, 60])
precipitation['heavy'] = fuzz.trimf(precipitation.universe, [50, 75, 100])

# Define fuzzy sets for Temperature
temperature['cold'] = fuzz.trimf(temperature.universe, [-20, -10, 0])
temperature['cool'] = fuzz.trimf(temperature.universe, [-5, 10, 25])
temperature['mild'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['hot'] = fuzz.trimf(temperature.universe, [25, 35, 40])

# Define fuzzy sets for Wind Speed
wind_speed['calm'] = fuzz.trimf(wind_speed.universe, [0, 0, 10])
wind_speed['light'] = fuzz.trimf(wind_speed.universe, [5, 15, 25])
wind_speed['moderate'] = fuzz.trimf(wind_speed.universe, [20, 35, 50])
wind_speed['strong'] = fuzz.trimf(wind_speed.universe, [40, 50, 60])

# Define fuzzy sets for Humidity
humidity['low'] = fuzz.trimf(humidity.universe, [0, 15, 30])
humidity['medium'] = fuzz.trimf(humidity.universe, [20, 50, 80])
humidity['high'] = fuzz.trimf(humidity.universe, [70, 85, 100])

# Define the Consequent (Output)
weather_outlook = ctrl.Consequent(np.arange(0, 11, 1), 'weather_outlook')
weather_outlook['bad'] = fuzz.trimf(weather_outlook.universe, [0, 0, 4])
weather_outlook['moderate'] = fuzz.trimf(weather_outlook.universe, [3, 5, 7])
weather_outlook['good'] = fuzz.trimf(weather_outlook.universe, [6, 10, 10])

# Define the Rules
rule1 = ctrl.Rule(precipitation['heavy'] | wind_speed['strong'], weather_outlook['bad'])
rule2 = ctrl.Rule(precipitation['moderate'] & temperature['cold'], weather_outlook['bad'])
rule3 = ctrl.Rule(temperature['hot'] & humidity['high'], weather_outlook['bad'])

rule4 = ctrl.Rule(precipitation['light'] & wind_speed['light'], weather_outlook['moderate'])
rule5 = ctrl.Rule(temperature['cool'] & humidity['medium'], weather_outlook['moderate'])
rule6 = ctrl.Rule(precipitation['none'] & temperature['mild'] & wind_speed['calm'], weather_outlook['good'])
rule7 = ctrl.Rule(precipitation['none'] & temperature['cool'] & humidity['low'], weather_outlook['good'])
rule8 = ctrl.Rule(temperature['mild'] & humidity['medium'] & wind_speed['light'], weather_outlook['moderate'])
rule9 = ctrl.Rule(precipitation['light'] | humidity['high'], weather_outlook['moderate'])
rule10 = ctrl.Rule(wind_speed['moderate'] | temperature['cold'], weather_outlook['bad'])


# Create the Control System
weather_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
weather_prediction_sim = ctrl.ControlSystemSimulation(weather_ctrl)

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page with the weather prediction form and results.
    """
    prediction_result = None
    if request.method == 'POST':
        try:
            # Get input values from the form
            input_precipitation = float(request.form['precipitation'])
            input_temperature = float(request.form['temperature'])
            input_wind_speed = float(request.form['wind_speed'])
            input_humidity = float(request.form['humidity'])

            # Set input values in the fuzzy system
            weather_prediction_sim.input['precipitation'] = input_precipitation
            weather_prediction_sim.input['temperature'] = input_temperature
            weather_prediction_sim.input['wind_speed'] = input_wind_speed
            weather_prediction_sim.input['humidity'] = input_humidity

            # Compute the prediction
            weather_prediction_sim.compute()
            predicted_outlook = weather_prediction_sim.output['weather_outlook']

            # Determine the category based on the defuzzified value
            # These thresholds correspond roughly to the fuzzy sets in the output
            if 0 <= predicted_outlook <= 4:
                outlook_category = "Bad"
            elif 4 < predicted_outlook <= 7:
                outlook_category = "Moderate"
            else:
                outlook_category = "Good"

            prediction_result = {
                'precipitation': input_precipitation,
                'temperature': input_temperature,
                'wind_speed': input_wind_speed,
                'humidity': input_humidity,
                'predicted_value': predicted_outlook,
                'outlook_category': outlook_category
            }

        except ValueError:
            prediction_result = {'error': 'Invalid input. Please enter numerical values.'}
        except Exception as e:
            prediction_result = {'error': f'An error occurred: {e}'}

    # Render the HTML template, passing the prediction result if available
    return render_template('index.html', prediction_result=prediction_result)

if __name__ == '__main__':
    # Run the Flask development server
    # In a production environment, you'd use a production-ready server like Gunicorn or uWSGI
    app.run(debug=True)