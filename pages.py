LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BUZZ-CHECK</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  --light-blue: #8CCBF0;
  --blue: #3E9AD3;
  --background: #EEF7FC;
  --text: #14324B;
  --gray-text: #4F6B82;
  --yellow: #F4B63F;
  --red: #C8352E;
  --line: #D6EAF6;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--background);
  color: var(--text);
  font: 400 1rem/1.55 Figtree, system-ui, sans-serif;
}

header { background: white; border-bottom: 3px solid var(--light-blue); }
.top-bar {
  max-width: 34rem;
  margin: 0 auto;
  padding: 0.5rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.top-bar a { margin-left: auto; color: var(--gray-text); font-size: 0.9rem; }
.small-bee { width: 3.2rem; height: auto; flex: none; }
.logo { font: 800 1.45rem/1 "Bricolage Grotesque", sans-serif; }
.logo span { color: var(--blue); }

main { max-width: 34rem; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }
footer { max-width: 34rem; margin: 0 auto; padding: 0 1.25rem 2rem; color: var(--gray-text); font-size: 0.85rem; }

h1 { font: 800 2rem/1.1 "Bricolage Grotesque", sans-serif; margin: 0 0 0.4rem; }
h2 { font: 600 1.25rem/1.2 "Bricolage Grotesque", sans-serif; margin: 2rem 0 0.6rem; }
p { margin: 0.4rem 0 1rem; max-width: 60ch; }
.gray { color: var(--gray-text); }
.small { font-size: 0.92rem; }

label { display: block; font-weight: 600; margin: 1rem 0 0.3rem; }
input, select {
  width: 100%;
  font: inherit;
  padding: 0.7rem 0.8rem;
  border: 2px solid #C9E3F3;
  border-radius: 0.5rem;
  background: white;
  color: var(--text);
}
input:focus, select:focus, button:focus-visible, a:focus-visible {
  outline: 3px solid var(--yellow);
  outline-offset: 2px;
}
.two-columns { display: grid; grid-template-columns: 1.4fr 1fr; gap: 0.75rem; }
.two-columns label { margin-top: 0; }

button {
  font: 600 1rem Figtree, sans-serif;
  padding: 0.8rem 1.2rem;
  margin-top: 1.1rem;
  border: 2px solid var(--text);
  border-radius: 0.5rem;
  background: var(--text);
  color: white;
  cursor: pointer;
}
button.outline { background: transparent; color: var(--text); }
button.text-button {
  border: 0;
  background: none;
  color: var(--gray-text);
  padding: 0;
  margin: 0;
  font-weight: 400;
  text-decoration: underline;
}

.error { background: #FBE5E3; color: var(--red); padding: 0.7rem 0.9rem; border-radius: 0.5rem; font-weight: 600; }
.message { background: white; border: 2px solid var(--light-blue); padding: 0.7rem 0.9rem; border-radius: 0.5rem; }

.big-bee-box { display: flex; justify-content: center; margin-bottom: 0.75rem; }
.big-bee { width: min(11rem, 50vw); height: auto; }

/* restaurant list */
.places { list-style: none; margin: 1rem 0 0; padding: 0; border-top: 1px solid var(--line); }
.places button {
  all: unset;
  box-sizing: border-box;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.1rem 1rem;
  padding: 1rem 0.25rem;
  border-bottom: 1px solid var(--line);
  cursor: pointer;
}
.places button:focus-visible { outline: 3px solid var(--yellow); outline-offset: -3px; }
.places button:hover .place-name { text-decoration: underline 3px var(--yellow); }
.place-name { font: 600 1.15rem/1.25 "Bricolage Grotesque", sans-serif; }
.place-kind { grid-column: 1; color: var(--gray-text); font-size: 0.92rem; }
.drink-count { grid-row: 1 / 3; grid-column: 2; align-self: center; color: var(--gray-text); font-size: 0.9rem; }

.current-place a { margin-left: 0.5rem; color: var(--gray-text); }

/* BAC hexagon */
.meter { display: grid; place-items: center; margin: 0.5rem 0; }
.meter svg { width: min(15rem, 70vw); }
.meter .number { font: 800 46px "Bricolage Grotesque", sans-serif; fill: var(--text); }
.meter .label { font: 500 15px Figtree, sans-serif; fill: var(--gray-text); }
.meter-fill { transition: y 0.8s ease, height 0.8s ease; }
.time-left { text-align: center; color: var(--gray-text); margin: 0 auto 1.25rem; }
.time-left strong { color: var(--text); white-space: nowrap; }

.warning { padding: 1rem 1.1rem; border-radius: 0.6rem; background: white; border-left: 6px solid var(--light-blue); }
.warning.over { border-color: var(--yellow); }
.warning.danger { border-color: var(--red); background: #FBE5E3; }
.warning strong { display: block; font-size: 1.05rem; }
.warning ul { margin: 0.4rem 0 0.6rem; padding-left: 1.2rem; }
.call { color: var(--red); font-weight: 700; }

.drink-list { list-style: none; padding: 0; margin: 0; }
.drink-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--line);
}

@media (prefers-reduced-motion: reduce) {
  .meter-fill, .small-bee, .big-bee { transition: none; animation: none; }
}
</style>
</head>
<body>
<header>
  <div class="top-bar">
    <img class="small-bee" src="{{ url_for('bee_image') }}" alt="">
    <div class="logo">BUZZ<span>-WISE</span></div>
    {% if session.get('name') %}<a href="{{ url_for('switch_person') }}">Switch person</a>{% endif %}
  </div>
</header>
<main>
{% if error %}<p class="error" role="alert">{{ error }}</p>{% endif %}
{% if message %}<p class="message" role="status">{{ message }}</p>{% endif %}
{{ page }}
</main>
<footer>
  BUZZ-WISE gives an estimate, not a measurement. Food, medication and metabolism all change your real BAC.
  Never use this number to decide whether you can drive.
</footer>
</body>
</html>"""


VERIFY = """
<div class="big-bee-box"><img class="big-bee" src="{{ url_for('bee_image') }}" alt=""></div>
<h1>Check your age</h1>
<p class="gray">Upload a photo of your ID and enter your birthday. You need to be 21 or older.
Your photo isn't saved.</p>
<form method="post" action="{{ url_for('verify') }}" enctype="multipart/form-data">
  <label for="id_photo">Photo of your ID</label>
  <input id="id_photo" type="file" name="id_photo" accept="image/*" required>
  <label for="birthday">Date of birth</label>
  <input id="birthday" type="date" name="birthday" required>
  <button>Verify age</button>
</form>
"""


PROFILE = """
<h1>Who's drinking?</h1>
<p class="gray">Returning? Just enter your name. New here? Add your weight and sex too.
The calculation needs them.</p>
<form method="post" action="{{ url_for('profile') }}">
  <label for="name">Name</label>
  <input id="name" name="name" autocomplete="given-name" required>
  <label for="weight">Body weight (lb)</label>
  <input id="weight" name="weight" type="number" min="80" max="600" step="any">
  <label for="sex">Sex</label>
  <select id="sex" name="sex">
    <option value="male">Male</option>
    <option value="female">Female</option>
  </select>
  <button>Continue</button>
</form>
{% if names %}<p class="gray small">Profiles on this phone: {{ names|join(', ') }}</p>{% endif %}
"""


PLACES = """
<h1>Where are you tonight?</h1>
<p class="gray">Pick the place you're at to see its drink menu.</p>
<ul class="places">
{% for place_id, place in places.items() %}
  <li>
    <form method="post" action="{{ url_for('pick_place', place_id=place_id) }}">
      <button>
        <span class="place-name">{{ place.name }}</span>
        <span class="place-kind">{{ place.kind }}</span>
        <span class="drink-count">{{ place.menu|length }} drinks</span>
      </button>
    </form>
  </li>
{% endfor %}
</ul>
"""


TRACKER = """
<h1>Hi, {{ name|title }}</h1>
<p class="gray small current-place">At {{ place.name }}<a href="{{ url_for('change_place') }}">Change place</a></p>

{% set fill_color = {'ok': '#8CCBF0', 'over': '#F4B63F', 'danger': '#E07A72'}[status] %}
<div class="meter">
  <svg viewBox="0 0 200 230" role="img" aria-label="Estimated BAC {{ '%.3f'|format(bac) }}">
    <defs>
      <clipPath id="hexagon"><polygon points="100,6 194,58 194,172 100,224 6,172 6,58"/></clipPath>
    </defs>
    <polygon points="100,6 194,58 194,172 100,224 6,172 6,58" fill="white"/>
    <rect class="meter-fill" clip-path="url(#hexagon)" x="0" width="200"
          y="{{ 224 - fill * 218 }}" height="{{ fill * 218 + 6 }}" fill="{{ fill_color }}"/>
    <polygon points="100,6 194,58 194,172 100,224 6,172 6,58" fill="none"
             stroke="#14324B" stroke-width="5" stroke-linejoin="round"/>
    <text class="number" x="100" y="124" text-anchor="middle">{{ '%.3f'|format(bac) }}</text>
    <text class="label" x="100" y="150" text-anchor="middle">estimated BAC</text>
  </svg>
</div>

{% if status != 'danger' and bac > 0 %}
<p class="time-left">Your BAC drops about 0.015 an hour.
At that rate you'd be back to 0.000 in about <strong>{{ time_left }}</strong>.</p>
{% elif status != 'danger' and has_calculated %}
<p class="time-left">Your estimated BAC is back to 0.000.</p>
{% endif %}

{% if status == 'danger' %}
<div class="warning danger" role="alert">
  <strong>Your BAC is dangerously high. Stop drinking now.</strong>
  Get medical help right away, especially if you notice any of these:
  <ul>{% for symptom in symptoms %}<li>{{ symptom }}</li>{% endfor %}</ul>
  <a class="call" href="tel:911">Call 911</a>
</div>
{% elif status == 'over' %}
<div class="warning over">
  <strong>You're at or above 0.08. Do not drive.</strong>
  Call 911 if any of these show up:
  <ul>{% for symptom in symptoms %}<li>{{ symptom }}</li>{% endfor %}</ul>
  <a class="call" href="tel:911">Call 911</a>
</div>
{% else %}
<div class="warning"><strong>This is only an estimate.</strong> Don't assume you're safe to drive.</div>
{% endif %}

{% if skipped %}
<p class="gray small">Not added again (you had it before your last calculation): {{ skipped|join(', ') }}.</p>
{% endif %}

<h2>Add drinks</h2>
<form method="post" action="{{ url_for('add_drink') }}">
  <div class="two-columns">
    <div>
      <label for="drink">Drink</label>
      <select id="drink" name="drink">
      {% for drink, info in menu.items() %}
        {% if drink == water %}
        <option value="{{ drink }}">Water / no drink</option>
        {% else %}
        <option value="{{ drink }}">{{ drink|title }} ({{ info.ounces }} oz, {{ info.abv_percent }}%)</option>
        {% endif %}
      {% endfor %}
      </select>
    </div>
    <div>
      <label for="hours">Hours</label>
      <input id="hours" name="hours" type="number" min="0" step="0.25" value="0">
    </div>
  </div>
  <p class="gray small">For a drink, how long ago you had it (0 means just now).
  For water / no drink, how long you've been resting. 1.25 means 1 hour 15 minutes.</p>
  <button class="outline">Add to list</button>
</form>

{% if drinks %}
<ul class="drink-list">
{% for drink in drinks %}
  <li>
    {% if drink.name == water %}
    <span>Water / no drink, resting {{ drink.hours_ago }} h</span>
    {% else %}
    <span>{{ drink.name|title }}, {{ drink.hours_ago }} h ago</span>
    {% endif %}
    <form method="post" action="{{ url_for('remove_drink', index=loop.index0) }}">
      <button class="text-button">Remove</button>
    </form>
  </li>
{% endfor %}
</ul>
<form method="post" action="{{ url_for('calculate_bac') }}"><button>Calculate BAC</button></form>
{% endif %}
"""
