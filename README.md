# personal budget tracker

a clean, turnkey budget web app built with flask, sqlite, and vanilla js. tracks your income, expenses, and visualizes where your money is actually going.

## features

* simple dashboard for balance, income, and expenses
* expense breakdown chart using chart.js
* custom categories and transaction history
* persistent backend storage with sqlite
* minimal installer gui to manage flask dependencies

---

## setup & running

### 1. clone or download the repo

make sure your project directory looks like this:

```text
budget_app/
├── app.py
├── req.py
├── static/
│   ├── script.js
│   └── style.css
└── templates/
    └── index.html
```

### 2. install dependencies

you can use the built-in gui installer to manage python packages:

```bash
python req.py
```

* click **check status** to see if flask is already installed
* click **install all** to set up everything automatically
* click **uninstall all** if you ever want to clean up your environment

### 3. start the server

```bash
python app.py
```

the app will automatically create the `budget.db` database file on its first run and launch at `http://127.0.0.1:5000`.

---

## tech stack

* **backend:** python, flask, sqlite3
* **frontend:** html5, css3, vanilla javascript
* **charting:** chart.js via cdn
* **installer:** python tkinter
