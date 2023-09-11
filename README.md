1. Create Virtual env
`python -m venv env`

2. Activate Virtual env

For linux - `source env/bin/activate`
For windows - `env\Scripts\activate`

3. Install Python packages

`pip install -r requirements.text`

4. Create Database on your system and replace the creds of database in `database.database.py` file

5. Run the server

`uvicorn main:app --reload`
