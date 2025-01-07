# HR Manager Web Application

I'm a Web application with (almost) no tests.

Test me!

## Running the backend - docker

* Install docker and docker-compose
* Make sure port 5433 and 8000 are free
* Run:

```
$ cd backend/
$ docker compose up --build
```

## Running the backend - python

Install [poetry](https://python-poetry.org)


Go to the `backend/.env` file with this contents:
```
DJANGO_SECRET_KEY=this-is-an-unsafe-secret
DJANGO_DEBUG=true
```


```
$ poetry install
$ poetry run python manage.py migrate
$ poetry run python manage.py runserver
```

## Instructions

Do _not_ look inside the `backend/` folder yet - you're doing black-box testing at this point.

### Step 1

Do some manual, exploratory testing first

### Step 2

* Open the folder corresponding to your prefer programming language,
* Install and configure `playwright`
* Make sure you can run the end-to-end tests

Once it's running, add tests for the bugs found during step 1.

Make sure to use the "Page Object Model" design pattern.

Also, do _not_ issue POST or GET requests outside the browser
(you'll do that in step 3)

### Step 3


* Make sure you can run the integration tests
 
Once they're running, rewrite the tests from step 2 using raw http request
and SQL queries.

<details>
<summary>Some clues</summary>
<ul>
<li>You'll see the PostgreQSL credentials in the docker logs - you can use DBeaver to go look at the database</li>
<li>You can use your browser dev extensions to look at the payload of the POST requests</li>
<li>And you can also look at the backend code to see the routes (in `hr/urls.py`)</li>
</ul>
</details>
