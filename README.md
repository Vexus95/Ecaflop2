# HR Manager Web Application

I'm a Web application with (almost) no tests.

Test me!


## Running the backend

Install Python >=3.12

Go to the `backend` folder

Create a copy of the `.env.local` file named `.env`

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

See: [The Playwright Kata](https://github.com/dmerejkowsky/kata-playwright)

# Part 3 - integration tests

## Step 1

* Make sure you can run the **integration** test for add-team.

You'll see it only works when the database contains no other team.

Find a strategy to handle clean separation between tests while still 
using the database.

Note: do NOT use the `/reset_db`  route, that's cheating ...

Once your done, rewrite the tests from part 2 using raw HTTP requests
and SQL queries.

Some clues:

Use DBEaver to inspect the contents of the database by opening the file `db.sqlite3`.

Use your browser dev extensions to look at the payload of the POST requests

The tables used by the backend code can be created and dropped using the `up`  and `down` sql scripts respectively.
