# Mile-Tracker README

## CURRENT STATUS

Currently deployed and functional.
Working on improving mile tracking features and styling.

.
07/14/2026

MAJOR:
    -Fixed Internal Server Error! *!YAY!*
        -Bad url end point for url build (miles-tracker -> miles_tracker)
    -Added filtering functionality to mile tracker to sort through a selected activity
    -Refactored html for template inheritence
    -Basic CSS styling

MINOR:
    -Minor bug fixes
    -Deleted 'history.html'
        -combined history with mile-tracker page, it feels cleaner

TO DO:
    -Display filered results
    -Logout feature
    -Add feature that gives a random uploaded photo from uploaded photos
    -Add gallery of all uploaded photos
    -Tidy up html pages
    -Further CSS styling

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

    MAJOR:
    -Fix Internal Server Error after login
    
    MINOR:
    -Logout feature
    -Refactor for template inheritence
    -Add feature that gives a random uploaded photo from uploaded photos
    -Add gallery of all uploaded photos
    -Tidy up html pages
    -CSS

.
07/12/2026

INITIAL SETUP:
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
