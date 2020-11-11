# Enoki

#Python 3.8

# Start app with Docker
```sh
$ cd Enoki
$ docker-compose up
```

# Otherwise you have to install the dependencies manually
```sh
$ pip install -r requirements.txt
$ python manage.py runserver
```

Good to know:
  - One user is created in the database, you can log in with username=admin and password=admin
  - You can add more user at localhost:8000/admin
  
  If you are on Linux and you are experiencing a permission problem it is probably because of SELinux (Security-Enhanced Linux), you can disable it by typing the following command:
```sh
$ sudo setenforce 0
```
