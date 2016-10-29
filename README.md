# Wo Ist Bier Backend
[![Build Status](https://travis-ci.org/WoIstBier/bier-django.svg?branch=master)](https://travis-ci.org/WoIstBier/bier-django)

Current work is ongoing on the v2 branch.
```shell
pip install -r requirements.txt
```

should work. Tests can be run like this:
```shell
python manage.py test --settings=woistbier.local_test_settings
```

For development, first create the database, add a superuser and load some data
via
```shell
python manage.py migrate --settings=woistbier.local_test_settings
python manage.py createsuperuser --settings=woistbier.local_test_settings
...
python manage.py loaddata woistbier_rest/fixtures/test_data.json --settings=woistbier.local_test_settings
```

The development server starts like
```shell
python manage.py runserver --settings=woistbier.local_test_settings
```
