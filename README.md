# e-invoice

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/709aac6159724d5195e2120d67b6279d)](https://app.codacy.com/app/tmeftah/e-invoice?utm_source=github.com&utm_medium=referral&utm_content=tmeftah/e-invoice&utm_campaign=Badge_Grade_Settings)   [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/0cc998c220f948068232af96efd3741b)](https://www.codacy.com/app/tmeftah/e-invoice?utm_source=github.com&utm_medium=referral&utm_content=tmeftah/e-invoice&utm_campaign=Badge_Coverage)

e-invoice for small business based on flask, jwt and vuejs.

## Flask-app (backend)

### Terminal commands

Befor being able to run the app please be sure that you have install python2 and pip on your computer and then install dependencies.
When using virtualenv activate it bevor executing this command.

```python
pip install requirements.txt

```

After downloading all the dependencies it's time to run the application

```python
python manage.py run
```

you should see `Running on http://127.0.0.1:5000/`
Now the backend is working correctly use an API development environment of your choise. I prefer Postman.

### Using Postman

for the first use you should register at least one user following:

```txt
URL: http://127.0.0.1:5000/registration
Methode: Post
Body Form-data(Keys): username,password
```

after successfully registered go to login

```txt
URL:    http://127.0.0.1:5000/login
Methode:   Post
Body Form-data(Keys): username,password
as a responce you get 2 token.
```

Each new request must have the session-token on authorization.

-   product list  

```txt
URL:  http://127.0.0.1:5000/product/
Methode: Get
Key: Authorization
Value: "Bearer session_token_generated_during_login"
```

### Debug on vscode

-   Settings (launch.js): select on the debbuging module flask (or add a new configuration)

```javascript
       {
         "name": "Python: Flask",
         "type": "python",
         "request": "launch",
         "module": "flask",
         "env": {
                   "FLASK_APP": "app\\run.py"
                },
         "args": [
                   "run",
                   "--no-debugger",
                   "--no-reload"
                 ],
         "jinja": false
       }
```

### Todo

-   [ ] vuejs client
-   [ ] add additional tables to database (products/custumers/invoices/settings , etc..)
-   [ ] set new tests
-   [ ] connect the repo to one online coverage provider

### Contributing

If you want to contribute to this flask e-invoice app, clone the repository and just start making pull requests.

```txt
https://github.com/tmeftah/e-invoice.git
```
