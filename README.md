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
Do everuthing as priviously done, exept running test server

12) apply updates 
`sudo apt apdate`, `sudo apt upgrade`
13) install Postresql `sudo apt install postgresql`
14) check it's installation
```
sudo systemctl is-active postgresql
sudo systemctl is-enabled postgresql
sudo systemctl status postgresql
```
15) confirm readiness
`sudo pg_isready`
16) log in as pq user and run shell
```
sudo su - postgres
psql
```
17) create user and db
```
CREATE USER user WITH PASSWORD 'pass';
CREATE DATABASE test;
GRANT ALL PRIVILEGES ON DATABASE test to user;
\q
```
18) exit from user
`exit`
19) 