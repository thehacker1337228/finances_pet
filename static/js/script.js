console.log("Скрипт подключен")

var authModal = document.getElementById('authModal')
var auth_username = document.getElementById('auth_username')

authModal.addEventListener('shown.bs.modal', function () {
  auth_username.focus()
})


var registerModal = document.getElementById('registerModal')
var register_name = document.getElementById('register_name')

registerModal.addEventListener('shown.bs.modal', function () {
  register_name.focus()
})

console.log("Скрипт с модалками выполнен")






document.getElementById('registerForm').addEventListener('submit', async (e) => {
  e.preventDefault(); 

  const form = e.target;
  const formData = new FormData(form);

  const password = document.getElementById('register_password').value;
  const confirmPassword = document.getElementById('confirm_register_password').value;

  if (password === confirmPassword) {
    const response = await fetch('/register', {
      method: 'POST',
      body: formData
    });

    const text = await response.text();
    alert(text);
  } else {
    alert("Пароли не совпадают");
  }
})


var name_of_user = document.getElementById('name_of_user').textContent
console.log(name_of_user, " Имя пользователя")
if (name_of_user !== 'Гость') {
  console.log("if сработал")
  document.getElementById("loginBtns").classList.add('d-none');

  const elle = document.getElementById("loginBtns");
  elle.classList.remove('d-flex');
  elle.classList.add('d-none');


  const el = document.getElementById("usernameBtn");
  el.classList.remove('d-none');
  el.classList.add('d-flex');


}


