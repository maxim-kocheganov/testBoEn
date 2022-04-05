# test for program tactics

## installation

### windows - test server
1) python -m venv .venv
2) .\.venv\Sripts\activate
3) pip install -r .\requirements.txt

### Linux (Ubuntu) - test server
1) install python 3.9.7 or higher (Already shipped for default Ubuntu)
2) install git 
`sudo apt install git`
3) clone repo
`git clone https://github.com/maxim-kocheganov/testBoEn.git`
4) `cd testBoEn`
5) install python venv (Ubuntu way)
`sudo apt install python3.9-venv`
6) create environment in new foldier .venv
`python3 -m venb .env`
7) apply environment
`source .env/bin/activate`
8) install requirements
`pip3 install -r requirements.txt`
9) goto projects foldier
`cd exeldb`
10) do migrations
`python3 manage.py makemigrations`
`python3 manage.py migrate`
11) run test server on localhost
`python3 manage.py runserver`

### linux (Ubuntu) - production
Do everuthing as priviously done + deploy on prod
(TODO)