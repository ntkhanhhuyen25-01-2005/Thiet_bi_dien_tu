from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

# NOTE: This app uses in-memory data structures and Flask session for demo purposes.
# For production, replace with a real database and authentication.

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

# ================== SIMPLE IN-MEMORY DATA ==================

# Demo products
PRODUCTS = [
    {
        "id": 1,
        "name": "Laptop gaming MSI GP66 10UE - 206VN",
        "price": 40000000,
        "image": "https://laptop88.vn/media/news/0606_6251_msi_gp66_leopard_10ue_206vn-min.jpg",
        "category": "Laptop",
    },
    {
        "id": 2,
        "name": "Điện thoại IPhone 17 Pro",
        "price": 39500000,
        "image": "https://cdn.xtmobile.vn/vnt_upload/product/09_2025/thumbs/600_iPhone_17_Pro_cam_1_1.jpg",
        "category": "Điện thoại",
    },
    {
        "id": 3,
        "name": "Tai nghe Bluetooth",
        "price": 2900000,
        "image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcTgR7oRzKxxLQArNiYWhlv4GHQqb0eMrcpy5O8IH-WO6odxDoY6xGTqDNteTM3_SliO0AI73zLTnjVV_pJXOIT_Ik3ufCzSlgYpDrenkaOBE5RseUPZ7TmgsA",
        "category": "Âm thanh",
    },
    {
        "id": 4,
        "name": "Chuột Gaming",
        "price": 1490000,
        "image": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSnncyd6cCfeea2PvQslU-FgT1xii2iA_I10hh9q74Z_AoMVHoFz3oWi4A8UsD_D_eddOBhIhq6wuXhXsLtmgRvZiYLV_fO3FuQnoQPJgkfFvs-9LlAVBTY",
        "category": "Chuột & Bàn phím",
    },
    {
        "id": 5,
        "name": "Bàn phím cơ Filco Majestouch Convertible 3",
        "price": 4700000,
        "image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSC_t27kV1xIUe32sxTHoLpyX6ipIMocv33o_0fgHa4dA_yOikpAKeUPoMFCvj6dE-MMRlQ49MsNG-U1hFEyPu8DwTJFvwiL6hdd7eF_anzHU4DIIH1874rTZ8",
        "category": "Chuột & Bàn phím",
    },
]

# Simple user store (for demo only)
USERS = {
    # username: {username, email, first_name, last_name, password}
    "abc123": {
        "username": "abc123",
        "email": "abc@gmail.com",
        "first_name": "Nguyễn Văn",
        "last_name": "ABC",
        "password": "123456",
    },
    "user1": {
        "username": "user1",
        "email": "user1@example.com",
        "first_name": "Trần Thị",
        "last_name": "Bình",
        "password": "123456",
    },
    "customer1": {
        "username": "customer1",
        "email": "customer1@gmail.com",
        "first_name": "Lê Văn",
        "last_name": "Chi",
        "password": "123456",
    }
}

# Admin store (for demo only)
ADMINS = {
    # username: {username, email, first_name, last_name, password, role, created_at}
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Nguyễn",
        "last_name": "Admin",
        "password": "admin123",
        "role": "super_admin",
        "created_at": "2025-01-01 00:00:00"
    }
}


def get_cart():
    """Return cart from session. Cart format: {product_id: quantity}.
    Ensures a cart dict exists in session.
    """
    cart = session.get("cart")
    if cart is None:
        cart = {}
        session["cart"] = cart
    return cart


def cart_items_with_totals():
    """Builds a list of items with product info and calculates totals."""
    cart = get_cart()
    items = []
    subtotal = 0
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = next((p for p in PRODUCTS if p["id"] == pid), None)
        if not product:
            continue
        line_total = product["price"] * int(qty)
        subtotal += line_total
        items.append({
            "product": product,
            "quantity": int(qty),
            "line_total": line_total,
        })
    shipping = 30000 if subtotal > 0 else 0
    grand_total = subtotal + shipping
    return items, subtotal, shipping, grand_total


def current_user():
    """Get current logged-in user dict or None."""
    username = session.get("username")
    if not username:
        return None
    return USERS.get(username)

# ================== ROUTES CHO CLIENT ==================

@app.route('/')
def index():
    return render_template('Client/Trangchu.html')

@app.route('/dangnhap', methods=["GET", "POST"])
def dangnhap():
    # Basic demo login: match username + password in USERS
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = USERS.get(username)
        if user and user.get("password") == password:
            session["username"] = username
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('index'))
        flash("Sai thông tin đăng nhập", "danger")
    return render_template('Client/Dangnhap.html')

@app.route('/dangky', methods=["GET", "POST"])
def dangky():
    # Basic demo register: create user if username not taken
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password1 = request.form.get("password1", "")
        password2 = request.form.get("password2", "")
        if not username or not email or not password1:
            flash("Vui lòng điền đầy đủ thông tin", "warning")
        elif password1 != password2:
            flash("Mật khẩu xác nhận không khớp", "danger")
        elif username in USERS:
            flash("Tên đăng nhập đã tồn tại", "danger")
        else:
            USERS[username] = {
                "username": username,
                "email": email,
                "first_name": username,
                "last_name": "",
                "password": password1,
            }
            flash("Đăng ký thành công, vui lòng đăng nhập", "success")
            return redirect(url_for('dangnhap'))
    return render_template('Client/Dangky.html')

@app.route('/dangxuat')
def dangxuat():
    session.pop("username", None)
    flash("Đã đăng xuất", "info")
    return redirect(url_for('index'))

@app.route('/danhmuc')
def danhmuc():
    # Could pass categories/products for real app; static demo UI for now
    return render_template('Client/Danhmuc.html')

@app.route('/sanpham')
def sanpham():
    # Pass demo products for listing
    return render_template('Client/Sanpham.html', products=PRODUCTS)

@app.route('/giohang')
def giohang():
    items, subtotal, shipping, grand_total = cart_items_with_totals()
    user = current_user()
    return render_template('Client/Giohang.html', items=items, subtotal=subtotal, shipping=shipping, grand_total=grand_total, user=user)

@app.route('/thanhtoan', methods=["GET", "POST"])
def thanhtoan():
    # Kiểm tra đăng nhập bắt buộc
    user = current_user()
    if not user:
        flash("Vui lòng đăng nhập để thanh toán", "warning")
        return redirect(url_for('dangnhap'))
    
    # GET: show checkout with current cart
    items, subtotal, shipping, grand_total = cart_items_with_totals()
    if request.method == "GET":
        return render_template('Client/Thanhtoan.html', items=items, subtotal=subtotal, shipping=shipping, grand_total=grand_total, user=user)

    # POST: create an order, then clear cart
    if not items:
        flash("Giỏ hàng trống", "warning")
        return redirect(url_for('giohang'))

    order = {
        "code": f"DH{datetime.now().strftime('%y%m%d%H%M%S')}",
        "created_at": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "items": [
            {
                "product_id": it["product"]["id"],
                "name": it["product"]["name"],
                "price": it["product"]["price"],
                "quantity": it["quantity"],
                "line_total": it["line_total"],
            }
            for it in items
        ],
        "subtotal": subtotal,
        "shipping": shipping,
        "total": grand_total,
        "status": "Đang xử lý",
        "customer": {
            "full_name": request.form.get("full_name", "") or f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
            "phone": request.form.get("phone", ""),
            "email": request.form.get("email", "") or user.get("email", ""),
            "address": request.form.get("address", ""),
            "payment": request.form.get("payment", "cod"),
        },
    }

    username = session.get("username", "guest")
    orders = session.get("orders", {})
    user_orders = orders.get(username, [])
    user_orders.append(order)
    orders[username] = user_orders
    session["orders"] = orders

    # clear cart
    session["cart"] = {}
    flash("Đặt hàng thành công!", "success")
    return redirect(url_for('donhang'))

@app.route('/donhang')
def donhang():
    username = session.get("username", "guest")
    orders = session.get("orders", {}).get(username, [])
    return render_template('Client/Donhang.html', orders=orders)

@app.route("/profile")
def profile():
    user = current_user() or {
        "email": "guest@example.com",
        "first_name": "Guest",
        "last_name": "",
        "username": "guest",
    }
    return render_template("Client/profile.html", user=user)

# -------- CART OPERATIONS --------

@app.route('/cart/add', methods=["POST"])
def cart_add():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 1))
    if not product_id:
        return redirect(url_for('sanpham'))
    # ensure product exists
    pid = int(product_id)
    if not any(p["id"] == pid for p in PRODUCTS):
        flash("Sản phẩm không tồn tại", "danger")
        return redirect(url_for('sanpham'))
    cart = get_cart()
    cart[str(pid)] = cart.get(str(pid), 0) + max(1, quantity)
    session["cart"] = cart
    flash("Đã thêm vào giỏ hàng", "success")
    return redirect(url_for('giohang'))

@app.route('/cart/update', methods=["POST"])
def cart_update():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 1))
    cart = get_cart()
    if product_id in cart:
        if quantity <= 0:
            cart.pop(product_id)
        else:
            cart[product_id] = quantity
        session["cart"] = cart
        flash("Đã cập nhật giỏ hàng", "info")
    return redirect(url_for('giohang'))

@app.route('/cart/remove', methods=["POST"])
def cart_remove():
    product_id = request.form.get("product_id")
    cart = get_cart()
    if product_id in cart:
        cart.pop(product_id)
        session["cart"] = cart
        flash("Đã xóa sản phẩm", "warning")
    return redirect(url_for('giohang'))
# ================== ROUTES CHO ADMIN ==================

def admin_required(f):
    """Decorator để kiểm tra đăng nhập admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Vui lòng đăng nhập với tài khoản admin', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    """Trang đăng ký admin"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not first_name or not password:
            flash('Vui lòng điền đầy đủ thông tin', 'warning')
        elif password != confirm_password:
            flash('Mật khẩu xác nhận không khớp', 'danger')
        elif username in ADMINS:
            flash('Tên đăng nhập admin đã tồn tại', 'danger')
        elif len(password) < 6:
            flash('Mật khẩu phải có ít nhất 6 ký tự', 'danger')
        else:
            # Tạo tài khoản admin mới
            ADMINS[username] = {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "role": "admin",
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            flash('Đăng ký admin thành công! Vui lòng đăng nhập', 'success')
            return redirect(url_for('admin_login'))
    
    return render_template('admin/register.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Trang đăng nhập admin"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Kiểm tra thông tin đăng nhập admin
        admin = ADMINS.get(username)
        if admin and admin.get('password') == password:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['admin_role'] = admin.get('role', 'admin')
            flash('Đăng nhập admin thành công!', 'success')
            return redirect(url_for('admin_index'))
        else:
            flash('Sai thông tin đăng nhập admin', 'danger')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Đăng xuất admin"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Đã đăng xuất admin', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_index():
    return render_template('admin/Trangchu.html')

@app.route('/admin/sanpham')
def admin_sanpham():
    return render_template('admin/sanpham.html', products=PRODUCTS)

@app.route('/admin/donhang')
def admin_donhang():
    # Lấy tất cả đơn hàng từ session
    all_orders = []
    orders_data = session.get("orders", {})
    for username, user_orders in orders_data.items():
        for order in user_orders:
            order_copy = order.copy()
            order_copy['username'] = username
            all_orders.append(order_copy)
    return render_template('admin/donhang.html', orders=all_orders)

@app.route('/admin/nguoidung')
def admin_nguoidung():
    # Hiển thị tất cả người dùng mặc định
    users = [(username, user) for username, user in USERS.items()]
    return render_template('admin/nguoidung.html', users=users)

@app.route('/admin/quanly-admin')
def admin_quanly_admin():
    """Quản lý tài khoản admin"""
    admins = [(username, admin) for username, admin in ADMINS.items()]
    return render_template('admin/quanly_admin.html', admins=admins)

@app.route('/admin/thongke')
def admin_thongke():
    return render_template('admin/thongke.html')

# ================== ADMIN SEARCH ROUTES ==================

@app.route('/admin/search/donhang')
def admin_search_donhang():
    """Tìm kiếm đơn hàng theo mã đơn hàng, tên khách hàng, trạng thái"""
    search_term = request.args.get('q', '').strip().lower()
    search_type = request.args.get('type', 'all')  # all, code, customer, status
    
    # Lấy tất cả đơn hàng từ session
    all_orders = []
    orders_data = session.get("orders", {})
    for username, user_orders in orders_data.items():
        for order in user_orders:
            order_copy = order.copy()
            order_copy['username'] = username
            all_orders.append(order_copy)
    
    filtered_orders = []
    
    if search_term:
        for order in all_orders:
            # Tìm kiếm theo mã đơn hàng
            if search_type in ['all', 'code']:
                if search_term in order.get('code', '').lower():
                    filtered_orders.append(order)
                    continue
            
            # Tìm kiếm theo tên khách hàng
            if search_type in ['all', 'customer']:
                customer_name = order.get('customer', {}).get('full_name', '').lower()
                if search_term in customer_name:
                    filtered_orders.append(order)
                    continue
            
            # Tìm kiếm theo trạng thái
            if search_type in ['all', 'status']:
                if search_term in order.get('status', '').lower():
                    filtered_orders.append(order)
                    continue
    else:
        filtered_orders = all_orders
    
    return render_template('admin/donhang.html', orders=filtered_orders, search_term=search_term, search_type=search_type)

@app.route('/admin/search/nguoidung')
def admin_search_nguoidung():
    """Tìm kiếm người dùng theo username, email, tên"""
    search_term = request.args.get('q', '').strip().lower()
    search_type = request.args.get('type', 'all')  # all, username, email, name
    
    filtered_users = []
    
    if search_term:
        for username, user in USERS.items():
            # Tìm kiếm theo username
            if search_type in ['all', 'username']:
                if search_term in username.lower():
                    filtered_users.append((username, user))
                    continue
            
            # Tìm kiếm theo email
            if search_type in ['all', 'email']:
                email = user.get('email', '').lower()
                if search_term in email:
                    filtered_users.append((username, user))
                    continue
            
            # Tìm kiếm theo tên
            if search_type in ['all', 'name']:
                first_name = user.get('first_name', '').lower()
                last_name = user.get('last_name', '').lower()
                full_name = f"{first_name} {last_name}".strip().lower()
                if search_term in full_name:
                    filtered_users.append((username, user))
                    continue
    else:
        filtered_users = [(username, user) for username, user in USERS.items()]
    
    return render_template('admin/nguoidung.html', users=filtered_users, search_term=search_term, search_type=search_type)

@app.route('/admin/search/khachhang')
def admin_search_khachhang():
    """Tìm kiếm khách hàng theo thông tin đặt hàng (tên, email, phone, địa chỉ)"""
    search_term = request.args.get('q', '').strip().lower()
    search_type = request.args.get('type', 'all')  # all, name, email, phone, address
    
    # Lấy tất cả khách hàng từ đơn hàng
    customers = {}
    orders_data = session.get("orders", {})
    
    for username, user_orders in orders_data.items():
        for order in user_orders:
            customer_info = order.get('customer', {})
            # Tạo key duy nhất cho khách hàng (email hoặc phone)
            customer_key = customer_info.get('email') or customer_info.get('phone') or f"user_{username}"
            
            if customer_key not in customers:
                customers[customer_key] = {
                    'full_name': customer_info.get('full_name', ''),
                    'email': customer_info.get('email', ''),
                    'phone': customer_info.get('phone', ''),
                    'address': customer_info.get('address', ''),
                    'total_orders': 0,
                    'total_spent': 0,
                    'username': username
                }
            
            customers[customer_key]['total_orders'] += 1
            customers[customer_key]['total_spent'] += order.get('total', 0)
    
    filtered_customers = []
    
    if search_term:
        for customer_key, customer in customers.items():
            # Tìm kiếm theo tên
            if search_type in ['all', 'name']:
                if search_term in customer.get('full_name', '').lower():
                    filtered_customers.append((customer_key, customer))
                    continue
            
            # Tìm kiếm theo email
            if search_type in ['all', 'email']:
                if search_term in customer.get('email', '').lower():
                    filtered_customers.append((customer_key, customer))
                    continue
            
            # Tìm kiếm theo số điện thoại
            if search_type in ['all', 'phone']:
                if search_term in customer.get('phone', '').lower():
                    filtered_customers.append((customer_key, customer))
                    continue
            
            # Tìm kiếm theo địa chỉ
            if search_type in ['all', 'address']:
                if search_term in customer.get('address', '').lower():
                    filtered_customers.append((customer_key, customer))
                    continue
    else:
        filtered_customers = [(key, customer) for key, customer in customers.items()]
    
    return render_template('admin/nguoidung.html', customers=filtered_customers, search_term=search_term, search_type=search_type, is_customer_search=True)

@app.route('/admin/search/sanpham')
def admin_search_sanpham():
    """Tìm kiếm sản phẩm theo tên, danh mục"""
    search_term = request.args.get('q', '').strip().lower()
    search_type = request.args.get('type', 'all')  # all, name, category
    
    filtered_products = []
    
    if search_term:
        for product in PRODUCTS:
            # Tìm kiếm theo tên sản phẩm
            if search_type in ['all', 'name']:
                if search_term in product.get('name', '').lower():
                    filtered_products.append(product)
                    continue
            
            # Tìm kiếm theo danh mục
            if search_type in ['all', 'category']:
                if search_term in product.get('category', '').lower():
                    filtered_products.append(product)
                    continue
    else:
        filtered_products = PRODUCTS
    
    return render_template('admin/sanpham.html', products=filtered_products, search_term=search_term, search_type=search_type)

@app.route('/admin/search/admin')
def admin_search_admin():
    """Tìm kiếm admin theo tên, username, email"""
    search_term = request.args.get('q', '').strip().lower()
    search_type = request.args.get('type', 'all')  # all, name, username, email
    
    filtered_admins = []
    
    if search_term:
        for username, admin in ADMINS.items():
            # Tìm kiếm theo username
            if search_type in ['all', 'username']:
                if search_term in username.lower():
                    filtered_admins.append((username, admin))
                    continue
            
            # Tìm kiếm theo email
            if search_type in ['all', 'email']:
                email = admin.get('email', '').lower()
                if search_term in email:
                    filtered_admins.append((username, admin))
                    continue
            
            # Tìm kiếm theo tên
            if search_type in ['all', 'name']:
                first_name = admin.get('first_name', '').lower()
                last_name = admin.get('last_name', '').lower()
                full_name = f"{first_name} {last_name}".strip().lower()
                if search_term in full_name:
                    filtered_admins.append((username, admin))
                    continue
    else:
        filtered_admins = [(username, admin) for username, admin in ADMINS.items()]
    
    return render_template('admin/quanly_admin.html', admins=filtered_admins, search_term=search_term, search_type=search_type)

# ================== MAIN ==================
if __name__ == '__main__':
    app.run(debug=True)
