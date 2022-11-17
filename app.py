from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import certifi

app = Flask(__name__)

# client = MongoClient('mongodb+srv://test:sparta@cluster0.rypuzfe.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbMyPlaylist

ca=certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.rypuzfe.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbMyPlaylist

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

@app.route("/api/posts", methods=["POST"])
def web_comments_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})  # payload에서 아이디를 가져와서 실제 유저의 정보를 읽어온다.

        img_receive = request.form['img_give']
        title_receive = request.form['title_give']
        singer_receive = request.form['singer_give']
        comment_receive = request.form['comment_give']
        genre_receive = request.form['genre_give']
        date_receive = request.form['date_give']

        all_sings = list(db.sing.find({}, {'_id': False}))

        count = len(all_sings) + 1

        doc = {
            'user_id': payload['id'],
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
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})  # payload에서 아이디를 가져와서 실제 유저의 정보를 읽어온다.
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/create')
def create():
    return render_template('creates.html')

@app.route('/user/<user_id>')
def user(user_id):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (user_id == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"user_id": user_id}, {"_id": False})
        user_sings = list(db.sing.find({"user_id": user_id}).sort("date", -1).limit(20))
        return render_template('user.html', user_info=user_info, user_sings=user_sings, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 로그인 및 회원가입 API
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    user_id_receive = request.form['user_id_give']
    password_receive = request.form['password_give']
    # 패스워드를 sha256 방법(=단방향 암호화, 풀어볼 수 없음)으로 암호화해서 저장한다.
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'user_id': user_id_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': user_id_receive,
            # 'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
            'exp': datetime.datetime.utcnow() + timedelta(seconds=60 * 5)  # 로그인 2분 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    user_id_receive = request.form['user_id_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "user_id": user_id_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": user_id_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    user_id_receive = request.form['user_id_give']
    exists = bool(db.users.find_one({"user_id": user_id_receive}))
    return jsonify({'result': 'success', 'exists': exists})



@app.route("/api/posts", methods=['GET'])
def get_posts():
    posts = list(db.sing.find({}).sort("date", -1).limit(20))
    for post in posts:
        post["_id"] = str(post["_id"])
    return jsonify({"result": "success", "msg": "카드를 가져왔습니다.", "posts": posts})

# comment post
@app.route("/detail/comment", methods=["POST"])
def comments_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    # one_card_receive = request.form['one_card_give']
    card_id_receive = request.form['card_id_give']

    doc = {
        # 'one_card': one_card_receive,
        'name': name_receive,
        'comment': comment_receive,
        'card_id': card_id_receive
    }
    db.comments.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

# comment get
@app.route("/detail/comment", methods=["GET"])
def comments_get():
    card_index = request.args.get('card')
    comment_list = list(db.comments.find({'card_id':card_index}, {'_id': False}))
    return jsonify({'comments': comment_list})

@app.route("/detail/")
def get_cards():
    one_card = request.args.get('card')
    print(one_card)
    cards = db.sing.find_one({'index': int(one_card)}, {'_id': False})

    if cards:
        index = cards['index']
        img = cards['img']
        title = cards['title']
        singer = cards['singer']
        genre = cards['genre']
        comment = cards['comment']
    return render_template("detail.html", img=img, title=title, singer=singer, genre=genre, comment=comment, index=index)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
