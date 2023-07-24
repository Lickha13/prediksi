from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

app = Flask(__name__)

# Membaca data dari file CSV
data = pd.read_csv('./static/data/stemming_fix.csv')

# Memisahkan teks dan label
tweets = data['stemming']
labels = data['label']

# Menggabungkan teks dan label ke dalam satu dataframe
df = pd.DataFrame({'tweets': tweets, 'labels': labels})

# Menghapus baris dengan missing values
df = df.dropna()

# Augmentasi data
augmented_df = df.copy()

# Melakukan augmentasi dengan menggandakan data negatif, netral, dan positif
augmented_df = pd.concat([augmented_df, augmented_df[augmented_df['labels'] != 'positive']])
augmented_df = pd.concat([augmented_df, augmented_df[augmented_df['labels'] != 'neutral']])

# Ubah teks menjadi vektor fitur menggunakan CountVectorizer
vectorizer = CountVectorizer(binary=True)
X = vectorizer.fit_transform(augmented_df['tweets'])
y = augmented_df['labels']

# Split data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Melatih model dengan metode Multinomial Naive Bayes
model = MultinomialNB()
model.fit(X_train, y_train)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/word-clouds')
def word_clouds():
    return render_template('word-clouds.html')

@app.route('/word-data')
def word_data():
    return render_template('word-data.html')

def predict_sentiment(tweet):
    input_vector = vectorizer.transform([tweet])
    prediction = model.predict(input_vector)[0]
    return prediction

@app.route('/prediksi', methods=['GET', 'POST'])
def prediksi():
    if request.method == 'POST':
        tweet = request.form['tweet']
        prediction = predict_sentiment(tweet)  # Ganti 'prediksi' menjadi 'predict_sentiment'
        return render_template('prediksi_result.html', tweet=tweet, prediction=prediction)
    return render_template('prediksi.html')

if __name__ == '__main__':
    app.run(debug=True)
