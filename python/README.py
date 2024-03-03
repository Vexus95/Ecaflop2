# Python tests

## Installing dependencies

```
python -b venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Running end-to-end tests

```
playwright install chromium
pytest --base-url http://127.0.0.1:8000 --browser=chromium --headed end_to_end_tests --slowmo=1000
```

## Running integration tests

```
pytest integration_tests
```
