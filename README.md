# django_quiz

> A Quiz app to write exams using Django.
> <br/>

## Features

- Admin (superuser) can manage quiz by adding and removing them.
- students can attend the quiz and see the score they get for corresponding quiz.

<br/>

## Getting started

Add os environments on `settings.py`

```sh
os.environ['SECRET_KEY'] = 'your secret key'
os.environ['MONGODB_URI'] = 'your mongodb atlas url'
```

<br/>

Install all packages using `pip`

```sh
$ pip install -r requirements.txt
```

<br/>

Run this project on server

```sh
$ python manage.py runserver
```

<br/>
