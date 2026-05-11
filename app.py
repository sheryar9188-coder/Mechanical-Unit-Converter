from flask import Flask, render_template_string, request

app = Flask(__name__)

categories = {
    "Length": {
        "meter": 1,
        "kilometer": 0.001,
        "centimeter": 100,
        "millimeter": 1000,
        "inch": 39.3701,
        "foot": 3.28084,
        "yard": 1.09361,
        "mile": 0.000621371,
    },
    "Force": {
        "newton": 1,
        "kilonewton": 0.001,
        "dyne": 100000,
        "poundForce": 0.224809,
    },
    "Pressure": {
        "pascal": 1,
        "kilopascal": 0.001,
        "bar": 0.00001,
        "psi": 0.000145038,
        "atmosphere": 0.00000986923,
    },
    "Speed": {
        "mps": 1,
        "kph": 3.6,
        "mph": 2.23694,
        "knot": 1.94384,
    },
    "Torque": {
        "nm": 1,
        "lbft": 0.737562,
        "kgfm": 0.101972,
    },
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Mechanical Unit Converter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #111827;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background: #1f2937;
            padding: 30px;
            border-radius: 15px;
            width: 400px;
        }
        h1 {
            text-align: center;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border-radius: 8px;
            border: none;
        }
        button {
            background: cyan;
            color: black;
            font-weight: bold;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            text-align: center;
            font-size: 24px;
            color: cyan;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Mechanical Unit Converter</h1>

        <form method="POST">
            <label>Category</label>
            <select name="category" onchange="this.form.submit()">
                {% for cat in categories.keys() %}
                    <option value="{{cat}}" {% if cat == category %}selected{% endif %}>
                        {{cat}}
                    </option>
                {% endfor %}
            </select>

            <label>Value</label>
            <input type="number" step="any" name="value" value="{{value}}" required>

            <label>From Unit</label>
            <select name="from_unit">
                {% for unit in units %}
                    <option value="{{unit}}" {% if unit == from_unit %}selected{% endif %}>
                        {{unit}}
                    </option>
                {% endfor %}
            </select>

            <label>To Unit</label>
            <select name="to_unit">
                {% for unit in units %}
                    <option value="{{unit}}" {% if unit == to_unit %}selected{% endif %}>
                        {{unit}}
                    </option>
                {% endfor %}
            </select>

            <button type="submit">Convert</button>
        </form>

        {% if result is not none %}
            <div class="result">
                Result: {{result}} {{to_unit}}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    category = "Length"
    value = 1
    from_unit = "meter"
    to_unit = "foot"
    result = None

    if request.method == "POST":
        category = request.form["category"]
        value = float(request.form["value"])
        from_unit = request.form["from_unit"]
        to_unit = request.form["to_unit"]

        units = categories[category]

        base_value = value / units[from_unit]
        result = round(base_value * units[to_unit], 4)

    units = list(categories[category].keys())

    return render_template_string(
        HTML,
        categories=categories,
        category=category,
        units=units,
        value=value,
        from_unit=from_unit,
        to_unit=to_unit,
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)
