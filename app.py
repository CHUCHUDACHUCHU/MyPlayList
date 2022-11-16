from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.rypuzfe.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbMyPlaylist


@app.route('/')
def home():
   return render_template('creates.html')

@app.route("/api/posts", methods=["POST"])
def web_comments_post():
    img_receive = request.form['img_give']
    title_receive = request.form['title_give']
    singer_receive = request.form['singer_give']
    comment_receive = request.form['comment_give']
    genre_receive = request.form['genre_give']
    date_receive = request.form['date_give']

    all_sings = list(db.sing.find({},{'_id':False}))
    count = len(all_sings) + 1

    doc = {
        'img': img_receive,
        'title': title_receive,
        'singer': singer_receive,
        'comment': comment_receive,
        'genre': genre_receive,
        'date': date_receive,
        'index': count

    }

    db.sing.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)