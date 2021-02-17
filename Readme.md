It is a django blog app. Here you can create, modify and delete the blogs very easily. But to view and create the blogs , you have to first strictly register with us. It is not mandatory to provide any personal email or mobile. You can provide any random email or mobile to register . Once you have register with this app, you can create or delete your own blogs and view all the blogs.

Steps to use this app:

-> Install python and git in your system. 

-> After installing git, open git bash.

-> git clone https://github.com/Subhamtyagi684/blogapp.git

-> Now create a virtual environment with this code ->    python -m venv venv

-> Once venv created successfully, activate it by -> source venv/Scripts/activate

-> After that go inside the main directory by -> cd blogapp/

-> create a database file by -> touch db.sqlite3

-> Once it is created, create a .env file -> touch .env

-> inside .env file , provide any random SECRET_KEY, FOR e.x. -> SECRET_KEY = 'hello_world'

-> now save it.

-> Once you have completed all the steps successfully.

-> run python manag.py makemigrations

-> run python manage.py migrate

-> Now run the django server using ->   python manage.py runserver 

-> If everything was fine, you will see a sign up form.

-> Provide the details , you can provide any random details .

-> After submitting, you will see a message 'User created successfully'.

-> Now you can login in the app using email and password to this app.

-> Once logged in, you can create your blog and  view all the blogs.

-> After using app, click on logout from the navbar.

-> Done.

There is also some API'S, you can test in the postman:

1. Register API ->    http://localhost:8000/api/register/
2. Login API ->    http://localhost:8000/api/login/
3. Create data in Category table ->   http://localhost:8000/createcat/
4. Modify(update, delete) data in Category table ->  http://localhost:8000/modifycat/pk
5. Create data in Blog table ->   http://localhost:8000/createblog/
6. Modify(update, delete) data in Blog table ->  http://localhost:8000/modifyblog/<int:pk>
7. Search blog with category ->   http://localhost:8000/api/searchblog/<str:cat>
