[![Build Status](https://travis-ci.org/tonykimathi/Andela_WeConnect_v2.svg?branch=ft-get-all-user-reviews-157660976)](https://travis-ci.org/tonykimathi/Andela_WeConnect_v2)
[![Coverage Status](https://coveralls.io/repos/github/tonykimathi/Andela_WeConnect_v2/badge.svg?branch=ft-get-all-user-reviews-157660976)](https://coveralls.io/github/tonykimathi/Andela_WeConnect_v2?branch=ft-get-all-user-reviews-157660976)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/51c2106d3a9842aabe2c996e22537d6a)](https://www.codacy.com/app/tonykimathi/Andela_WeConnect_v2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tonykimathi/Andela_WeConnect_v2&amp;utm_campaign=Badge_Grade)

# WeConnect

This is an API for WeConnect, a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to:

- Register for an account
- Login into registered account
- Reset forgotten password
- Change password
- Delete user account
- Register, Update and Delete a Business
- View all Businesses
- View single Business
- Write Reviews on a business
- View all Reviews to a business
- Search and filter businesses

## Prerequisites

- Python 3.6 or a later version
- PostgreSQL

## Installation

Clone the repo.
```
git clone https://github.com/tonykimathi/Andela_WeConnect_v2
```

and navigate into the folder: 

```
$ cd /Andela_WeConnect_v2
```

## Virtual environment

Create a virtual environment:
```
virtualenv venv
```
Activate the environment
```
$ source venv/bin/activate
```

## Dependencies

Install package requirements to your environment.
```
pip install -r requirements.txt
```

## Database migration

Create two Databases in PostgreSQL:
- andela_weconnect (production DB)
- test_db (testing DB)

Run the following commands for each database:
```
python manager.py db init

python manager.py db migrate

python manager.py db upgrade

```

## Testing

To set up unit testing environment:
```
$ pip install nose
$ pip install coverage
```

To run tests perform the following:
```
$ nosetests -v --with-coverage --cover-package=app
```

## Start The Server

To start the server run the following command
```
python run.py
```
The server will run on http://127.0.0.1:5000/

## Testing API on Postman

*Note* Ensure that after you succesfully login a user, you use the generated token for the endpoints that require authentication. 

### API endpoints

```
| Endpoint | Method |  Functionality | Authentication |
| --- | --- | --- | --- |
| /api/v2/register | POST | Creates a user account | FALSE
| /api/v2/login | POST | Logs in a user | TRUE
| /api/v2/logout | POST | Logs out a user | TRUE
| /api/v2/reset-password | POST | Reset user password | TRUE
| /api/v2/change-password | PUT | Change user password | TRUE
| /api/v2/delete-account | POST | Delete user password | TRUE
| /api/v2/businesses | POST | Register a business | TRUE
| /api/v2/businesses | GET | Retrieves all businesses | OPTIONAL 
| /api/v2/businesses/{businessid} | GET | Retrieve a single business | OPTIONAL
| /api/v2/businesses/{businessid} | PUT | Update a business profile | TRUE
| /api/v2/businesses/{businessid} | DELETE | Delete a business | TRUE
| /api/v2/businesses/{businessid}/reviews | POST | Post a review on a business | TRUE
| /api/v2/businesses/{businessid}/reviews | GET | Get all reviews to a business | OPTIONAL
| /api/v2/search | GET | Search and filter businesses | OPTIONAL

```
## Pagination

The API enables pagination by passing in *page* and *limit* as arguments in the request url as shown in the following example:

```
http://127.0.0.1:5000//api/v2/businesses?page=1&limit=20

```

## Searching and filtering

The API implements searching based on the name using a GET parameter *q* as shown below:
```
http://127.0.0.1:5000//api/v2/search?q=Andela
```

## Author

* **Tony Kimathi Mputhia** - [tonykimathi](https://github.com/tonykimathi)

