from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.rypuzfe.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbMyPlaylist

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

#sing get_detail
@app.route("/detail/sing", methods=["GET"])
def sing_get():
    id = int(request.args('index'))
    sing_one = db.sing.find_one({'index':id}, {'_id': False})
    return jsonify({'sings': sing_one})

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

    # dklfjlskjdf