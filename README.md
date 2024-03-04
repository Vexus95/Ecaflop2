# HR Manager Web Application

I'm a Web application with (almost) no tests.

Test me!

## Running the backend

* Install docker and docker-compose
* Make sure port 5433 and 8000 are free
* Run:

```
$ docker compose up --build
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
