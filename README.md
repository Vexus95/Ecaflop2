# HR Manager Web Application

I'm a Web application with (almost) no tests.

Test me!


## Running the backend

Install Python >=3.12

Go to the `backend` folder

Create a `.env` file containing:

```
DJANGO_SECRET_KEY=this-is-an-unsafe-secret
DJANGO_DEBUG=true
```

Run:

```
# Create a virtual environment
$ python -m venv .venv --prompt hr-db
# Activate it
$ source .venv/bin/activate
# or
.venv\Scripts\activate.bat
# Install dependencies
$ pip install -r requirements.txt
# Migrate the database
$ python manage.py migrate
# Run the server
$ python manage.py runserver
```

# Part 1 - manual testing

Do _not_ look inside the `backend/` folder yet - you're doing black-box testing at this point.

## Step 1

Do some manual, exploratory testing first.

Create a test plan and run it manually.

## Step 2

Put all the bugs you find into a bug tracker

# Part 2 - end-to-end testing

## Step 1

* Open the folder corresponding to your prefer programming language
* Install and configure `playwright`
* Install a browser that playwright can control:

```
playwright install chromium
```

## Step 2

* Use `playwright codegen` to automate the steps from one your tests in the test plan.

* Add the code to the git repository *without any changes*.

* Modify the code so that it can run.

## Step 3


* Make sure you can run the already existing **end-to-end** `add-team` test

Once it's running, add tests for all the bugs found during step 1.

Notes:

* Use a fixture to reset the database
* Make sure to use the "Page Object Model" design pattern.
* Do _not_ issue POST or GET requests directly outside the browser
(you'll do that in a later step)

## Step 4

Compare the code written using the Page Object Model with the one playwright automatically generated.

# Part 3 - integration tests

## Step 1

* Make sure you can run the **integration** test for add-team.

You'll see it only works when the database contains no other team.

Find a strategy to handle clean separation between tests while still 
using the database.
 
Once your done, rewrite the tests from part 2 using raw http request
and SQL queries.

Some clues:

Use DBEaver to inspect the contents of the database by opening the file `db.sqlite3`.

Use your browser dev extensions to look at the payload of the POST requests

The tables used by the backend code can be created and dropped using the `up`  and `down` sql scripts respectively.
