# WhatYouKnow.

This is a [demo](http://3.234.249.104:8080/) project of the blogging platform WhatYouKnow. Written using Django and
Fomantic-ui.

## Dependencies

Python 3.10

## Get up and running

1. Clone this repo
2. Create a virtual environment and install the requirements:

```
cd whatyouknow
pipenv install
```

3. Initialize virtual environment:

```
pipenv shell
```

4. Create a file named `.env`

Inside add:

```
SECRET_KEY={create_and_add_your_own_SECRET_KEY_here_with_no_spaces}
DEBUG=True
```

or you can just execute the generate-env.sh script:

```
chmod +x generate-env.sh
./generate-env.sh
```

NOTE:

For more information on how you can generate a secret key visit [here](https://foxrow.com/generating-django-secret-keys)
or you can generate a key online [here](https://www.miniwebtool.com/django-secret-key-generator/).

5. Run migrations:

```
python manage.py migrate
```

6. Run collect static:

```
python manage.py collectstatic
```

7. Get the server up and running:

```
python manage.py runserver
```

or:

```
pipenv run server
```

## Generating test data

To generate test data, run the command in a terminal:

```
python -m data_gen
```

And wait a little. To control the amount of data generated, specify a factor using the optional `[-f, --factor]` argument:

```
python -m data_gen -f 5
```