from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# اتصال به جمنای
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel('gemini-3.6-flash')

KNOWN_ALGORITHMS = {
    "bubble sort": {"name": "مرتب‌سازی حبابی", "time": "O(n^2)", "space": "O(1)", "desc": "ساده اما بسیار کند برای داده‌های بزرگ."},
    "quick sort": {"name": "مرتب‌سازی سریع", "time": "O(n log n)", "space": "O(log n)", "desc": "سریع‌ترین در عمل، اما در بدترین حالت O(n^2) می‌شود."},
    "merge sort": {"name": "مرتب‌سازی ادغامی", "time": "O(n log n)", "space": "O(n)", "desc": "نیاز به حافظه اضافی دارد اما همیشه پایدار است."},
    "binary search": {"name": "جستجوی دودویی", "time": "O(log n)", "space": "O(1)", "desc": "فقط روی آرایه‌های مرتب شده کار می‌کند."},
    "linear search": {"name": "جستجوی خطی", "time": "O(n)", "space": "O(1)", "desc": "تک تک عناصر را چک می‌کند."}
}

COMPLEXITY_RANKS = {"O(1)": 1, "O(log n)": 2, "O(n)": 3, "O(n log n)": 4, "O(n^2)": 5}

def get_winner(val1, val2):
    rank1 = COMPLEXITY_RANKS.get(val1, 99)
    rank2 = COMPLEXITY_RANKS.get(val2, 99)
    if rank1 < rank2: return "algo1"
    elif rank2 < rank1: return "algo2"
    else: return "tie"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/compare_names', methods=['POST'])
def compare_names():
    data = request.json
    name1 = data.get('algo1', '').strip().lower()
    name2 = data.get('algo2', '').strip().lower()

    res1 = KNOWN_ALGORITHMS.get(name1, {"error": "یافت نشد"})
    res2 = KNOWN_ALGORITHMS.get(name2, {"error": "یافت نشد"})

    verdict = {}
    if "error" not in res1 and "error" not in res2:
        verdict['time'] = get_winner(res1['time'], res2['time'])
        verdict['space'] = get_winner(res1['space'], res2['space'])

    return jsonify({"algo1": res1, "algo2": res2, "verdict": verdict})

@app.route('/api/compare_codes', methods=['POST'])
def compare_codes():
    data = request.json
    code1 = data.get('code1', '')
    code2 = data.get('code2', '')

    if not code1 or not code2:
        return jsonify({"success": False, "error": "Codes are empty!"})

    # پرامپت سخت‌گیرانه برای دریافت پاسخ انگلیسی، کوتاه و دقیق
    prompt = f"""
    Analyze these two Python codes and compare their time and space complexity in English. Do not mention any AI or models. Keep it extremely short and clean.
    
    Code A:
    {code1}
    
    Code B:
    {code2}
    
    Strictly format your response like this:
    - Code A Complexity: Time O(...), Space O(...)
    - Code B Complexity: Time O(...), Space O(...)
    - Speed Winner: [Code A / Code B / Tie] (short reason)
    - Memory Winner: [Code A / Code B / Tie] (short reason)
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"success": True, "ai_report": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)