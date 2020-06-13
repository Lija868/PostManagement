# Post
Post Management System
1. download or clone the project (https://github.com/Lija868/PostManagement.git) use development branch
2. open post folder in corresponding ide.
3. replace appropriate values for DATABASES  in settings.py file (post\post\settings.py)
4. install the requirements using pip install -r /path/to/requirements.txt
6. create a database in the corresponding db with name in settings file( mysql command :- create database post_system )
6. run migration script(python manage.py migrate)
7. run the server by activating virtual env 
source venv/bin/activate
python manage.py runserver

Post and post tags and post images are added by admin
so create a super user by using command python manage.py createsuperuser

Reference of Api Documentation 
https://documenter.getpostman.com/view/3601477/Szzhddf5