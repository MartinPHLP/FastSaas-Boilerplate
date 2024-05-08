# FastSaas Boilerplate
A django solution to accelerate Backend Development for SaaS initiatives

![Illustration](./illustration.jpeg)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Description](#description)
- [License](#license)

## Installation

- Clone the repo
- Create env : `python -m venv env`
- Activate env : `source ./env/bin/activate`
- Install dependencies : `pip install --upgrade pip && pip install -r requirements.txt`
- Create .env file and save your keys in it
- Make migrations with `python manage.py makemigrations`
- Migrate to your database : `python manage.py migrate`

## Usage

`python manage.py runserver`

## Description

The goal is to create a backend template to build a saas as fast as possible. We use django in this project. It includes :

- A core app (head of the project)
- An auth app (google social auth, declaration of a custom user model, creation of new users)
- A user management app (modify users and accounts, delete accounts, etc...)
- A support app ('contact us' part, open tickets, user problems management)
- A billing app (billing part of the saas based on Paypal, manage plans, manage permissions to use services)
- A service app (the service itself, need to custom it by yourself)

The user's connection is ensured by jwt, in core app.
Here is the custom user model:

`email`
`unique_id`
`provider`
`api_access`
`is_staff`
`sub_id`
