# py-stadium
Mate Academy portfolio project. Website for tickets reservation.


## General information 

The purpose of the project is to create back end of the website where authorised
users can reserve tickets to visit the stadium. Any user can register at the 
site and after the registration he can access (read only) the pages SportArenas, 
Genres, Actors, Teams, Sections, Events, EventSessions. Users can create orders
and add tickets to them. A user can see only own orders. Our stadium can sell
tickets not only for sports events, it can be adapted to
a wide scope of activities. There are a set of venues at the stadium - 
SportArenas, e.g. for football, hockey, concerts, exhibitions, 
corporates, etc. Thus, each event can be marked to some Genres, e.g. football,
basketball, rock concert, dance conquest, fair, etc. Each SportArena has 
a set of section for fans. For different events different set of sections 
can be for visitors. For example - for a rock concert fan zones can be 
deployed at the football field, and obviously not for football match. One 
event can repeat several times e.g. travelling circus or zoo can perform 
for months, probable even on different revenues. Concerts can be related 
with actors, sports events can be related with teams. Only authorised staff 
has rights to edit Genres, Actors, Teams, SportArenas, Sections, Events, 
EventSessions.


## Installation

1. Python3 must be already installed.
2. ModHeader must be installed for using JWT authentication.
3. Docker must be installed in the case you need to work with dockerized version.


```shell
git clone https://github.com/AndyStarGitHub/py-stadium/
cd py-stadium
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py runserver
```


```Docker shell
7777777777777777
```


## Additional software requirements
* crispy-bootstrap4             2024.10
* Django                        5.2.1
* django-crispy-forms           2.4
* django-debug-toolbar          5.2.0
* django-storages               1.14.6
* djangorestframework           3.16.0
* djangorestframework_simplejwt 5.5.0
* drf-spectacular               0.28.0
* Faker
* flake8-quotes                 3.3.1
* flake8-variables-names        0.0.5
* gunicorn                      23.0.0
* inflection                    0.5.1
* jsonschema                    4.23.0
* jsonschema-specifications     2025.4.1
* mccabe                        0.7.0
* packaging                     25.0
* pep8-naming                   0.13.2
* pillow                        11.2.1
* pip                           23.2.1
* psycopg                       3.1.18
* psycopg-binary                3.2.7
* psycopg2-binary               2.9.10
* pycodestyle                   2.9.1
* pyflakes                      2.5.0
* PyJWT                         2.9.0
* python-dotenv                 1.1.0
* pytz                          2025.2
* PyYAML                        6.0.2
* referencing                   0.36.2
* rpds-py                       0.24.0
* setuptools                    80.3.1
* qlparse                      0.5.3
* typing_extensions             4.13.2
* tzdata                        2025.2
* uritemplate                   4.1.1
* uv                            0.6.13
* whitenoise                    6.9.0


## Features

1. Any user can register at the site with his email at 
    http://127.0.0.1:8000/api/user/register/.
2. The registered user can  sign in with obtained tokens at
    http://127.0.0.1:8000/api/user/token/.
3. The user can browse his profile at
    http://127.0.0.1:8000/api/user/me/.
4. The documentation is available at
    http://127.0.0.1:8000/api/doc/swagger.
5. The authorized user can started browsing at 
    http://127.0.0.1:8000/api/stadium/.
6. It is possible to skip from list presentation of items to 
    respective instances by it' id 
    http://127.0.0.1:8000/api/stadium/actors/11/). The needed 
    id can be found at list page.
7. Event list can be filtered by genres, actors, teams (e.g.
    http://127.0.0.1:8000/api/stadium/events/?teams=Dynamo).
8. Event session list can be filtered by sportarenas, events,
    event session date(e.g.
    http://127.0.0.1:8000/api/stadium/eventsessions/?show_time=2025-05-11
   ).
9. Admin panel can be reach here: http://127.0.0.1:8000/admin.
10. For testing the command should be run from terminal:
    python manage.py test.
11. Each user is allowed to browse pages read only. 
12. Each user can create his own order and reserve tickets (if not 
    sold out) for event sessions.
13. Useful information is available for users - the capacity of each 
    section of sport arena, the number of reserved and available tickets
    for any event session.


## Demo

The project can be cloned from https://github.com/AndyStarGitHub/py-stadium.

Training database has been populated with faked data. 

To login as a superuser with the credentials:
    Login: super@stadium.mate
    Password: ueur!!77eeen


## Run with Docker

Docker must be installed.
To run the commands:
    docker-compose build
    docker-compose up



