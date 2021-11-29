# WhatYouKnow.

This is a demo project of a site for blogs WhatYouKnow. Written in Django and Fomantic-ui.

## Get up and running

1. Clone this repo
2. Create a virtual environment:

```
cd whatyouknow
python -m venv ./venv
```

3. Activate the virtual environment:

```
source ./venv/bin/activate
```

4. Install the requirements:

```
pip install -r requirements.txt
```

5. Create a file named `.env`

Inside add:
```
SECRET_KEY={create_and_add_your_own_SECRET_KEY_here_with_no_spaces}
DEBUG=True
```

NOTE:

For more information on how you can generate a secret key visit [here](https://foxrow.com/generating-django-secret-keys) or you can generate a key online at [here](https://www.miniwebtool.com/django-secret-key-generator/).

6. Run migrations:

```
python manage.py migrate
```

7. Run collect static:

```
python manage.py collectstatic
```

8. Get the server up and running:

```
python manage.py runserver
```


## Generating test data
To generate test data, run the command in the terminal:
```
python -m data_gen
```
And wait a little. To control the amount of data generated, specify a factor using the optional [-f, --factor] parameter:
```
python -m data_gen -f 5
```