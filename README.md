# Установка и запуск
<ol>
  <li>Клонировать этот репозиторий <code>git clone https://github.com/BgPyt/second_task.git</code></li>
  <li>В env файле где <strong>PG_ADMIN_EMAI</strong> и <strong>PG_ADMIN_PASSWORD</strong> вставить свои значения для входа в БД-интерфейс</strong></li>
  <li>Создание образов и запуск контейнеров в фоновом режиме<code>docker-compose up -d</code></li>
</ol>
<blockquote>Доступ к документаци к тестовому API http://localhost:8000/docs</blockquote>

#  Реализация 
<ul>Стек применения:
  <li>Fastapi</li>
  <li>alembic</li>
  <li>асинхроннй движок - <b>asyncpg2</b></li>
  <li>Sqlalchemy</li>
  <li>Pydantic</li>
  <li>Fastapi-users</li>
  <li>Postgresql</li>
</ul>

<ul><h2>Создание пользователя, POST:</h2>
  <ul>
    <li><strong>Регистрация:</strong><br>
      POST-запрос вида:
<br>
URL: http://localhost:8000/auth/register
<br>
Request body(raw - JSON): {"email": "string", password": "string", "is_active": true, "is_superuser": false, "is_verified": false, username": "string"}
<br>
Response example: {"email": "string", password": "string", "is_active": true, "is_superuser": false, "is_verified": false, username": "string"}
<br>
      <li><strong>Авторизация:</strong><br>
        POST-запрос вида:
<br>
URL: http://localhost:8000/auth/jwt/login
<br>
Request body: (x-www-form-urlencoded): username = email, password = password
<br>
Response example: {
    "access_token": "Jcn2JjK7UGXc8AUGQ8kEoE9YH9UGt5yNR5qFf7uhgZI",
    "token_type": "bearer",
    "UUID": "eb3c5cd4-b08f-4341-bba1-46271b606ab5"
}
<br>
  </ul>
</ul>
<ul><h2>Добавление аудиозаписи, POST</h2>
  <ul>
    <li><strong>Добавить аудиозапись</strong><br>
      POST-запрос вида:
<br>
URL: http://localhost:8000/uploadfile/?UUID={ваш UUID}
<br>
HEADERS: Authorization:Bearer {token}
<br>
Request body(form-data): file = {select file}
<br>
Response example: {
    "url": "http://0.0.0.0:8000/record?id=f061bbdd-fe3c-477d-aa31-8906acfcc481&user=eb3c5cd4-b08f-4341-bba1-46271b606ab5"
}
<br>
 <li><strong>Доступ к аудиозаписи</strong><br>
      GET-запрос вида:
<br>
URL: http://localhost:8000/record?id=id_записи&user=id_пользователя
<br>
Response example: Загрузка файла 
<br>
