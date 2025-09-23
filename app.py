# from flask import Flask, render_template, flash

# app = Flask(__name__)
# app.secret_key = "mysecret" 

# @app.route("/")
# def home():
#     return render_template("Trangchu.html", title="Trang chủ")

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Trangchu.html")

@app.route("/sanpham")
def sanpham():
    return render_template("Sanpham.html")

@app.route("/dangnhap")
def dangnhap():
    return render_template("Dangnhap.html")

if __name__ == "__main__":
    app.run(debug=True)
