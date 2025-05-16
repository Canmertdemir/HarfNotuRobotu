from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def anasayfa():
    return render_template('home.html')

@app.route('/not-hesaplama')
def home():
    return render_template('index.html')

@app.route('/quiz-ortalama', methods=['POST'])
def quiz_ortalama():
    data = request.get_json()
    q_avg = sum([data['quiz1'], data['quiz2'], data['quiz3'], data['quiz4']]) / 4
    return jsonify({'quiz_ortalama': round(q_avg, 2)})

@app.route('/genel-ortalama', methods=['POST'])
def genel_ortalama():
    data = request.get_json()
    quiz_avg = sum([data['quiz1'], data['quiz2'], data['quiz3'], data['quiz4']]) / 4
    genel = quiz_avg * 0.1 + data['vize'] * 0.3 + data['final'] * 0.6
    harf = 'AA' if genel >= 90 else 'BA' if genel >= 85 else 'BB' if genel >= 75 else 'CC'
    return jsonify({'genel_ortalama': round(genel, 2), 'harf_notu': harf})

@app.route('/devamsizlik', methods=['POST'])
def devamsizlik():
    data = request.get_json()
    toplam_saat = data['haftalik_ders_sayisi'] * 14 * (data['teorik_saat'] + (data['uygulama_saat'] if data['uygulamali_mi'] else 0))
    limit = toplam_saat * 0.3
    durum = "Geçerli" if data['devamsizlik'] <= limit else "Devamsızlıktan Kaldı"
    return jsonify({'durum': durum})

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
