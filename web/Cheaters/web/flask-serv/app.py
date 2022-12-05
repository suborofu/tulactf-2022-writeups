import shutil
from flask import Flask,render_template,request,make_response,redirect
import jwt
from werkzeug.utils import secure_filename
from functools import wraps
import uuid
import os
from tester import checkForCheaters, extractWorkbook, getScore, core
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024

SECRET_KEY = os.getenv('SECRET_KEY')
FLAG = os.getenv('FLAG')

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'token' in request.cookies:
            token = request.cookies.get('token')
        if not token:
            response = make_response(redirect('/login'))
            response.set_cookie('token', "",expires=0)
            return response
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user']
        except:
            response = make_response(redirect('/login'))
            response.set_cookie('token', "",expires=0)
            return response
        return f(*args, **kwargs)
    return decorator


@app.route('/',methods=['GET'])
@token_required
def home():
    return render_template('index.html')

@app.route('/flag',methods=['GET'])
@token_required
def flag():
    token = request.cookies.get('token')
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if data['admin']:
        return FLAG
    else:
        return "I don't think you are an admin? Are you?"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template('login.html')
    else:
        if request.form['username'] and request.form['password']:
            flag=False
            token=jwt.encode({
                'user':request.form['username'],'admin':flag
            }, SECRET_KEY)
            response = make_response(redirect('/'))
            response.set_cookie('token', token)
            return response
        else:
            return make_response('Unable to verify',403,{'WWW-Authenticate':'Basic realm: "Authentication failed"'})

@app.route('/tester',methods=['POST'])
@token_required
def tester():
    if request.method == "POST":
        f = request.files["file"]
        tmpFolder = "./uploads/" + str(uuid.uuid4())
        os.mkdir(tmpFolder)
        filename = tmpFolder + "/" + secure_filename(f.filename)
        f.save(filename)
        try:
            extractWorkbook(filename, tmpFolder)
            corePath = tmpFolder + "/" + core
            cheater = checkForCheaters(corePath)
            score=getScore(filename,testAnswers)
            print(cheater,score)
        except Exception:
            return render_template("error.html")
        finally:
            shutil.rmtree(tmpFolder)
        if cheater[0]:
            theCheater=cheater[1][-1]
            return "Dear teacher! Student {} has cheated!".format(theCheater)
        return 'The score is {}/{}!'.format(score,maxScore)


testAnswers=[]
maxScore=0
if __name__=="__main__":
    f = open('answers.txt', 'r')
    testAnswers = [line.rstrip() for line in f]
    maxScore=len(testAnswers)
    f.close()
    app.run(host="0.0.0.0")
