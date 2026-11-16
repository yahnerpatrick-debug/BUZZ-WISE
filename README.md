# BUZZ-WISE

Personal blood alcohol (BAC) estimator. Python + Flask, deployed on Vercel.

## Files
- `app.py`: the website (Vercel finds the `app` in here automatically)
- `calculator.py`: BAC math
- `restaurants.py`: the places and each one's drink menu. Add, rename or remove places here.
- `drink_menu.py`: your original drink list (used as Stinger's Sports Grill's menu)
- `bee.py`: the animated bee logo
- `profiles.py`: creating and saving profiles
- `templates.py`: page layout and colors
- `requirements.txt`: tells Vercel to install Flask

## Deploy
1. Upload all of these files to the top level of a GitHub repo (not inside a folder).
2. On Vercel: Add New > Project > import the repo. Leave Framework Preset, Root Directory and the build settings as they are.
3. Under Environment Variables, add `SECRET_KEY` with a long random value, then click Deploy.

BUZZ-WISE gives an estimate, not a measurement. Never use it to decide whether you can drive.
