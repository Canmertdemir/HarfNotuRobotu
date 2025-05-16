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

def quiz_ortalama_hesapla(data):
    return sum([data['quiz1'], data['quiz2'], data['quiz3'], data['quiz4']]) / 4

@app.route('/quiz-ortalama', methods=['POST'])
def quiz_ortalama():
    data = request.get_json()

    gecerli , mesaj = quiz_not_kontrol(data)
    if not gecerli:
        return jsonify({'Hata!': mesaj})

    q_avg = quiz_ortalama_hesapla(data)
    return jsonify({'quiz_ortalama': round(q_avg, 2)})

@app.route('/genel-ortalama', methods=['POST'])
def genel_ortalama():
    data = request.get_json()

    gecerli , mesaj = vize_final_not_kontrol(data)
    if not gecerli:
        return jsonify({'Hata!': mesaj})

    gecerli_quiz, mesaj_quiz = quiz_not_kontrol(data)
    if not gecerli_quiz:
        return jsonify({'Hata!': mesaj_quiz})

    quiz_avg = quiz_ortalama_hesapla(data)

    genel = quiz_avg * 0.1 + data['vize'] * 0.3 + data['final'] * 0.6
    harf = 'AA' if genel >= 90 else 'BA' if genel >= 85 else 'BB' if genel >= 75 else 'CC'

    return jsonify({'genel_ortalama': round(genel, 2), 'harf_notu': harf})


@app.route('/devamsizlik', methods=['POST'])
def devamsizlik():
    data = request.get_json()

    required_keys = ['uygulamali', 'teorik', 'uygulama', 'devamsizlik']
    for key in required_keys:
        if key not in data:
            return jsonify({'hata': f'{key} alanı eksik!'}), 400

    try:
        if data['uygulamali'] == 0:
            toplam_devamsizlik_hakki = (15 * data['teorik']) * 0.4
        elif data['teorik'] == 1:
            toplam_devamsizlik_hakki = 15 * (data['teorik'] * 0.4 + data['uygulama'] * 0.3)
        else:
            toplam_devamsizlik_hakki = (15 * data['uygulama']) * 0.3

        if data['devamsizlik'] > toplam_devamsizlik_hakki:
            durum = "Devamsızlıktan kaldı."
        else:
            durum = "Derse devamlı."

        return jsonify({'durum': durum})
    except Exception as e:
        return jsonify({'hata': str(e)}), 500


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
