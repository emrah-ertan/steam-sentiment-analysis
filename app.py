from flask import Flask, render_template
import pandas as pd
from game_dict import id_to_name

app = Flask(__name__)

# CSV'leri orijinal haliyle yükle (sütun adlarını değiştirme)
vote_df = pd.read_csv("vote_rates.csv")  # Pretrained
vote_lstm_df = pd.read_csv("vote_rates_lstm.csv")  # LSTM (custom)

@app.route("/")
def home():
    # Pretrained toplamları
    pretrained_positive = vote_df.get('Positive', 0).sum() + vote_df.get('Very Positive', 0).sum()
    pretrained_negative = vote_df.get('Negative', 0).sum() + vote_df.get('Very Negative', 0).sum()

    # LSTM toplamları (sadece "positive" ve "negative" sütunları var)
    lstm_positive = vote_lstm_df.get('positive', 0).sum()
    lstm_negative = vote_lstm_df.get('negative', 0).sum()

    total_comments = vote_df.iloc[:, 1:].sum().sum()

    return render_template("index.html",
                           pretrained_positive=int(pretrained_positive),
                           pretrained_negative=int(pretrained_negative),
                           lstm_positive=int(lstm_positive),
                           lstm_negative=int(lstm_negative),
                           total_comments=int(total_comments),
                           games=id_to_name)

@app.route("/game/<int:appid>")
def game_detail(appid):
    # AppID'ye göre satır filtrele
    pretrained_row = vote_df[vote_df["AppID"] == appid].to_dict("records")
    lstm_row = vote_lstm_df[vote_lstm_df["AppID"] == appid].to_dict("records")

    return render_template("game_detail.html",
                           appid=appid,
                           game_name=id_to_name.get(appid, f"AppID {appid}").replace('_', ' ').title(),
                           pretrained=pretrained_row[0] if pretrained_row else None,
                           lstm=lstm_row[0] if lstm_row else None,
                           games=id_to_name)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
