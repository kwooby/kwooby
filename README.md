# Mile-Tracker README

*This is not the README for my personal website setup! This README is just for the mile-tracker project!

.
07/13/2026

MAJOR:
    -Connected with Render to official domain
    -Added home.html
    -Added basic navigation between home and mile tracker

MINOR:
    -Code cleanup
    -Password fixed
    -Renamed mile-tracker.py to app.py for transparency with framework
    -Removed requirements.txt from gitignore and manually added gunicorn 26.0.0

TO DO:
    -Logout feature
    -Refactor for template inheritence
    -Add feature that gives a random uploaded photo from uploaded photos
    -Add gallery of all uploaded photos
    -Tidy up html pages
    -CSS

.
07/12/2026

START:
-Initial commit
-README and gitignore setup
-Basic git setup
-index.html skeleton setup
    -basic forms
    -basic boilerplate
-flask skeleton setup
    -basic connection
    -sqlite db created
    -requirements.txt created

MAJOR:
    -Making this my website
    -Added password protection (website is WIP, don't want randos once its live)
    -Moved mile tracking logic into separate html file (cleaner)
    -Basic boilerplate in history.html
    -Basic password authetication in index.html
    -Two forms in mile-tracker.html
        -'Run Details' form and 'Photo Upload' form

TO DO:
    -Logout feature
    -Fix password
    -Connect to website
        -Use Render?
    -Refactor for template inheritence
    -Add feature that gives a random uploaded photo from uploaded photos
        -Probably on the same page as mile tracker input
        -Eventually, make it so that if there are no pictures ulpoaded yet this feature does not appear
