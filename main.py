import asyncio
from flask import Flask, render_template, redirect, url_for, request, make_response, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from services.user_requests import UserRequests, UserDto, UserLogin
from services.models import init_main
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import SECRET_KEY

user_requests = UserRequests()
app = Flask(__name__)
app.secret_key = SECRET_KEY
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin.fromDB(user_id)

@app.route('/')
def main():
  return render_template('index.html', name=current_user.get_name() if current_user.is_authenticated else "Гость", username=current_user.get_username() if current_user.is_authenticated else "Guest", user_id=current_user.get_user_id() if current_user.is_authenticated else "Guest", email=current_user.get_email() if current_user.is_authenticated else "Guest")

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def reg_user():
    name = request.form.get("register_name")
    email = request.form.get("register_email")
    username = request.form.get("register_username")
    password = request.form.get("register_password")
    confirm_register_password = request.form.get("confirm_register_password")
    password_hash = generate_password_hash(password)


    check_username = asyncio.run(user_requests.check_username(username))
    check_email = asyncio.run(user_requests.check_email(email))

    if check_username > 0:
        return "Юзернейм уже занят"

    if check_email >0:
        return "Email уже зарегистрирован"

    if password!=confirm_register_password:
        return "Пароли не совпадают"

    new_user = UserDto(name, email, username, password_hash)
    asyncio.run(user_requests.add(new_user))
    return "Успешная регистрация"


@app.route('/authorize', methods=['GET', 'POST'])
def auth_user():
    logout_user()
    username = request.form.get("auth_username")
    password = request.form.get("auth_password")
    print("Введенный пользователем пароль ",password)
    if password:
        password_hash = asyncio.run(user_requests.get_password(username))
        print("Хеш пароль из Базы ", password_hash)

    if check_password_hash(password_hash, password) == True:
        user = asyncio.run(user_requests.getUserByUsername(username))
        userlogin = UserLogin().create(user)
        rm = False
        if request.form.get("save_computer"):
            rm = True
        login_user(userlogin, remember=rm)
        return redirect('/')
        #return f"Авторизация пройдена {userlogin.get_name()}{current_user.get_name()}"
    else:
        return render_template('wrong_password.html')






if __name__ == '__main__':
    asyncio.run(init_main())  # инитим создание таблиц (sqlalchemy)
    app.run(debug=True)
