## Links


* [Documentation](http://confluence.zubdim.com/)
* [Android prototype](http://ux.zubdim.com/android/index.html)
* [iOS prototype](http://ux.zubdim.com/ios/index.html)
* [Database scheme](http://dbdsgnr.appspot.com/app#ag1zfmRiZHNnbnItaHJkchMLEgZTY2hlbWEYgICAgMiAmgsM)

## Deploy

Used software:
* PostgreSQL
* RabbitMQ
* Redis

Notes:

* Do not use `./manage.py createsuperuser`, create user in `./manage.py shell`
with following commands:
```
>>> from accounts.models import User
>>> import datetime
>>> user = User.objects.create_user('admin', 'admin@wheelapp.com', 'admin', 'admin full name', 1, datetime.datetime.now())
>>> user.is_superuser = True
>>> user.save()
```
