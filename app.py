from flask import Flask, render_template, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

# --- Fuzzy Logic System (Predicting Temperature Outlook) ---

# Define the Antecedents (Inputs)
precipitation = ctrl.Antecedent(np.arange(0, 101, 1), 'precipitation')
wind_speed = ctrl.Antecedent(np.arange(0, 61, 1), 'wind_speed')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')

# Define fuzzy sets for Precipitation
precipitation['none'] = fuzz.trimf(precipitation.universe, [0, 0, 10])
precipitation['light'] = fuzz.trimf(precipitation.universe, [5, 15, 25])
precipitation['moderate'] = fuzz.trimf(precipitation.universe, [20, 40, 60])
precipitation['heavy'] = fuzz.trimf(precipitation.universe, [50, 75, 100])

# Define fuzzy sets for Wind Speed
wind_speed['calm'] = fuzz.trimf(wind_speed.universe, [0, 0, 10])
wind_speed['light'] = fuzz.trimf(wind_speed.universe, [5, 15, 25])
wind_speed['moderate'] = fuzz.trimf(wind_speed.universe, [20, 35, 50])
wind_speed['strong'] = fuzz.trimf(wind_speed.universe, [40, 50, 60])

# Define fuzzy sets for Humidity
humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 30])
humidity['medium'] = fuzz.trimf(humidity.universe, [20, 50, 80])
humidity['high'] = fuzz.trimf(humidity.universe, [70, 90, 100])

# Define the Consequent (Output - Temperature Outlook)
# We'll use a numerical range that maps to the temperature descriptions
temperature_outlook_value = ctrl.Consequent(np.arange(0, 11, 1), 'temperature_outlook_value')
temperature_outlook_value['cold'] = fuzz.trimf(temperature_outlook_value.universe, [0, 0, 3])
temperature_outlook_value['cool'] = fuzz.trimf(temperature_outlook_value.universe, [2, 4, 6])
temperature_outlook_value['mild'] = fuzz.trimf(temperature_outlook_value.universe, [5, 7, 9])
temperature_outlook_value['hot'] = fuzz.trimf(temperature_outlook_value.universe, [8, 10, 10])


# Define the Rules for predicting Temperature Outlook
# These rules link input weather conditions to a predicted temperature description
rule1 = ctrl.Rule(precipitation['heavy'] | humidity['high'], temperature_outlook_value['cool']) # Heavy rain/high humidity might feel cooler
rule2 = ctrl.Rule(wind_speed['strong'], temperature_outlook_value['cold']) # Strong wind feels colder
rule3 = ctrl.Rule(precipitation['none'] & wind_speed['calm'] & humidity['low'], temperature_outlook_value['hot']) # Clear, calm, dry weather can be hot
rule4 = ctrl.Rule(precipitation['light'] & humidity['medium'], temperature_outlook_value['mild']) # Light rain/medium humidity can feel mild
rule5 = ctrl.Rule(wind_speed['light'] & humidity['high'], temperature_outlook_value['cool']) # Light wind with high humidity
rule6 = ctrl.Rule(precipitation['none'] & wind_speed['light'] & humidity['medium'], temperature_outlook_value['mild']) # Clear, light wind, medium humidity
rule7 = ctrl.Rule(precipitation['none'] & wind_speed['calm'] & humidity['medium'], temperature_outlook_value['mild']) # Clear, calm, medium humidity
rule8 = ctrl.Rule(precipitation['moderate'] | wind_speed['moderate'], temperature_outlook_value['cool']) # Moderate rain or wind
rule9 = ctrl.Rule(precipitation['none'] & humidity['high'], temperature_outlook_value['mild']) # Clear, high humidity might feel mild

# Add more rules to cover various combinations and refine the temperature prediction.
# This is just a starting point.

# Create the Control System
temperature_outlook_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
temperature_outlook_sim = ctrl.ControlSystemSimulation(temperature_outlook_ctrl)

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page with the weather prediction form and results.
    """
    prediction_result = None
    if request.method == 'POST':
        try:
            # Get input values from the form (Temperature is NOT an input for prediction now)
            input_precipitation = float(request.form['precipitation'])
            # input_temperature = float(request.form['temperature']) # Removed as input
            input_wind_speed = float(request.form['wind_speed'])
            input_humidity = float(request.form['humidity'])

            # Set input values in the fuzzy system
            temperature_outlook_sim.input['precipitation'] = input_precipitation
            temperature_outlook_sim.input['wind_speed'] = input_wind_speed
            temperature_outlook_sim.input['humidity'] = input_humidity

            # Compute the prediction
            temperature_outlook_sim.compute()
            predicted_outlook_value = temperature_outlook_sim.output['temperature_outlook_value']

            # Determine the descriptive temperature category based on the defuzzified value
            # These thresholds should align with the output fuzzy sets
            if 0 <= predicted_outlook_value <= 3:
                outlook_category = "Cold"
            elif 3 < predicted_outlook_value <= 6:
                outlook_category = "Cool"
            elif 6 < predicted_outlook_value <= 9:
                outlook_category = "Mild"
            else:
                outlook_category = "Hot"

            prediction_result = {
                'precipitation': input_precipitation,
                # 'temperature': input_temperature, # Removed from result
                'wind_speed': input_wind_speed,
                'humidity': input_humidity,
                'predicted_value': predicted_outlook_value,
                'outlook_category': outlook_category # This is now the descriptive temperature
            }

        except ValueError:
            prediction_result = {'error': 'Invalid input. Please enter numerical values.'}
        except Exception as e:
            prediction_result = {'error': f'An error occurred: {e}'}

    # Render the HTML template, passing the prediction result if available
    return render_template('index_temp.html', prediction_result=prediction_result) # Using a new template name

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)