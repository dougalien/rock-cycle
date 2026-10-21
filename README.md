# The Rock Cycle

An exploration-style guide to the rock cycle for introductory geology students, by Dougalien Systems.

Pages: Welcome, The Big Picture, Rock Gallery (lab sample photos), Take a Journey, Rock Detective and Glossary.

## Run it on your own computer

```
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Photos

`photos/` holds resized lab-sample photos and `photos/thumbs/` the small versions. They are built from the original `Rock Samples` folder (kept on your computer, not in this repo) by `prepare_photos.py`. Rocks without a lab photo use Wikimedia Commons images, credited under each photo in the app.

## Edit the content

All rock text lives in `rock_data.py`.
