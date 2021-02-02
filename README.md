# basic_api_full-stack-python


## Instructions

1. Start local postgres server via psql in the command line
2. Launch virtual environment 
```
python3 -m venv venv
source venv/bin/activate
```
3. Download dependencies 
```
pip3 install -r requirements.txt
```
4. Init postgres database
```
flask db init 
``
5. migrate schema
```
flask db migrate
```
6. upgrade schema to postgres db
```
flask db upgrade 
```

Now you have a restful api via localhost:5000/api, or localhost:3000 when the frontend is running. 
