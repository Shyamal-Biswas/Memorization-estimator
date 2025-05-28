from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Memorization Estimator</title>
<h2>🧠 Enter a Definition to Estimate Memorization Time</h2>
<form method=post>
  <textarea name=definition rows=6 cols=80 placeholder="Type your definition here..."></textarea><br><br>
  <input type=submit value="Estimate">
</form>
{% if result %}
  <h3>Difficulty: {{ result.difficulty }}</h3>
  <p>Estimated Time Range: {{ result.time_range }} minutes</p>
  <p>Exact Time: {{ result.exact_time }} minutes</p>
{% endif %}
"""

REFERENCE_TIME = 17

def estimate_time(def_text):
    if len(def_text.split()) < 10:
        difficulty = "easy"
        factor = (0.6, 0.8)
    elif len(def_text.split()) < 25:
        difficulty = "medium"
        factor = (1.0, 1.2)
    else:
        difficulty = "hard"
        factor = (1.75, 2.0)
    low, high = round(REFERENCE_TIME * factor[0]), round(REFERENCE_TIME * factor[1])
    exact = round((low + high) / 2 + random.uniform(-1, 1), 1)
    return {
        "difficulty": difficulty,
        "time_range": f"{low}-{high}",
        "exact_time": exact
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form["definition"]
        result = estimate_time(user_input)
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
      
