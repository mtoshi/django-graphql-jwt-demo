django-graphql-jwt-demo 
====================================
* This repository is experimental for django-graphql-jwt.
* https://django-graphql-jwt.domake.io/en/latest/
* https://github.com/flavors/django-graphql-jwt


Installation
====================================
* Get repo and runserver.

.. code::

    $ python3.7 -m venv /tmp/django-graphql-jwt-demo && source /tmp/django-graphql-jwt-demo/bin/activate
    $ git clone git@github.com:mtoshi/django-graphql-jwt-demo.git
    $ cd django-graphql-jwt-demo
    $ pip install setuptools --upgrade && pip install pip --upgrade
    $ pip install -r requirements.txt
    $ cp .env.sample .env  # Please check env variables.
    $ python manage.py migrate
    $ python manage.py runserver 127.0.0.1:8000

* Access with your browser.

.. code::

    http://localhost:8000/graphql/


Create superuser
=======================================
* Create superuser for demo.

.. code::

    $ python manage.py createsuperuser 

    # Example

    Username (leave blank to use 'mtoshi'): admin
    Email address: admin@example.com
    Password: demopassword
    Password (again): demopassword
    Superuser created successfully. 

Superuser authentication
=======================================
* Authenticate with username(superuser) and password, and receive JWT.

.. code::

    # Request

    mutation {
      login(username: "admin", password: "demopassword") {
        token
      }
    }

    # Return

    {
      "data": {
        "login": {
          "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTg5NzI5MDU1LCJvcmlnSWF0IjoxNTg5NzI1NDU1fQ.OG-V5D68yOncxSqbvUbEQV77kDVZeOkC5sl7bBjYHLw"
        }
      }
    }

Verify admin JWT
=======================================
* Verify.

.. code::

    # Request

    mutation {
      verifyToken(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTg5NzI5MDU1LCJvcmlnSWF0IjoxNTg5NzI1NDU1fQ.OG-V5D68yOncxSqbvUbEQV77kDVZeOkC5sl7bBjYHLw") {
        payload
      }
    }

    # Return

    {
      "data": {
        "verifyToken": {
          "payload": {
            "username": "admin",
            "exp": 1589729055,
            "origIat": 1589725455
          }
        }
      }
    }

Create user
====================================
* Create test user(superuser restriction implemented).

.. code::

    # Request

    mutation {
      createUser(username: "testuser",
                 email: "testuser@example.com",
                 password: "demopassword") {
        user {
          id
          username
          email
        }
      }
    }

    # Return

    {
      "data": {
        "createUser": {
          "user": {
            "id": "2",
            "username": "testuser",
            "email": "testuser@example.com"
          }
        }
      }
    }

* Also you can create user with superuser JWT.
* Please add the following header when POST.

.. code::

    "Authorization: JWT superuser-jwt-value"

* If the JWT has expired, you will get the following error.

.. code::

    {"errors":[{"message":"Signature has expired", ...

* In case of JWT without permission, you will get the following error.

.. code::

    {"errors":[{"message":"You do not have permission to perform this action" ...

Test user authentication
=======================================
* Authenticate with username and password, and receive JWT.

.. code::

    # Request

    mutation {
      login(username: "testuser", password: "demopassword") {
        token
      }
    }

    # Return

    {
      "data": {
        "login": {
          "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg5NzMwMTk5LCJvcmlnSWF0IjoxNTg5NzI2NTk5fQ.U6hj3PordFJzt2y96lMSdWWPLx86F_SMWE2GvM3V_fc"
        }
      }
    }

* Get user name and email with testuser JWT.

.. code::

    # Request

    query {
      user(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg5NzMwMTk5LCJvcmlnSWF0IjoxNTg5NzI2NTk5fQ.U6hj3PordFJzt2y96lMSdWWPLx86F_SMWE2GvM3V_fc") {
        username
        email
      }
    }

    # Return

    {
      "data": {
        "user": {
          "username": "testuser",
          "email": "testuser@example.com"
        }
      }
    }

* Get all users with testuser JWT(superuser restriction implemented).

.. code::

    # Request

    query {
      users(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIiwiZXhwIjoxNTg5NzMwMTk5LCJvcmlnSWF0IjoxNTg5NzI2NTk5fQ.U6hj3PordFJzt2y96lMSdWWPLx86F_SMWE2GvM3V_fc") {
        username
        email
      }
    }

    # Return

    {
      "errors": [
        {
          "message": "You do not have permission to perform this action",
          "locations": [
            {
              "line": 4,
              "column": 7
            }
          ],
          "path": [
            "users"
          ]
        }
      ],
      "data": {
        "users": null
      }
    }

* Good! Superuser restriction is in effect.
* Try again with superuser JWT.

.. code::

    # Request

    query {
      users(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTg5NzI5MDU1LCJvcmlnSWF0IjoxNTg5NzI1NDU1fQ.OG-V5D68yOncxSqbvUbEQV77kDVZeOkC5sl7bBjYHLw") {
        username
        email
      }
    }

    # Return

    {
      "data": {
        "users": [
          {
            "username": "admin",
            "email": "admin@example.com"
          },
          {
            "username": "testuser",
            "email": "testuser@example.com"
          }
        ]
      }
    }

