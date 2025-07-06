from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


@app.route('/')
def index():
    popular_df = pickle.load(open('popular.pkl', 'rb'))
    return render_template('index.html', book_name=popular_df['Book-Title'].tolist(),
                           book_author=popular_df['Book-Author'].tolist(),
                           book_image=popular_df['Image-URL-M'].tolist(),
                           book_rating=popular_df['avg_rating'].tolist(),
                           book_votes=popular_df['num_ratings'].tolist())

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend_w():
    user_input =request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)
    return render_template('recommend.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


