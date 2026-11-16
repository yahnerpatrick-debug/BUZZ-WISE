"""HTML for each page, kept as Python strings so the whole app is Python files."""

from bee import BEE_CSS, bee_svg

LAYOUT = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BUZZ-WISE</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --sky:#8CCBF0; --sky-deep:#3E9AD3; --ice:#EEF7FC; --white:#fff;
  --ink:#14324B; --ink-soft:#4F6B82; --honey:#F4B63F; --red:#C8352E; --line:#D6EAF6;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ice);color:var(--ink);
  font:400 1rem/1.55 Figtree,system-ui,sans-serif}
header{background:var(--white);border-bottom:3px solid var(--sky)}
.bar{max-width:34rem;margin:0 auto;padding:.5rem 1.25rem;display:flex;align-items:center;gap:.5rem}
.bee-sm{width:2.8rem;height:auto;flex:none}
.word{font:800 1.45rem/1 "Bricolage Grotesque",sans-serif;letter-spacing:-.01em}
.word span{color:var(--sky-deep)}
.bar a{margin-left:auto;color:var(--ink-soft);font-size:.9rem}
main{max-width:34rem;margin:0 auto;padding:1.5rem 1.25rem 3rem}
h1{font:800 2rem/1.1 "Bricolage Grotesque",sans-serif;margin:0 0 .4rem}
h2{font:600 1.25rem/1.2 "Bricolage Grotesque",sans-serif;margin:2rem 0 .6rem}
p{margin:.4rem 0 1rem;max-width:60ch}
.lede{color:var(--ink-soft)}
label{display:block;font-weight:600;margin:1rem 0 .3rem}
input,select{width:100%;font:inherit;padding:.7rem .8rem;border:2px solid #C9E3F3;
  border-radius:.5rem;background:var(--white);color:var(--ink)}
input:focus,select:focus,button:focus-visible,a:focus-visible{outline:3px solid var(--honey);outline-offset:2px}
.row{display:grid;grid-template-columns:1.4fr 1fr;gap:.75rem}
.row label{margin-top:0}
button{font:600 1rem Figtree,sans-serif;padding:.8rem 1.2rem;border-radius:.5rem;cursor:pointer;
  border:2px solid var(--ink);background:var(--ink);color:var(--white);margin-top:1.1rem}
button.quiet{background:transparent;color:var(--ink)}
button.link{border:0;background:none;color:var(--ink-soft);padding:0;margin:0;text-decoration:underline;font-weight:400}
.err{background:#FBE5E3;color:var(--red);padding:.7rem .9rem;border-radius:.5rem;font-weight:600}
.flash{background:var(--white);border:2px solid var(--sky);padding:.7rem .9rem;border-radius:.5rem}

/* hero bee on the first screens */
.hero{display:flex;justify-content:center;margin:-.5rem 0 .5rem}
.bee-lg{width:min(8.5rem,40vw);height:auto}

/* restaurant picker */
.places{list-style:none;margin:1rem 0 0;padding:0;border-top:1px solid var(--line)}
.places button{all:unset;box-sizing:border-box;display:grid;grid-template-columns:1fr auto;gap:.1rem 1rem;
  width:100%;padding:1rem .25rem;border-bottom:1px solid var(--line);cursor:pointer}
.places button:focus-visible{outline:3px solid var(--honey);outline-offset:-3px}
.places button:hover .pname{text-decoration:underline;text-decoration-color:var(--honey);text-decoration-thickness:3px}
.pname{font:600 1.15rem/1.25 "Bricolage Grotesque",sans-serif}
.pkind{color:var(--ink-soft);font-size:.92rem;grid-column:1}
.pcount{grid-row:1/3;grid-column:2;align-self:center;color:var(--ink-soft);font-size:.9rem}

.where{display:flex;gap:.6rem;align-items:baseline;flex-wrap:wrap;margin:0 0 .25rem}
.where a{color:var(--ink-soft);font-size:.9rem}

/* the honeycomb meter */
.meter{display:grid;place-items:center;margin:.5rem 0 .5rem}
.meter svg{width:min(15rem,70vw)}
.meter .num{font:800 46px "Bricolage Grotesque",sans-serif;fill:var(--ink)}
.meter .unit{font:500 15px Figtree,sans-serif;fill:var(--ink-soft)}
.fill{transition:y .8s ease,height .8s ease}
.countdown{text-align:center;color:var(--ink-soft);margin:0 auto 1.25rem}
.countdown strong{color:var(--ink);white-space:nowrap}

.note{padding:1rem 1.1rem;border-radius:.6rem;background:var(--white);border-left:6px solid var(--sky)}
.note.over{border-color:var(--honey)}
.note.danger{border-color:var(--red);background:#FBE5E3}
.note strong{display:block;font-size:1.05rem}
.note ul{margin:.4rem 0 .6rem;padding-left:1.2rem}
.call{color:var(--red);font-weight:700}

.rest{display:flex;gap:1rem;align-items:center;background:var(--white);border-radius:.6rem;
  padding:1rem 1.1rem;margin-top:1rem;border:2px dashed var(--sky)}
.rest p{margin:0;font-size:.95rem}
.rest button{margin:0;flex:none;white-space:nowrap;background:var(--sky);border-color:var(--sky);color:var(--ink)}

.round{list-style:none;padding:0;margin:0}
.round li{display:flex;justify-content:space-between;align-items:center;padding:.6rem 0;border-bottom:1px solid var(--line)}
.muted{color:var(--ink-soft);font-size:.92rem}
footer{max-width:34rem;margin:0 auto;padding:0 1.25rem 2rem;color:var(--ink-soft);font-size:.85rem}
@media (prefers-reduced-motion:reduce){.fill{transition:none}}
""" + BEE_CSS + """
</style></head><body>
<header><div class="bar">""" + bee_svg('hdr', 'bee bee-sm') + """<div class="word">BUZZ<span>-WISE</span></div>
{% if session.get('current') %}<a href="{{ url_for('switch') }}">Switch person</a>{% endif %}
</div></header>
<main>
{% if error %}<p class="err" role="alert">{{ error }}</p>{% endif %}
{% if flash %}<p class="flash" role="status">{{ flash }}</p>{% endif %}
__BODY__
</main>
<footer>BUZZ-WISE gives an estimate, not a measurement. Food, medication and metabolism all change your real BAC.
Never use this number to decide whether you can drive.</footer>
</body></html>"""

HERO = '<div class="hero">' + bee_svg('hero', 'bee bee-lg') + '</div>'

VERIFY = HERO + """
<h1>Check your age</h1>
<p class="lede">Upload a photo of your ID and enter your birthday. You need to be 21 or older.
Your photo isn't saved.</p>
<form method="post" action="{{ url_for('verify') }}" enctype="multipart/form-data">
  <label for="id_photo">Photo of your ID</label>
  <input id="id_photo" type="file" name="id_photo" accept="image/*" required>
  <label for="dob">Date of birth</label>
  <input id="dob" type="date" name="dob" required>
  <button>Verify age</button>
</form>
"""

PROFILE = """
<h1>Who's drinking?</h1>
<p class="lede">Returning? Just enter your name. New here? Add your weight and sex too.
The calculation needs them.</p>
<form method="post" action="{{ url_for('profile') }}">
  <label for="name">Name</label>
  <input id="name" name="name" autocomplete="given-name" required>
  <label for="weight">Body weight (lb)</label>
  <input id="weight" name="weight" type="number" min="80" max="600" step="any">
  <label for="sex">Sex</label>
  <select id="sex" name="sex"><option value="male">Male</option><option value="female">Female</option></select>
  <button>Continue</button>
</form>
{% if names %}<p class="muted">Profiles on this phone: {{ names|join(', ') }}</p>{% endif %}
"""

PLACES = """
<h1>Where are you tonight?</h1>
<p class="lede">Pick the place you're at to see its drink menu.</p>
<ul class="places">
{% for pid, p in places.items() %}
  <li><form method="post" action="{{ url_for('choose_place', pid=pid) }}">
    <button>
      <span class="pname">{{ p.name }}</span>
      <span class="pkind">{{ p.kind }}</span>
      <span class="pcount">{{ p.menu|length }} drinks</span>
    </button>
  </form></li>
{% endfor %}
</ul>
"""

METER = """
<div class="where"><h1>Hi, {{ name|title }}</h1></div>
<p class="where muted">At {{ place.name }} <a href="{{ url_for('change_place') }}">Change place</a></p>

<div class="meter">
<svg viewBox="0 0 200 230" role="img" aria-label="Estimated BAC {{ '%.3f'|format(bac) }}">
  <defs><clipPath id="hex"><polygon points="100,6 194,58 194,172 100,224 6,172 6,58"/></clipPath></defs>
  <polygon points="100,6 194,58 194,172 100,224 6,172 6,58" fill="#fff"/>
  <rect class="fill" clip-path="url(#hex)" x="0" y="{{ 224 - level * 218 }}" width="200" height="{{ level * 218 + 6 }}"
        fill="{{ {'estimate':'#8CCBF0','over':'#F4B63F','danger':'#E07A72'}[state] }}"/>
  <polygon points="100,6 194,58 194,172 100,224 6,172 6,58" fill="none" stroke="#14324B" stroke-width="5" stroke-linejoin="round"/>
  <text class="num" x="100" y="124" text-anchor="middle">{{ '%.3f'|format(bac) }}</text>
  <text class="unit" x="100" y="150" text-anchor="middle">estimated BAC</text>
</svg>
</div>
{% if state == 'danger' %}
{% elif bac > 0 %}
<p class="countdown">Your BAC drops about 0.015 an hour.
At that rate you'd be back to 0.000 in about <strong>{{ to_zero }}</strong>.</p>
{% elif last %}
<p class="countdown">Your estimated BAC is back to 0.000.</p>
{% endif %}

{% if state == 'danger' %}
<div class="note danger" role="alert">
  <strong>Your BAC is dangerously high. Stop drinking now.</strong>
  Get medical help right away, especially if you notice any of these:
  <ul>{% for s in symptoms %}<li>{{ s }}</li>{% endfor %}</ul>
  <a class="call" href="tel:911">Call 911</a>
</div>
{% elif state == 'over' %}
<div class="note over">
  <strong>You're at or above 0.08. Do not drive.</strong>
  Call 911 if any of these show up:
  <ul>{% for s in symptoms %}<li>{{ s }}</li>{% endfor %}</ul>
  <a class="call" href="tel:911">Call 911</a>
</div>
{% else %}
<div class="note"><strong>This is only an estimate.</strong> Don't assume you're safe to drive.</div>
{% endif %}

{% if last %}
<div class="rest">
  <p>Taking a break? Log water or no drink and see how far your BAC has dropped.</p>
  <form method="post" action="{{ url_for('rest') }}"><button>Log a break</button></form>
</div>
{% endif %}

{% if skipped %}<p class="muted">Not added again (you had it before your last calculation): {{ skipped|join(', ') }}.</p>{% endif %}

<h2>Add drinks</h2>
<form method="post" action="{{ url_for('add_to_round') }}">
  <div class="row">
    <div><label for="drink">Drink</label>
      <select id="drink" name="drink">{% for d, info in menu.items() %}
        <option value="{{ d }}">{% if info.abv_percent == 0 %}Water / no drink{% else %}{{ d|title }} ({{ info.ounces }} oz, {{ info.abv_percent }}%){% endif %}</option>{% endfor %}
      </select></div>
    <div><label for="hours_ago">Hours ago</label>
      <input id="hours_ago" name="hours_ago" type="number" min="0" step="0.25" value="0"></div>
  </div>
  <p class="muted">1.25 means 1 hour 15 minutes ago. 0 means just now.</p>
  <button class="quiet">Add to list</button>
</form>

{% if round %}
<ul class="round">{% for d in round %}
  <li><span>{{ 'Water / no drink' if d.name == water_name else d.name|title }}, {{ d.hours_ago }} h ago</span>
    <form method="post" action="{{ url_for('remove_from_round', i=loop.index0) }}"><button class="link">Remove</button></form></li>
{% endfor %}</ul>
<form method="post" action="{{ url_for('calculate_bac') }}"><button>Calculate BAC</button></form>
{% endif %}
"""
