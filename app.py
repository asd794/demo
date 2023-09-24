from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://asd123753951:q9BsyWYDLiZXjCYh@cluster0.azvuikv.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
from flask import *
from flask_bcrypt import Bcrypt #匯入flask-bcrypt 套件
bcrypt=Bcrypt() # 建立Bcrypt實體並指定給變數bcrypt

# doec

app=Flask(
    __name__,
    static_folder="public",
    # static_url_path="/"
)
app.secret_key="secret key for flask test"

# 登入首頁
@app.route("/")
def index():
    return render_template("login.html")

# 註冊頁面
@app.route("/register")
def register():
    return render_template("register.html")

# 會員頁面
@app.route("/member")
def member():
    if "account" in session: # 判斷session有無資料，沒有就導向到/
        return render_template("member.html",account=session['account'],email=session['email'])
    else:
        return redirect("/")

# 錯誤頁面 /error?msg=錯誤訊息
@app.route("/error")
def error():
    message=request.args.get("msg","發生錯誤請聯繫客服")
    return render_template("error.html",message=message)

# 處理會員註冊
@app.route("/signup" ,methods=["POST"])
def signup():
    # 從前端接收資料
    email=request.form["email"]
    account=request.form["account"]
    password=request.form["password"]
    #
    if account=="" or email=="" or password=="":
        return redirect("/error?msg=三個欄位都是必填，請重新註冊")
    # 根據接收的資料與資料庫互動
    db=client.myweb
    collection=db.users
    hashed_password=bcrypt.generate_password_hash(password=password) # 雜湊函數加密密碼
    if collection.find_one({"email":email})==None: # 檢查email是否空值None,是空值就新增到資料庫
        collection.insert_one({
            "email":email,
            "account":account,
            "password":hashed_password
        })
        return redirect("/")
    else: # 不是空值傳Query String到error.html報錯
        return redirect("/error?msg=信箱已經被註冊")
        # return render_template("error.html",msg="信箱已經被註冊了")

# 處理會員登入 MongoDB
@app.route("/signin" ,methods=["post"])
def signin():
    account=request.form["account"] # 前端form傳入的帳號
    passowrd=request.form["password"] # 前端form傳入的密碼
    db=client.myweb
    collection=db.users
    db_check=collection.find_one({"account":account})  # db查詢結果放入db_check
    print(account) # 確認account
    print(db_check) # 確認db查詢是否正確(查無結果會是None)
    # print(db_check['email']) # 確認db查詢是否正確
    if db_check != None:
        check_password=bcrypt.check_password_hash(db_check['password'],passowrd) # 雜湊密碼比對
        if check_password ==True: # 如果比對為正確(true)將email和account存入seesion，否則回傳帳密輸入錯誤
            session['email']=db_check['email']
            session['account']=account
            print(type(session['email']))
            return redirect("/member")
            # return session['email']+session['account']
        else:
            return redirect("/error?msg=帳密輸入錯誤")
    else:
        return redirect("/error?msg=帳密輸入錯誤")
    
# 會員登出 清除session
@app.route("/signout")
def signout():
    del session["email"]
    del session["account"]
    session.clear()
    print(session) # 確認session是否清除
    return redirect("/")

# 變更密碼
@app.route("/change")
def change():
    return render_template("change.html")

# 處理變更密碼 原本是處理"會員註冊"
@app.route("/changed" ,methods=["POST"])
def changed():
    # 從前端form接收資料
    old_password=request.form["old_password"]
    new_password=request.form["new_password"]

    if old_password=="" or new_password=="": # 處理form空值
        return redirect("/error_change?msg=舊、新密碼欄位為必填")
    
    # 根據接收的資料與資料庫互動
    db=client.myweb
    collection=db.users

    db_check=collection.find_one({"account":session['account']})  # db查詢結果放入db_check
    check_password=bcrypt.check_password_hash(db_check['password'],old_password) # 雜湊密碼比對
    if check_password ==True: # 雜湊密碼比對如果正確=True
        hashed_password=bcrypt.generate_password_hash(password=new_password) # 將新密碼加密，並更新db
        collection.update_one({
            "email":session['email']
        },{
            "$set":{
                "password":hashed_password # 如果無password欄位，會新增一個新的欄位
            }
        })
        session.clear() # 清除seesion
        print(session) # 確認session是否清除
        return redirect("/change_complete")
    else:
        return redirect("/error_change?msg=舊密碼輸入錯誤")
    
# 變更密碼錯誤頁面 /error_change?msg=錯誤訊息
@app.route("/error_change")
def error_change():
    message=request.args.get("msg","發生錯誤請聯繫客服")
    return render_template("error_change.html",message=message)

@app.route("/change_complete")
def error_complete():
    return render_template("change_complete.html")


if __name__=='__main__':
    app.run(host='0.0.0.0',port=80)
