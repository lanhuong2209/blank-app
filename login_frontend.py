from nicegui import ui
from login_backend import User , UserDatabase, user_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from typing import List, Dict

def create_intro_page():
    nav_items: List[Dict] = [
        {"name": "Home", "url": "/", "icon": "home"},
        {"name": "Explore", "url": "/explore", "icon": "explore"},
        {"name": "Help", "url": "/help", "icon": "help"}
    ]

    features = [
        {
            "title": "Effective Learning",
            "description": "The SKT legacy has been reignited and T1'll be your 2023 World Champions",
            "icon": "school"
        },
        {
            "title": "Create Activities",
            "description": "They say Busan was Church of Chovy, but what's God to 5 non believers",
            "icon": "groups"
        },
        {
            "title": "Fun Flashcards",
            "description": "It is not LPL versus LCK, it's T1 versus the LPL and I like those odds",
            "icon": "library_books"
        }
    ]

    # Set page background and styles
    ui.query('body').style(
        '''
        background: linear-gradient(135deg, #f0f4ff, #e5e7ff);
        margin: 0;
        padding: 0;
        min-height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        '''
    )

    # Header
    with ui.header().classes('w-full').style('background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px);'):
        with ui.row().classes('w-full max-w-7xl mx-auto justify-between items-center p-4'):
            # Logo section
            with ui.row().classes('items-center gap-2'):
                ui.icon('auto_stories').classes('text-3xl text-indigo-600')
                ui.label('MYMY').classes('text-2xl font-bold text-indigo-600')
            
            # Navigation
            with ui.row().classes('space-x-6'):
                for item in nav_items:
                    with ui.row().classes('items-center gap-2 cursor-pointer hover:text-indigo-600 transition-colors duration-200 '):
                        ui.icon(item['icon']).classes('text-indigo-600')
                        ui.link(item['name'], item['url']).classes(
                            'text-gray-700 hover:text-indigo-600 transition-colors duration-200'
                        )
            

# Các hàm tiện ích (utility functions)
def create_centered_container():
    # Tạo container căn giữa màn hình
    return ui.element('div').style('position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; max-width: 400px;')

def redirect(url: str):
    # Chuyển hướng trang
    ui.run_javascript(f'window.location.href = "{url}"')

def get_date_limits():
    # Lấy giới hạn ngày cho input date
    today = datetime.now()
    max_date = today.strftime('%Y-%m-%d')  # Ngày hiện tại
    min_date = (today - timedelta(days=365 * 100)).strftime('%Y-%m-%d')  # 100 năm trước
    return min_date, max_date

# Trang đăng nhập (/)
@ui.page('/')
def login_page():
    #ui.query('body')
    create_intro_page()
        # Tạo giao diện đăng nhập
    with create_centered_container():
            with ui.card().classes('w-full p-8 rounded-lg shadow-lg'):
            # Tiêu đề
                ui.label('Log in').classes('text-3xl font-bold text-center mb-6')
            
                with ui.column().classes('w-full gap-4'):
                # Form đăng nhập
                    with ui.row().classes('w-full items-center gap-2'):
                        username_input = ui.input('Your username...').props('rounded').props('outlined required').classes('w-full')    
                    with ui.row().classes('w-full items-center gap-2'):
                        password_input = ui.input('Enter password...').props('rounded').props('outlined required type=password').classes('w-full')
                # Link quên mật khẩu
                    ui.link('Forgot password?', '/forgot-password').classes('text-blue-500 text-center hover:text-blue-700 cursor-pointer no-underline')
                
                # Xử lý đăng nhập
                    async def handle_login():
                        success, message = user_db.authenticate_user(username_input.value, password_input.value)
                        ui.notify(message, color='positive' if success else 'negative')
                        if success:
                            user_db.set_user_status_on_by_username(username_input.value)
                            redirect('/home')

                # Nút đăng nhập
                    ui.button('LOG IN', on_click=handle_login).props('rounded').classes('w-full bg-indigo hover:bg-indigo-600 text-white font-semibold py-2 rounded-lg shadow-md')
                
                # Phần link đăng ký
                    with ui.row().classes('w-full justify-center items-center gap-2 mt-4'):
                        ui.label('Do not have account yet?').classes('text-center')
                        ui.link('Create account', '/register').classes('text-blue-500 hover:text-blue-700 cursor-pointer no-underline')
# Trang đăng ký (/register)
@ui.page('/register')
def register_page():
    #ui.query('body').style('margin: 0; padding: 0; background: linear-gradient(135deg, #f0f4ff, #e5e7ff);')
    create_intro_page()
    # Lấy giới hạn ngày
    min_date, max_date = get_date_limits()
    
    # Tạo giao diện đăng ký
    with create_centered_container():

        with ui.card().classes('w-full p-8 rounded-lg shadow-lg'):
            # Tiêu đề
            ui.label('Sign up').classes('text-3xl front-bold text-center mb-6')
            
            with ui.column().classes('w-full gap-4') as form_container:
                # Form đăng ký
                username_input = ui.input('Login name*').props('rounded').props('outlined required').classes('w-full')
                fullname_input = ui.input('User name*').props('rounded').props('outlined required').classes('w-full')
                email_input = ui.input('Email*').props('rounded').props('outlined required type=email').classes('w-full')
                birthdate_input = ui.input('Date of birth*').props('rounded').props(f'outlined required type=date min="{min_date}" max="{max_date}"').classes('w-full')
                password_input = ui.input('Password*').props('rounded').props('outlined required type=password').classes('w-full')
                confirm_password_input = ui.input('Confirm password*').props('rounded').props('outlined required type=password').classes('w-full')
                
                # Thông báo
                ui.label('* Please enter correctly and remember the information to retrieve your password when necessary').classes('text-red-500 text-sm mb-2')

                # Nút đăng ký
                register_button = ui.button('SIGN UP').props('rounded').classes('w-full bg-indigo hover:bg-indigo text-white font-semibold py-2 rounded-lg shadow-md')
                
                # Xử lý đăng ký
                async def validate_and_register():

                    #Check email,username
                    if user_db.find_user_by_email(email_input.value):
                        ui.notify('Existed email', color = 'negative')
                    if not '@' in email_input.value:
                        ui.notify('Invalid email!', color='negative')
                        return
                    if user_db.find_user_by_username(username_input.value):
                        ui.notify('Existed username', color = 'negative')

                    # Kiểm tra ngày sinh
                    if not birthdate_input.value:
                        ui.notify('Please enter your date of birth!', color='negative')
                        return
                    
                    # Kiểm tra định dạng ngày
                    input_date = datetime.strptime(birthdate_input.value, '%Y-%m-%d')
                    min_date_obj = datetime.strptime(min_date, '%Y-%m-%d')
                    max_date_obj = datetime.strptime(max_date, '%Y-%m-%d')

                    # Validate ngày sinh
                    if input_date < min_date_obj or input_date > max_date_obj:
                        birthdate_input.value = min_date
                        ui.notify('Invalid date of birth', color='negative')
                        return
                    
                    # Kiểm tra mật khẩu
                    # Yêu cầu độ mạnh của mật khẩu
                    if len(password_input.value) < 8 or not any(char.isupper() for char in password_input.value) or not any(char.isdigit() for char in password_input.value):
                        ui.notify('Password must be at least 8 characters long, contain at least 1 uppercase letter, 1 lowercase letter, 1 number.', color='negative')
                        return
                    if password_input.value != confirm_password_input.value:
                        ui.notify('Password does not match!', color='negative')
                        return
                    
                    # Tạo user mới
                    new_user = User(
                        username=username_input.value,
                        fullname=fullname_input.value,
                        email=email_input.value,
                        birthdate=birthdate_input.value,
                        password=password_input.value
                    )
                    
                    # Thêm user vào database
                    success, message = user_db.add_user(new_user)
                    if success:
                        print(f"User registered: {new_user.__dict__}")

                    ui.notify(message, color='positive' if success else 'negative')
                    if success:
                        register_button.visible = False
                        ui.link('Back to log in', '/').classes('w-full text-center text-blue-500 hover:text-blue-700 cursor-pointer no-underline')

                register_button.on_click(validate_and_register)

# Trang quên mật khẩu (/forgot-password)
@ui.page('/forgot-password')
def forgot_password_page():
    #ui.query('body').style('margin: 0; padding: 0; background: linear-gradient(135deg, #f0f4ff, #e5e7ff);')
    create_intro_page()
    # Tạo giao diện quên mật khẩu
    with create_centered_container():
        with ui.card().classes('w-full p-8 rounded-lg shadow-lg'):
            # Tiêu đề
            ui.label('Find your account').classes('text-3xl font-bold text-center mb-6')
            
            with ui.column().classes('w-full gap-4'):
                # Thông báo
                ui.label('* Please enter your registered email').classes('text-red-500 text-sm mb-2')
                # Input email
                email_input = ui.input('Email').props('rounded').props('outlined required').classes('w-full')
                
                # Xử lý xác minh email
                async def verify_email():
                    if not '@' in email_input.value:
                        ui.notify('Invalid email!', color='negative')
                        return
                    
                    user = user_db.find_user_by_email(email_input.value)
                    if user:
                        ui.notify('Account found! Verify informaion', color='positive')
                        ui.timer(2.0, lambda: redirect(f'/verify-account/{user.username}'))
                    else:
                        ui.notify('No account found', color='negative')

                # Nút tiếp tục
                ui.button('Continue', on_click=verify_email).props('rounded').classes('w-full bg-indigo text-white')
                
                # Link quay lại
                with ui.row().classes('w-full justify-center items-center gap-2 mt-4'):
                    ui.link('Back to log in', '/').classes('text-blue-500 hover:text-blue-700 cursor-pointer no-underline')

# Trang xác minh tài khoản (/verify-account/{username})
@ui.page('/verify-account/{username}')
def verify_account_page(username: str):
    #ui.query('body').style('margin: 0; padding: 0; background: linear-gradient(135deg, #f0f4ff, #e5e7ff);')
    create_intro_page()
    # Lấy giới hạn ngày
    min_date, max_date = get_date_limits()
    
    # Tạo giao diện xác minh
    with create_centered_container():
        with ui.card().classes('w-full p-8 rounded-lg shadow-lg'):
            # Tiêu đề
            ui.label('Verify information').classes('text-3xl font-bold text-center mb-6')
            
            with ui.column().classes('w-full gap-4'):
                # Thông báo
                ui.label('* Please enter correct registration information').classes('text-red-500 text-sm mb-2')
                # Form xác minh
                fullname_input = ui.input('User name').props('rounded').props('outlined required').classes('w-full')
                birthdate_input = ui.input('Date of birth*').props('rounded').props(f'outlined required type=date min="{min_date}" max="{max_date}"').classes('w-full')
                
                # Xử lý xác minh thông tin
                async def verify_info():
                    user = user_db.find_user_by_username(username)
                    if user and user.fullname == fullname_input.value and user.birthdate == birthdate_input.value:
                        ui.notify('Verified successfully! Reset password...', color='positive')
                        ui.timer(2.0, lambda: redirect(f'/reset-password/{username}'))
                    else:
                        ui.notify('Incorrect information!', color='negative')

                # Nút xác minh
                ui.button('Verify', on_click=verify_info).props('rounded').classes('w-full bg-indigo text-white')
                
                # Link quay lại
                with ui.row().classes('w-full justify-center items-center gap-2 mt-4'):
                    ui.link('Back', '/forgot-password').classes('text-blue-500 hover:text-blue-700 cursor-pointer no-underline')

# Định nghĩa trang đặt lại mật khẩu với tham số username
@ui.page('/reset-password/{username}')
def reset_password_page(username: str):
    #ui.query('body').style('margin: 0; padding: 0; background: linear-gradient(135deg, #f0f4ff, #e5e7ff);')
    create_intro_page()
    # Tạo container có căn giữa để hiển thị form
    with create_centered_container():
        # Tạo card chứa form đặt lại mật khẩu
        with ui.card().classes('w-full p-6'):
            # Tiêu đề của form
            ui.label('Reset password').classes('text-3xl font-bold text-center mb-6')
            
            # Tạo cột chứa các trường nhập liệu
            with ui.column().classes('w-full gap-4'):
                # Input field cho mật khẩu mới
                new_password = ui.input('New password*')\
                    .props('outlined required type=password').props('rounded')\
                    .classes('w-full')
                
                # Input field để xác nhận mật khẩu mới
                confirm_password = ui.input('Verify new passwprd*')\
                    .props('rounded').props('outlined required type=password')\
                    .classes('w-full')
                
                # Nút để thực hiện đặt lại mật khẩu
                reset_button = ui.button('Change password')\
                    .props('rounded').classes('w-full bg-indigo text-white')
                
                # Hàm xử lý sự kiện khi nhấn nút đặt lại mật khẩu
                async def reset_password():
                    # Kiểm tra xem hai mật khẩu có khớp nhau không
                    if new_password.value != confirm_password.value:
                        ui.notify('Password does not match!', color='negative')
                        return
                    
                    # Tìm user trong database
                    user = user_db.find_user_by_username(username)
                    if user:
                        # Cập nhật mật khẩu mới đã được mã hóa
                        user.password_hash = generate_password_hash(new_password.value)
                        user_db.update_user_password(user.username, user.password_hash)
                        # Hiển thị thông báo thành công
                        ui.notify('Change password successfully!', color='positive')
                        # Ẩn nút đặt lại mật khẩu
                        reset_button.visible = False
                        # Hiển thị link quay về trang đăng nhập
                        ui.link('Back to log in', '/')\
                            .classes('w-full text-center text-blue-500 hover:text-blue-700 cursor-pointer no-underline')
                    else:
                        # Hiển thị thông báo lỗi nếu không tìm thấy user
                        ui.notify('Error occurred!', color='negative')
                
                # Gán hàm xử lý sự kiện cho nút đặt lại mật khẩu
                reset_button.on_click(reset_password)

# Định nghĩa trang chủ sau khi đăng nhập
@ui.page('/home')
def home_page():
    #ui.query('body').style('margin: 0; padding: 0; background: linear-gradient(135deg, #f0f4ff, #e5e7ff);')
    # Tạo cột chứa nội dung trang chủ
    #with ui.column().classes('w-full items-center p-4'):
        # Hiển thị thông điệp chào mừng
    #    ui.label('Chào mừng đến trang chủ!')\
    #        .classes('text-2xl font-bold mb-4')
        # Tạo nút đăng xuất và chuyển hướng về trang đăng nhập
    #    ui.button('Đăng xuất', on_click=lambda: redirect('/'))\
    #        .classes('bg-red-500 text-white')
    pass


# Khởi chạy ứng dụng
ui.run()