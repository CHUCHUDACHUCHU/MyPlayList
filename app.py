from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.rypuzfe.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbMyPlaylist

<<<<<<< HEAD

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

=======
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detail')
def detail():
    return render_template("detail.html")

@app.route("/api/posts", methods=['GET'])
def get_posts():
    posts = list(db.sing.find({}).sort("date", -1).limit(20))
    for post in posts:
        post["_id"] = str(post["_id"])
    return jsonify({"result": "success", "msg": "카드를 가져왔습니다.", "posts": posts})

#comment post
@app.route("/comment", methods=["POST"])
def comments_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name': name_receive,
        'comment': comment_receive
    }
    db.comments.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

#comment get
@app.route("/comment", methods=["GET"])
def comments_get():
    comment_list = list(db.comments.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

#sing get
@app.route("/sing", methods=["GET"])
def sing_get():
    sing_one = db.sing.find_one({'index':'1'}, {'_id': False})
    return jsonify({'sings': sing_one})
>>>>>>> develop

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)