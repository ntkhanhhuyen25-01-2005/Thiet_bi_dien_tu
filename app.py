from flask import Flask, render_template

app = Flask(__name__)

# Trang chủ
@app.route('/')
def index():
    return render_template('Trangchu.html')

# Đăng nhập
@app.route('/dangnhap')
def dangnhap():
    return render_template('Dangnhap.html')

# Đăng ký
@app.route('/dangki')
def dangki():
    return render_template('Dangki.html')

# Danh mục
@app.route('/danhmuc')
def danhmuc():
    return render_template('Danhmuc.html')

# Đơn hàng
@app.route('/donhang')
def donhang():
    return render_template('Donhang.html')

# Hồ sơ
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Sản phẩm
@app.route('/sanpham')
def sanpham():
    return render_template('Sanpham.html')

if __name__ == '__main__':
    app.run(debug=True)
