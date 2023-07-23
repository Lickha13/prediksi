from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

app = Flask(__name__)

# Membaca data dari file CSV
data = pd.read_csv('./data/stemming_fix.csv')

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tweet = request.form['tweet']
        input_vector = vectorizer.transform([tweet])
        prediction = model.predict(input_vector)[0]
        return render_template({{url_for('prediksi')}}, tweet=tweet, prediction=prediction)
    return render_template('index_flask.html')

if __name__ == '__main__':
    app.run(debug=True)
