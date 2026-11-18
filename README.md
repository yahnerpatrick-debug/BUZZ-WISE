# BUZZ-WISE

BUZZ-WISE is a personal blood alcohol (BAC) estimator for people 21 and older. You pick the bar or restaurant you're at, log what you drink, and the site estimates your BAC over the night. It shows how it goes up with each drink and back down over time.

## Live website

**👉 [BUZZ-WISE Website](https://buzz-wise-f6yq8cuvu-billee1.vercel.app/)**

> **Important:** BUZZ-WISE gives an *estimate*, not a measurement. Food, medication, metabolism and many other things change your real BAC. Never use this number to decide whether you can drive.

---

## Table of contents

1. [What the app does](#what-the-app-does)
2. [Project files](#project-files)
3. [How a page loads (the big picture)](#how-a-page-loads-the-big-picture)
4. [What Flask is](#what-flask-is)
5. [requirements.txt](#requirementstxt)
6. [app.py: the main Flask file](#apppy-the-main-flask-file)
7. [calculator.py: the BAC math](#calculatorpy-the-bac-math)
8. [profiles.py: user profiles](#profilespy-user-profiles)
9. [restaurants.py and drink_menu.py: places and menus](#restaurantspy-and-drink_menupy-places-and-menus)
10. [pages.py: how the pages are organized](#pagespy-how-the-pages-are-organized)
11. [bee.png and .gitignore](#beepng-and-gitignore)
12. [Coding style and format](#coding-style-and-format)
13. [How to deploy](#how-to-deploy)
14. [References](#references)

---

## What the app does

The site walks the user through four screens, in this order:

1. **Age check.** The user uploads a photo of their ID and enters their birthday. If they're under 21, they can't continue. (The photo is not saved anywhere.)
2. **Profile.** The user enters their name, body weight and sex. These are needed for the BAC formula. Returning users only need their name.
3. **Pick a place.** The user chooses the restaurant or bar they're at. Each place has its own drink menu.
4. **Tracker.** The user adds drinks (and how many hours ago they had each one), then presses **Calculate BAC**. The site shows:
   - the estimated BAC inside a honeycomb hexagon that fills up as BAC rises (blue under 0.08, yellow at 0.08+, red at 0.30+)
   - about how long until the BAC is back to 0.000
   - a warning: "only an estimate" under 0.08, "do not drive" at 0.08+, and "get medical help" with overdose symptoms at 0.30+

There's also a **Water / no drink** option. Its hours count as time spent resting, which lowers the BAC by 0.015 per hour.

---

## Project files

| File | What it's for |
|---|---|
| `app.py` | The main file. It creates the website with Flask and decides what happens at each URL. |
| `calculator.py` | All the BAC math: the Widmark formula, how BAC goes down over time, and the warning levels. |
| `profiles.py` | Creates and saves user profiles (weight, sex, last BAC). |
| `restaurants.py` | The list of places and each place's drink menu. |
| `drink_menu.py` | The original drink menu (whiskey, vodka, rum, beer, brandy, malibu). |
| `pages.py` | What every page looks like: the HTML layout, the CSS styling and the four screens. |
| `bee.png` | The BUZZ-WISE bee logo. |
| `requirements.txt` | Tells Vercel which outside libraries to install (just Flask). |
| `.gitignore` | Tells GitHub which junk files to ignore. |
| `README.md` | This file. |

All the files are in the top level of the repo, with no folders. Vercel needs `app.py` at the top level to find the app.

---

## How a page loads (the big picture)

Websites work through **requests** and **responses**:

1. The user's browser sends a **request**, such as "give me the page at `/`" or "here's the form I just filled out, send it to `/calculate`".
2. The server (our Python code on Vercel) runs and builds a **response**. That's usually an HTML page, sometimes an image, and sometimes a **redirect**, which tells the browser to go to a different page.
3. The browser shows the response.

Here is what happens when someone presses **Calculate BAC**:

```
Browser                         app.py                        calculator.py
   |  POST /calculate  ------->  calculate_bac()
   |                                |  calculate(profile, drinks) ----> does the math
   |                                |  <---- new BAC ------------------
   |                                |  saves BAC into the session
   |  <------- redirect to / ------ |
   |  GET /  ----------------------> home()
   |                                |  picks the TRACKER page from pages.py
   |                                |  fills in the BAC number, warnings, menu
   |  <------- finished HTML ------ |
   |  shows the page
```

Every button on the site follows this same pattern. A form sends data with **POST**, Python handles it, and then the browser is redirected back to the home page, which shows the right screen.

---

## What Flask is

**Flask** is a Python library for building websites. On its own, Python doesn't know how to talk to web browsers. Flask handles that part. It:

- listens for requests from browsers
- matches each URL (like `/calculate`) to the Python function that should handle it
- gives that function the data the user sent (form fields, uploaded files)
- sends whatever the function returns back to the browser

Flask is called a **micro framework**. It's small and simple: a whole website can be one Python file. That made it a good fit for this project, because the BAC calculator was already written in Python and Flask let us turn it into a website without switching languages.

Flask also comes with **Jinja**, the template language used in `pages.py` (the `{{ }}` and `{% %}` parts), and with **sessions**, which remember things about each user between pages.

---

## requirements.txt

```
flask==3.1.*
```

Vercel starts from a fresh computer that only has plain Python. `requirements.txt` is the **shopping list** of outside libraries to install before running the site. Anything that comes built into Python (`os`, `sys`, `datetime`) doesn't need to be listed. Only outside libraries do, and Flask is the only one.

**What `flask==3.1.*` means:**
- `flask` is the library's name.
- `==` means "exactly this version".
- `3.1.*` means "version 3.1, any patch number" (3.1.0, 3.1.1, 3.1.3 and so on). The `*` is a wildcard.

**Why pin the version?** Libraries change over time. If Flask 4.0 comes out and changes how something works, an un-pinned site could break the next time Vercel rebuilds it. Pinning to 3.1 keeps it stable. Patch versions (the last number) only contain bug fixes, so allowing any of them is safe.

**Can I edit or delete it?**
- **Edit:** yes. If you ever add another outside library (for example `requests`), add it on a new line.
- **Delete:** no. Without it, Vercel won't install Flask and the site will crash.

---

## app.py: the main Flask file

`app.py` is the **main Flask file**. It creates the website, connects all the other files, and has one function for every URL on the site. Vercel looks for a file named `app.py` with a variable named `app` inside it, so both of those names matter.

### The imports

The imports are at the very top of the file. An **import** brings in code from somewhere else so this file can use it. There are two styles:

- `import os` brings in the whole module. You then use it as `os.something`.
- `from datetime import date` brings in just one piece, so you can write `date` instead of `datetime.date`.

The imports are grouped in three blocks, in the order Python's official style guide (PEP 8) recommends: **built-in Python modules first, outside libraries second, our own files last.**

#### Block 1: built into Python (no install needed)

```python
import os
import sys
from datetime import date
```

| Import | What it is | How we use it |
|---|---|---|
| `os` | "Operating system". It lets Python work with files, folders and settings on the computer it's running on. | `os.path` builds the file path to `bee.png`. `os.environ` reads the `SECRET_KEY` setting from Vercel. |
| `sys` | "System". It controls how Python itself runs. | `sys.path` is the list of folders Python searches when you `import` something. We add our project folder to it. |
| `date` (from `datetime`) | A tool for working with calendar dates. | The 21+ age check: getting today's date and reading the birthday the user typed. |

#### Block 2: the Flask library (installed from requirements.txt)

```python
from flask import Flask, redirect, render_template_string, request, send_file, session, url_for
```

These seven names are all pieces of Flask:

| Import | What it is | How we use it |
|---|---|---|
| `Flask` | The class that creates the website itself. | `app = Flask(__name__)` creates our app. |
| `request` | Everything about the request that just came in. | `request.form` holds form fields the user typed (name, weight, hours). `request.files` holds uploaded files (the ID photo). `request.args` holds values in the URL, which is where error messages go. |
| `session` | A dictionary that **remembers things about one user** from page to page. It's stored in their browser as a cookie. | Stores whether they passed the age check, their profiles, which place they picked, and their list of drinks. |
| `redirect` | A response that tells the browser "go to this other page". | After every form, we redirect back to the home page. |
| `url_for` | Builds the URL for one of our functions, using the function's name. | `url_for('home')` gives `/`. If we ever change a URL, every link still works, because links point at function names instead of typed-out addresses. |
| `render_template_string` | Takes HTML text containing Jinja blanks (`{{ }}` and `{% %}`), fills them in, and returns the finished page. | Builds every page from the text in `pages.py`. It also **auto-escapes** what users type, so if someone puts HTML code in their name, it shows as plain text instead of running. |
| `send_file` | Sends a file instead of a web page. | Sends `bee.png` when the browser asks for the logo. |

#### Block 3: our own files

```python
import pages
from calculator import SYMPTOMS, calculate, format_hours, get_current_bac, get_status, hours_until_zero
from profiles import load_profiles, new_profile, save_profiles, valid_name
from restaurants import RESTAURANTS, WATER, get_menu
```

Any `.py` file can be imported like a library. `import pages` brings in all of `pages.py`, and we use it as `pages.LAYOUT`, `pages.TRACKER` and so on. The `from ... import ...` lines pull out specific functions and variables so we can call them directly, like `calculate(...)` instead of `calculator.calculate(...)`. Each of these is explained in its file's section below.

### The setup lines

```python
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)
```

- `__file__` is a special variable Python sets automatically. It holds the path of the current file (`app.py`).
- `os.path.abspath(...)` turns that into a full path from the root of the computer.
- `os.path.dirname(...)` drops the file name and keeps just the folder.
- So `HERE` is "the folder `app.py` lives in".
- `sys.path.append(HERE)` adds that folder to the places Python searches for imports. This guarantees `import pages`, `from calculator import ...` and the others always work, whichever folder Vercel starts the program from.

These two lines come **before** our own imports on purpose, because those imports need the folder to be searchable first.

```python
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')
```

- `Flask(__name__)` creates the website. `__name__` is another automatic variable holding the current module's name. Flask uses it to know where the app lives.
- `app.secret_key` is used to **sign** the session cookie. Users can't change their own cookie (for example, to skip the age check or lower their BAC), because any change breaks the signature and Flask throws the cookie away.
- `os.environ.get('SECRET_KEY', 'dev-key')` means "read the setting called `SECRET_KEY` from Vercel, and if it doesn't exist, use `'dev-key'`". The real key is stored in Vercel's settings, **not** in the code, because the code is on GitHub where anyone could read it.

### Helper functions

These are small functions the routes use over and over.

```python
def show(page, **info):
    info['error'] = request.args.get('error')
    info['message'] = session.pop('message', None)
    html = pages.LAYOUT.replace('{{ page }}', page)
    return render_template_string(html, **info)
```

`show()` builds a full page.
- `**info` collects any number of **keyword arguments** into a dictionary. So `show(pages.TRACKER, name=name, bac=bac)` gives `info = {'name': ..., 'bac': ...}`.
- It adds any error message from the URL, and any one-time message from the session. `.pop()` reads a value and deletes it in the same step, so "Welcome back!" only shows once.
- `pages.LAYOUT.replace('{{ page }}', page)` slots one screen (like the tracker) into the shared layout (header, footer, styling).
- `render_template_string(html, **info)` fills in all the blanks. The `**` here does the reverse: it spreads the dictionary back out into keyword arguments.

```python
def go_home(error=None):
    if error:
        return redirect(url_for('home', error=error))
    return redirect(url_for('home'))
```

`go_home()` sends the browser back to the home page. If there's an error, it's attached to the URL (for example `/?error=Pick+a+drink+from+the+menu.`), and `show()` picks it up from there. `error=None` is a **default argument**: if you call `go_home()` with nothing, `error` is `None`.

```python
def get_age(birthday):
    today = date.today()
    had_birthday = (today.month, today.day) >= (birthday.month, birthday.day)
    return today.year - birthday.year - (0 if had_birthday else 1)
```

`get_age()` works out how old someone is. It compares **tuples** (month, day). Python compares tuples item by item, so `(3, 15) >= (3, 10)` is `True`. If their birthday hasn't happened yet this year, it subtracts 1. `(0 if had_birthday else 1)` is a **one-line if/else** (called a conditional expression).

### Routes: one function per URL

A **route** connects a URL to a function. The `@` line above each function is a **decorator**. It wraps the function and registers it with Flask.

- `@app.get('/...')` handles **GET** requests: *viewing* a page (opening a link or loading the site).
- `@app.post('/...')` handles **POST** requests: *sending data* (submitting a form or pressing a button that changes something).

| Route | Type | Function | What it does |
|---|---|---|---|
| `/` | GET | `home()` | Decides which screen to show: age check, then profile, then place, then tracker. |
| `/bee.png` | GET | `bee_image()` | Sends the bee logo image. |
| `/verify` | POST | `verify()` | Checks that a photo was uploaded and the user is 21 or older. |
| `/profile` | POST | `profile()` | Creates a new profile, or welcomes back an existing one. |
| `/place/<place_id>` | POST | `pick_place()` | Saves which restaurant the user picked. |
| `/place/change` | GET | `change_place()` | Clears the restaurant so the user can pick again. |
| `/drinks/add` | POST | `add_drink()` | Adds a drink (or water) to the list. |
| `/drinks/remove/<int:index>` | POST | `remove_drink()` | Removes one drink from the list. |
| `/calculate` | POST | `calculate_bac()` | Runs the BAC math and saves the result. |
| `/switch` | GET | `switch_person()` | Goes back to the name screen. |

**URL variables:** in `/place/<place_id>`, the part in `< >` changes. Visiting `/place/blue-hive-lounge` calls `pick_place(place_id='blue-hive-lounge')`. In `/drinks/remove/<int:index>`, the `int:` part makes Flask check that the value is a whole number before calling the function.

**How `home()` picks a screen:** it's a chain of checks, and each one returns early if something is missing:

```python
if not session.get('verified'):        # no age check yet
    return show(pages.VERIFY)
...
if name not in profiles:               # no profile yet
    return show(pages.PROFILE, ...)
...
if place_id not in RESTAURANTS:        # no place picked yet
    return show(pages.PLACES, ...)
...
return show(pages.TRACKER, ...)        # everything's ready
```

This is called the **early return** pattern. It avoids deeply nested `if` statements.

**Handling bad input:** the routes never trust what users type. For example, `add_drink()`:
- checks that the drink is actually on the menu (`drink not in menu`)
- uses `try` / `except ValueError` in case someone types letters into the hours box (`float('abc')` raises a `ValueError`)
- rejects negative hours

If anything's wrong, it calls `go_home('...error message...')` so the user sees what to fix.

### Running it on your own computer

```python
if __name__ == '__main__':
    app.run(debug=True)
```

When you run `python app.py` yourself, Python sets `__name__` to `'__main__'`, so this starts a test server at `http://127.0.0.1:5000`. Vercel *imports* `app` instead of running the file, so it skips this part. `debug=True` shows detailed error pages and reloads automatically when you save. It should only be used on your own computer, never on the live site.

---

## calculator.py: the BAC math

This file is the original notebook calculator, split into small functions that the website can call (instead of using `input()` and `print()`).

### Import

```python
from datetime import datetime
```

`datetime` holds a date **and** a time (unlike `date`, which is only the day). We need the time to work out how many hours have passed since the last calculation.
- `datetime.now()` is the current moment.
- `.isoformat()` turns a datetime into text like `2026-11-17T21:30:00`, so it can be saved in the session cookie (cookies can only hold text).
- `datetime.fromisoformat(...)` turns that text back into a datetime.
- Subtracting two datetimes gives a time difference. `.total_seconds() / 3600` turns it into hours.

### Constants

```python
BURN_RATE = 0.015
SYMPTOMS = ['Vomiting', 'Seizures', ...]
```

Names in ALL CAPS are **constants**: values that never change while the program runs. 0.015 is the average amount BAC drops per hour. `SYMPTOMS` is the overdose warning list shown at 0.30+.

### Functions

| Function | What it does |
|---|---|
| `get_time_since(profile, now)` | Hours since the last calculation. The first time, it returns `float('inf')`, Python's "infinity", so that every drink counts on the first calculation. |
| `get_current_bac(profile, now)` | Last saved BAC minus `0.015 × hours since`. `max(0, ...)` keeps it from going below zero. |
| `get_drink_bac(ounces, abv_percent, weight, r, hours_ago)` | The **Widmark formula** for one drink (see below). |
| `calculate(profile, drinks, menu, now)` | The main calculation, like one run of the original `main()`. It handles water as rest time, skips drinks already counted earlier, adds up the rest, and saves the new BAC and time to the profile. It returns two values: the new BAC and a list of skipped drinks. |
| `hours_until_zero(bac)` | `bac / 0.015`: about how many hours until BAC is back to 0. |
| `format_hours(hours)` | Turns `2.75` into `"2 h 45 min"`. `divmod(total_minutes, 60)` gives hours and leftover minutes in one step. |
| `get_status(bac)` | Returns `'danger'` (0.30+), `'over'` (0.08+) or `'ok'`. The pages use this to pick the warning and the hexagon color. |

### The formula

```python
pure_alc = ounces * (abv_percent / 100)
drink_bac = (pure_alc * 5.14) / (weight * r)
drink_bac -= 0.015 * hours_ago
```

- `pure_alc` is the ounces of pure alcohol in the drink.
- `5.14` is a conversion factor for using ounces and pounds.
- `r` is the **Widmark factor**, roughly how much of the body's weight the alcohol spreads through: 0.68 for men and 0.55 for women.
- The last line subtracts what the body has burned off since the drink.
- Each drink's result is limited to 0 or more, so a drink that already wore off doesn't subtract from the others.

### The water / rest rule

Logging "Water / no drink" for 2 hours means "I've been resting for 2 hours". That lowers BAC by `0.015 × 2`. To avoid counting the same time twice, it only counts the hours that **haven't already passed** since the last calculation.

### The skip rule

If a drink was had *before* the last calculation (`hours_ago > time_since`), it was already counted, so it's skipped and listed on the page. This matches the original notebook code.

---

## profiles.py: user profiles

**No imports.** This file only works with dictionaries.

```python
R_VALUES = {'male': 0.68, 'female': 0.55}
```

A dictionary that maps each sex to its Widmark `r` value.

| Function | What it does |
|---|---|
| `load_profiles(session)` | `session.get('profiles', {})` returns the saved profiles, or an empty dictionary `{}` if there aren't any yet. |
| `save_profiles(session, profiles)` | Puts the profiles back into the session. |
| `new_profile(weight, sex)` | Builds a profile dictionary: weight, sex, r, `prior_bac` (starts at 0.0) and `last_calculation` (starts as `None`, meaning never). If the sex isn't valid, it uses `raise ValueError(...)` to report an error, which `app.py` catches with `try` / `except`. |
| `valid_name(name)` | `name.replace(' ', '').isalpha()` removes spaces, then checks that only letters are left. |

**Why the session and not a file?** The original notebook saved profiles into `profile_data.ipynb`. Vercel's servers can't save files permanently, so each user's profiles live in their own browser cookie instead. That's also why the session is passed **into** these functions as a parameter: the functions don't need to import Flask, so they stay simple and easy to test.

---

## restaurants.py and drink_menu.py: places and menus

### drink_menu.py

The original drink menu from the notebook, unchanged. It's a **dictionary of dictionaries**: each drink name maps to another dictionary with its ounces and alcohol percentage.

```python
DRINK_MENU = {
    'whiskey': {'ounces': 1.5, 'abv_percent': 50},
    ...
}
```

### restaurants.py

```python
from drink_menu import DRINK_MENU
```

This imports the original menu so Stinger's Sports Grill can reuse it instead of copying it.

`RESTAURANTS` is a dictionary three levels deep:

```
RESTAURANTS
 └── 'blue-hive-lounge'                  ← an ID used in the URL
      ├── 'name': 'Blue Hive Lounge'      ← shown on the page
      ├── 'kind': 'Cocktail bar'
      └── 'menu'
           └── 'margarita'
                ├── 'ounces': 4
                └── 'abv_percent': 20
```

The IDs use dashes and no spaces (`blue-hive-lounge`) because they go in URLs. Cocktail entries use the size and strength of the **whole mixed drink**, not just the shot.

`WATER = 'water / no drink'` is the name used for the water option everywhere, so it's spelled the same in every file.

```python
def get_menu(place_id):
    if place_id not in RESTAURANTS:
        return None
    menu = dict(RESTAURANTS[place_id]['menu'])
    menu[WATER] = {'ounces': 8, 'abv_percent': 0}
    return menu
```

`dict(...)` makes a **copy** of the menu before adding water. Without the copy, water would be added to the original menu in memory, which would change `DRINK_MENU` too.

**To add a real restaurant**, copy one of the blocks, change the ID, name, kind and drinks, and keep the same format.

---

## pages.py: how the pages are organized

`pages.py` holds **what every page looks like**. To keep the whole project in Python, the HTML is stored inside Python strings instead of separate `.html` files.

### Overall structure

The file has five variables, each a **triple-quoted string** (`"""..."""`). Triple quotes let a string run across many lines.

| Variable | What it is |
|---|---|
| `LAYOUT` | The frame shared by every page: the `<head>` (fonts and all the CSS styling), the header with the bee and the BUZZ-WISE name, error and message boxes, and the footer warning. It contains a placeholder, `{{ page }}`, where each screen goes. |
| `VERIFY` | Screen 1: the big bee, the ID photo upload and the birthday box. |
| `PROFILE` | Screen 2: name, weight and sex. |
| `PLACES` | Screen 3: the list of restaurants. |
| `TRACKER` | Screen 4: the hexagon BAC meter, warnings, the add-drink form and the drink list. |

Each time a page loads, `app.py` takes `LAYOUT`, swaps `{{ page }}` for one of the four screens, then fills in the data. This way the header, footer and styling are written **once** and shared by every screen, instead of being copied four times.

### The three languages inside pages.py

`pages.py` is a Python file, but the strings inside it contain three web languages working together:

**1. HTML (structure): *what* is on the page.**
HTML uses **tags** in angle brackets. Most come in pairs: `<h1>Hi</h1>`.
- `<header>`, `<main>` and `<footer>` are the three main areas of every page.
- `<h1>` and `<h2>` are headings, and `<p>` is a paragraph.
- `<form method="post" action="...">` is a form. `method="post"` makes it send a POST request, and `action` is the URL it sends to (which matches a route in `app.py`).
- `<input>`, `<select>` (a dropdown) and `<option>` (one choice in it) are form fields. Their `name="..."` is what `request.form.get('...')` reads in `app.py`.
- `enctype="multipart/form-data"` is needed on the age-check form because it uploads a file.
- `<button>` submits its form.
- `<ul>` and `<li>` make a list.
- `<img src="...">` shows the bee.
- `<svg>` draws shapes with code. It's used for the hexagon meter.
- `class="..."` gives an element a name that the CSS can style.

**2. CSS (styling): how things *look*.**
All the CSS is inside one `<style>` tag in `LAYOUT`. CSS rules have a **selector** (what to style) and **properties** (how):

```css
.error { background: #FBE5E3; color: var(--red); }
```

The CSS is organized from general to specific:
1. **Color variables** in `:root`. Each brand color is defined once, like `--yellow: #F4B63F;`, and reused everywhere as `var(--yellow)`. Changing one line changes the color across the whole site.
2. **Base styles**: the page background, font and text color.
3. **Header and logo**: the white top bar, the bee size, and BUZZ-WISE in two colors.
4. **Text**: headings, paragraphs, and helper classes like `.gray` and `.small`.
5. **Forms and buttons**: boxes, dropdowns, the two-column drink form (`display: grid`), and button styles (`.outline` and `.text-button`).
6. **Messages**: the red `.error` box and the blue `.message` box.
7. **Restaurant list**: each place is a full-width button with a name, type and drink count.
8. **BAC hexagon**: the meter and its smooth fill animation (`transition`).
9. **Warnings**: the left border color changes with the level (blue, yellow, red).
10. **Drink list**: each drink in a row with a Remove link.
11. **Reduced motion**: `@media (prefers-reduced-motion: reduce)` turns off the meter animation for anyone whose device is set to reduce motion.

Fonts come from **Google Fonts** through the `<link>` tags in `<head>`: *Bricolage Grotesque* for headings and *Figtree* for body text.

**3. Jinja (filling in the blanks): what *changes*.**
Jinja is the template language that comes with Flask. `render_template_string` reads it and replaces it with real values before the page is sent.

| Jinja syntax | What it does | Example from our pages |
|---|---|---|
| `{{ ... }}` | Prints a value. | `{{ bac }}` prints the BAC number. |
| `{% if ... %} ... {% endif %}` | Shows a part only if something is true. | The danger warning only shows when `status == 'danger'`. |
| `{% for ... %} ... {% endfor %}` | Repeats a part for each item in a list. | One `<option>` for each drink on the menu. |
| `{% set ... %}` | Makes a variable inside the page. | Picks the hexagon fill color from the status. |
| `\|` (a filter) | Changes a value before printing. | `{{ name\|title }}` capitalizes the name. `{{ names\|join(', ') }}` joins a list with commas. |
| `'%.3f'\|format(bac)` | Formats a number. | Always shows 3 decimal places: `0.065`. |
| `url_for(...)` | Builds a link to a route. | `action="{{ url_for('add_drink') }}"` |
| `loop.index0` | Position in a `for` loop, starting at 0. | Tells Remove which drink to delete. |

### The hexagon meter

The meter is drawn with SVG:
- a `<polygon>` with six corner points makes the hexagon shape
- a `<rect>` (rectangle) is the "liquid". Its height is set by `fill`, which `app.py` works out as `bac / 0.30`, so the hexagon is full at 0.30
- `<clipPath>` cuts the rectangle to the hexagon shape so it doesn't spill outside
- `<text>` shows the number in the middle

### Accessibility details

- `role="alert"` on error and danger messages makes screen readers announce them right away.
- `<label for="...">` connects each label to its input, so tapping the label focuses the box.
- `:focus-visible` outlines show which button is selected when using a keyboard.
- The bee images use `alt=""` because they're decoration, so screen readers skip them.

### Sources the page code is based on

The structure and styling in `pages.py` follow techniques from two references (full citations in [References](#references)):

- **MDN Web Docs: CSS styling basics.** The styling approach comes from here: CSS selectors and classes, color and font properties, spacing with margin and padding, the box model, laying out the drink form with `display: grid`, `transition` for the meter animation, and the `prefers-reduced-motion` media query.
- **Flask Documentation: Quickstart.** The page and route setup is modeled on the patterns here: creating the app with `Flask(__name__)`, the `@app.get` and `@app.post` route decorators, reading form data with `request`, storing data with `session` and a `secret_key`, `redirect` with `url_for`, and rendering HTML with Jinja templates.

---

## bee.png and .gitignore

### bee.png

The BUZZ-WISE logo. Browsers request it at `/bee.png`, and this route in `app.py` sends it:

```python
@app.get('/bee.png')
def bee_image():
    return send_file(os.path.join(HERE, 'bee.png'), mimetype='image/png', max_age=86400)
```

- `os.path.join(HERE, 'bee.png')` builds the full path to the image next to `app.py`.
- `mimetype='image/png'` tells the browser it's a PNG image.
- `max_age=86400` lets the browser keep the image for 86,400 seconds (one day), so it doesn't download it again on every page.

To change the logo, replace `bee.png` with a new image with the same name.

### .gitignore

Lists files GitHub should ignore:
- `__pycache__/` and `*.pyc`: files Python creates automatically to load faster. They're rebuilt every time, so there's no need to upload them.
- `.venv/`: a local Python install folder, if you make one.
- `.env`: a file that sometimes holds secret keys. It should never be uploaded.
- `.vercel/`: Vercel's local settings folder.

---

## Coding style and format

The code follows Python's official style guide, **PEP 8**, plus some common Flask habits.

### Naming conventions

| Style | Used for | Examples |
|---|---|---|
| `snake_case` (lowercase with underscores) | Variables and functions | `current_bac`, `get_drink_bac()`, `time_since` |
| `UPPER_CASE` | Constants that never change | `BURN_RATE`, `DRINK_MENU`, `RESTAURANTS`, `HERE` |
| `PascalCase` (capital first letters) | Classes | `Flask` (from the Flask library) |

Function names start with a **verb** that says what they do: `get_...`, `load_...`, `save_...`, `calculate...`. Variable names describe what they hold: `pure_alc`, `abv_decimal` and `time_since` all come from the original notebook code.

### Layout and formatting

- **4 spaces** of indentation. Python uses indentation to know what's inside an `if`, `for` or function.
- **Two blank lines** between functions.
- **Imports at the top**, grouped as built-in, then outside library, then our files.
- **Single quotes** `'...'` for normal strings, and **triple quotes** `"""..."""` for long multi-line HTML.
- **Short comments** with `#` only where the reason isn't obvious from the code.
- **One job per file**: math in `calculator.py`, pages in `pages.py`, data in `restaurants.py`. This is called **separation of concerns**. It makes each file easier to understand and change.

### Python features used

| Feature | Example | What it means |
|---|---|---|
| f-strings | `f'Welcome back, {name.title()}!'` | Puts variables straight into text. |
| `dict.get(key, default)` | `session.get('drinks', [])` | Gets a value, or a backup if it's missing, instead of crashing. |
| `max(0, x)` | `max(0, current_bac)` | Keeps a number from going below 0. |
| `try` / `except` | `except ValueError:` | Catches errors (like letters typed into a number box) instead of crashing. |
| `raise` | `raise ValueError(...)` | Reports an error so the caller can catch it. |
| Default arguments | `def go_home(error=None):` | The argument is optional. |
| `**kwargs` | `def show(page, **info):` | Accepts any number of named arguments. |
| Returning two values | `return current_bac, skipped` | Returns both at once. The caller writes `bac, skipped = calculate(...)`. |
| `float('inf')` | `return float('inf')` | Infinity, bigger than any number. |
| Conditional expression | `(0 if had_birthday else 1)` | An if/else in one line. |
| Decorators | `@app.post('/calculate')` | Registers the function below as a route. |

---

## How to deploy

1. **GitHub:** upload all the files to the top level of a repository (no folders).
2. **Vercel:** go to **Add New → Project** and import the GitHub repo. Vercel detects Flask automatically, so leave the build settings as they are.
3. **Secret key:** in the project's **Settings → Environment Variables**, add `SECRET_KEY` with a long random value. Never put the real key in the code.
4. **Deploy.** After that, every change committed to GitHub redeploys the site automatically.

To run it on your own computer:

```
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

---

## References

MDN contributors. (n.d.). *CSS styling basics*. MDN Web Docs. Retrieved November 16, 2026, from https://developer.mozilla.org/learn/css

Pallets. (n.d.). *Quickstart*. Flask Documentation (Version 3.1.x). Retrieved November 16, 2026, from https://flask.palletsprojects.com/quickstart/

### Acknowledgments

Built with help from Claude, an AI assistant made by Anthropic, for writing, debugging and explaining the code.
