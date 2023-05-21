# Arya.ai Assignment

## Prerequisites

- Docker (with docker compose)

## Project Setup

1. clone the repository from [git@github.com:RajeshJ3/arya.ai.git](https://github.com/RajeshJ3/arya.ai)

```sh
$ git clone git@github.com:RajeshJ3/arya.ai.git
```

2. create a `.env` file, take inspiration from `env.example`

```
# server
SECRET_KEY='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
DATABASE_URL='postgresql+psycopg2://postgres:postgres@db:5432/bank'
BROKER_URL='redis://redis:6379/0'

# postgres
POSTGRES_DB='bank'
POSTGRES_PASSWORD='postgres'
POSTGRES_USER='postgres'
PGDATA='/var/lib/postgresql/data/pgdata'
```

3. Once everything looks good, just run the servers

```sh
$ docker compose up --build
```

4. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

5. Test the APIs in [Postman](https://www.postman.com/cloudy-astronaut-15041/workspace/rajeshj3/collection/18151058-5b966438-4f35-4890-be0b-0615eecf4401)

## API Testing Order

1. Test out the root (`/`) end-point first. See if it returns -

```json
{
  "detail": "PING PONG! It worked 🚀"
}
```

2. Create a User account at registration(`/auth/registration/`) end-point

> Request Body

```json
{
  "email": "john@mail.com",
  "first_name": "John",
  "last_name": "Doe",
  "password1": "securepassword",
  "password2": "securepassword"
}
```

> Response Body

```json
{
  "details": "Account created!"
}
```

3. Login to John's account through login(`/auth/login/`) end-point

> Request body

```json
{
  "email": "john@mail.com",
  "password": "password"
}
```

> Response Body

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImlhdCI6MTY4NDY4NTEzOCwiZXhwIjoxNjg0NzcxNTM4fQ.rSFlKQsppc2fYXoX5nH8kR4FQM0N24xI5WmEu7fm4Fk",
  "user": {
    "id": 1,
    "email": "john@mail.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

4. Let's view the user's profile(`/accounts/profile/`)

**NOTE:** Make sure to pass the access token in the headers now onwards, to access the user's resources.

> Response body

```json
{
  "id": 1,
  "email": "john@mail.com",
  "first_name": "John",
  "last_name": "Doe",
  "bank_accounts": [
    {
      "amount": 0,
      "user_id": 1,
      "id": 1
    }
  ]
}
```

5. Let's view the user's bank accounts(`/bank/accounts/`)

> Response body

```json
[
  {
    "id": 1,
    "amount": 0,
    "user_id": 1,
    "entries": [],
    "credits": [],
    "debits": [],
    "statements": []
  }
]
```

6. Add some funds to this user's bank account via `/bank/accounts/{account_id}/deposit/` end-point

> Request body

```json
{
  "amount": 10000
}
```

> Response body

```json
{
  "id": 1,
  "amount": 10000,
  "entry_type": "deposit",
  "bank_account_id": 1,
  "created_at": 1684685498
}
```

7. Now, withdraw Rs. 1,500 from the account through `/bank/accounts/{account_id}/withdraw/`

> Request body

```json
{
  "amount": 1500
}
```

> Response body

```json
{
  "id": 2,
  "amount": 1500,
  "entry_type": "withdraw",
  "bank_account_id": 1,
  "created_at": 1684685604
}
```

8. View the bank account's status now through `/bank/accounts/{account_id}/`

> Response body

```json
{
  "id": 1,
  "amount": 8500,
  "user_id": 1,
  "entries": [
    {
      "entry_type": "deposit",
      "id": 1,
      "created_at": "2023-05-21T16:11:38.792672",
      "amount": 10000,
      "bank_account_id": 1
    },
    {
      "entry_type": "withdraw",
      "id": 2,
      "created_at": "2023-05-21T16:13:24.824297",
      "amount": 1500,
      "bank_account_id": 1
    }
  ],
  "credits": [],
  "debits": [],
  "statements": []
}
```

9. Now create another user(Jane), and transfer Rs.5,000 to their account.

> Reuqest body

```json
{
  "amount": 5000
}
```

> Response body

```json
{
  "id": 1,
  "amount": 5000,
  "source_bank_account_id": 1,
  "destination_bank_account_id": 2,
  "created_at": 1684686009
}
```

10. View the bank account's status again (refer to 8th point)

> Response body

```json
{
  "id": 1,
  "amount": 3500,
  "user_id": 1,
  "entries": [
    {
      "entry_type": "deposit",
      "id": 1,
      "created_at": "2023-05-21T16:11:38.792672",
      "amount": 10000,
      "bank_account_id": 1
    },
    {
      "entry_type": "withdraw",
      "id": 2,
      "created_at": "2023-05-21T16:13:24.824297",
      "amount": 1500,
      "bank_account_id": 1
    }
  ],
  "credits": [],
  "debits": [
    {
      "amount": 5000,
      "destination_bank_account_id": 2,
      "created_at": "2023-05-21T16:20:09.271646",
      "source_bank_account_id": 1,
      "id": 1
    }
  ],
  "statements": []
}
```

11. The Scheduled Job

Although, the job is schedules to run at 7:00AM if each month, but we can also use a DEBUG api (`/debug/generate-statements/`) to test out the dependent end-points.

> Response body

```josn
{
    "details": "Task #edf12d8e-fcbc-421d-8793-69a37eb0e037 scheduled"
}
```

12. Now, let's see if the statement is generated or not, Triger the statements API(`/bank/accounts/{account_id}/statements/`)

> Response body

```json
[
  {
    "id": 1,
    "month": 5,
    "year": 2023,
    "json_data": {
      "entries": [
        {
          "id": 1,
          "amount": 10000,
          "entry_type": "deposit",
          "bank_account_id": 1,
          "created_at": 1684685498
        },
        {
          "id": 2,
          "amount": 1500,
          "entry_type": "withdraw",
          "bank_account_id": 1,
          "created_at": 1684685604
        }
      ],
      "credits": [],
      "debits": [
        {
          "id": 1,
          "amount": 5000,
          "source_bank_account_id": 1,
          "destination_bank_account_id": 2,
          "created_at": 1684686009
        }
      ],
      "mab": 3500,
      "transactions_count": 3
    },
    "bank_account_id": 1,
    "created_at": 1684686207
  }
]
```

---

Thanks

Happy coding
