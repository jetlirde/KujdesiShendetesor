from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate_bmi", methods=["POST"])
def calculate_bmi():
    data = request.json
    pesha = data.get("pesha")
    gjatesia = data.get("gjatesia")
    mosha = data.get("mosha")  # Marrim edhe moshën nga kërkesa

    # Kontrollo që të gjitha të dhënat janë të plota dhe të sakta
    if not (pesha and gjatesia and mosha):
        return jsonify({"error": "Të gjitha fushat janë të detyrueshme"}), 400

    try:
        pesha = float(pesha)
        gjatesia = float(gjatesia)
        mosha = int(mosha)
    except ValueError:
        return jsonify({"error": "Të dhënat e dhëna nuk janë të sakta"}), 400

    # Llogaritja e BMI-së
    bmi = round(pesha / (gjatesia ** 2), 2)

    # Përcaktimi i kategorisë së BMI-së dhe sugjerimet për dietën dhe ushtrimet
    if bmi < 18.5:
        category = "Nën peshë"
        suggestions = {
            "dieta": "Shtoni ushqime me proteina dhe karbohidrate të shëndetshme në dietën tuaj.",
            "ushtrime": "Përqendrohuni te ushtrime për forcim dhe ndërtim muskujsh."
        }
    elif 18.5 <= bmi < 24.9:
        category = "Peshë normale"
        suggestions = {
            "dieta": "Ruani një dietë të ekuilibruar dhe të shëndetshme.",
            "ushtrime": "Kryeni aktivitete të rregullta fizike si ecja ose vrapimi i lehtë."
        }
    elif 25 <= bmi < 29.9:
        category = "Mbipeshë"
        suggestions = {
            "dieta": "Ulni marrjen e ushqimeve me shumë kalori dhe përqendrohuni te perimet dhe frutat.",
            "ushtrime": "Rrisni aktivitetet kardio si ecja e shpejtë apo çiklizmi."
        }
    else:
        category = "Obeziteti"
        suggestions = {
            "dieta": "Konsultohuni me një dietolog për një plan të personalizuar dhe ulni ushqimet me shumë yndyrë.",
            "ushtrime": "Kryeni aktivitete të moderuara me udhëzime profesionale."
        }

    return jsonify({
        "bmi": bmi,
        "category": category,
        "mosha": mosha,
        "suggestions": suggestions
    })

@app.route("/bmi_chart_data", methods=["GET"])
def bmi_chart_data():
    pesha_values = list(range(40, 151, 5))  # Pesha nga 40kg deri në 150kg me interval 5kg
    gjatesia = float(request.args.get("gjatesia", 1.7))  # Marrim gjatësinë nga query parameter (default 1.7m)
    bmi_values = [round(p / (gjatesia ** 2), 2) for p in pesha_values]
    return jsonify({"pesha": pesha_values, "bmi": bmi_values})

if __name__ == "__main__":
    app.run(debug=True)
