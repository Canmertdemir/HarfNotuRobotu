from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

def quiz_not_kontrol(data):
    for i in range(1, 5):
        quiz_key = f'quiz{i}'
        if not (0 <= data[quiz_key] <= 100):
            return False, f"{quiz_key} skoru 0 ile 100 arasında olmalıdır."
    return True, ""
def vize_final_not_kontrol(data):
    if not (0 <= data['vize'] <= 100):
        return False, "Vize skoru 0 ile 100 arasında olmalıdır."
    if not (0 <= data['final'] <= 100):
        return False, "Final skoru 0 ile 100 arasında olmalıdır."
    return True, ""

@app.route('/')
def anasayfa():
    return render_template('home.html')

@app.route('/not-hesaplama')
def home():
    return render_template('index.html')

@app.route('/quiz-ortalama', methods=['POST'])
def quiz_ortalama():

    data = request.get_json()

    gecerli , mesaj = quiz_not_kontrol(data)
    if not gecerli:
        return jsonify({'Hata!': mesaj})

    q_avg = sum([data['quiz1'], data['quiz2'], data['quiz3'], data['quiz4']]) / 4
    return jsonify({'quiz_ortalama': round(q_avg, 2)})

@app.route('/genel-ortalama', methods=['POST'])
def genel_ortalama():
    data = request.get_json()

    gecerli , mesaj = vize_final_not_kontrol(data)
    if not gecerli:
        return jsonify({'Hata!': mesaj})

    quiz_avg = quiz_ortalama()
    genel = quiz_avg * 0.1 + data['vize'] * 0.3 + data['final'] * 0.6
    harf = 'AA' if genel >= 90 else 'BA' if genel >= 85 else 'BB' if genel >= 75 else 'CC'
    return jsonify({'genel_ortalama': round(genel, 2), 'harf_notu': harf})

@app.route('/devamsizlik', methods=['POST'])
def devamsizlik():
    data = request.get_json()

    if  data['uygulamali'] == 0:
        toplam_devamsizlik_hakki = (15 * data['teorik']) * 0.4
    else:
        toplam_devamsizlik_hakki = (15 * data['uygulama']) * 0.3

    if data['devamsizlik'] > toplam_devamsizlik_hakki:
        durum = "Devamsızlıktan kaldı."
    else:
        durum = "Derse devaalı."

    return jsonify({'durum': durum})

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
