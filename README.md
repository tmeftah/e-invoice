# e-invoice

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/709aac6159724d5195e2120d67b6279d)](https://app.codacy.com/app/tmeftah/e-invoice?utm_source=github.com&utm_medium=referral&utm_content=tmeftah/e-invoice&utm_campaign=Badge_Grade_Settings)&nbsp;&nbsp;&nbsp;[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/0cc998c220f948068232af96efd3741b)](https://www.codacy.com/app/tmeftah/e-invoice?utm_source=github.com&utm_medium=referral&utm_content=tmeftah/e-invoice&utm_campaign=Badge_Coverage)

e-invoice for small business based on flask, jwt and vuejs.

## Flask-app (backend)

### Terminal commands

```
Befor being able to run the app please be sure that you have install python2 and pip on your computer.

Initial installation: pip install requirements.txt
When using virtualenv activate it bevor executing the command above.

after downloading all the dependencies it's time to run the app
- run the application: python manage.py run or python
- run test: python app\test\name_of_test.py
```

### Using Postman

```
Default url of app is: http://127.0.0.1:5000
for the first use you should register at least one user following:
URL: 			http://127.0.0.1:5000/registration
Methode: 		Post
Body Form-data(Keys): 	username,password

after successfully registered go to login
URL: 			http://127.0.0.1:5000/login
Methode: 		Post
Body Form-data(Keys): 	username,password
as a responce you get 2 token.

Each Request must have the session-token on authorization.
Example:
get product list:
URL: 			http://127.0.0.1:5000/product/
Methode: 		Get
Key: Authorization
Value: "Bearer session_token_generated_during_login"
```

### Todo

- [ ] vuejs client
- [ ] add additional tables to database (products/custumers/invoices/settings , etc..)
- [ ] set new tests
- [ ] connect the repo to one online coverage provider

### Debug on vscode

- Settings (launch.js):
  select on the debbuging module flask (or add a new configuration)


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

### Contributing

If you want to contribute to this flask e-invoice app, clone the repository and just start making pull requests.

```
https://github.com/tmeftah/e-invoice.git
```
