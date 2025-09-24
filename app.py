from flask import Flask, render_template

app = Flask(__name__)

# ================== ROUTES CHO CLIENT ==================

@app.route('/')
def index():
    return render_template('Client/Trangchu.html')

@app.route('/dangnhap')
def dangnhap():
    return render_template('Client/Dangnhap.html')

@app.route('/dangky')
def dangky():
    return render_template('Client/Dangky.html')

@app.route('/danhmuc')
def danhmuc():
    return render_template('Client/Danhmuc.html')

@app.route('/sanpham')
def sanpham():
    return render_template('Client/Sanpham.html')

@app.route('/giohang')
def giohang():
    return render_template('Client/Giohang.html')

@app.route('/thanhtoan')
def thanhtoan():
    return render_template('Client/Thanhtoan.html')

@app.route('/donhang')
def donhang():
    return render_template('Client/Donhang.html')

@app.route("/profile")
def profile():
    user = {
        "email": "abc@gmail.com",
        "first_name": "ABC",
        "last_name": " ",
        "username": "abc123"
    }
    return render_template("Client/profile.html", user=user)
# ================== ROUTES CHO ADMIN ==================

@app.route('/admin')
def admin_index():
    return render_template('admin/Trangchu.html')

@app.route('/admin/sanpham')
def admin_sanpham():
    return render_template('admin/sanpham.html')

@app.route('/admin/donhang')
def admin_donhang():
    return render_template('admin/donhang.html')

@app.route('/admin/nguoidung')
def admin_nguoidung():
    return render_template('admin/nguoidung.html')

@app.route('/admin/thongke')
def admin_thongke():
    return render_template('admin/thongke.html')

# ================== MAIN ==================
if __name__ == '__main__':
    app.run(debug=True)
