# Mile-Tracker and Website Development - DEVNOTES

## CURRENT STATUS

Currently deployed and functional.
Working on improving features and styling.

## Debug Notes

*****TURN DEBUG OFF BEFORE DEPLOYING*****

.
07/26/2029

MAJOR:
    -Added 'settings.html'
        -Route and basic authentication added
        -Basic HTML setup

MINOR:
    -Gallery pagination buttons implemented
    -Dashboard CSS feels better now
        -Centered, flow is better
    -Changed wording for several labels
    -Display user on dashboard now appears with capitalization

    -Users not saving bug seems to be fixed now
        -Leaving debug-users page for now to continue to monitor the issue but
        so far so good

    -Register page has been styled in the most basic sense
    -Renamed "/register" to "/register-user" for clarity
    -Changed gallery to hold six photos per page instead of nine

TO DO:
    HIGH PRIORITY:
        -Change date format: DD/MM/YY instead of (YYYY-DD-MM)
        -Finish setting up the settings page
            -still need to create 'delete_account' function
        -Create a demo page with items filled out already so that employers can look
        around without having to create an account
            -Make it read-only
            -If anyone wants to actively use the tracker or any other apps, they must make an account

    MINOR:
        -Add delete feature for photos
            -Need to figure out where to implement this so it's not annoying
        -Add feature that gives a random uploaded photo from uploaded photos (this
        is very last thing to be doing after everything else works well)
        -Tidy up html pages
        -Continued CSS styling

NOTES:
    -Keeping 'debug-users' until I can confirm the users and DB are functional

.
07/24/2026

MAJOR:
    -Migrated from SQLite to POSTGRES (good lord)
        -Created users were not saving in SQLite DB so users not created locally
        were lost
        -DB is now on POSTGRES through render
        -Basic plan + 5gb storage to mess around (lower storage if needed in
            the future)
    -Cloudinary is now in use for photo cloud storage
        -Stored in local machine before, resulted in inability to see any photos
        -Would appear as broken links
        -Dependency added and debugged
        -Cloudinary account is linked through github
        -Enviroment variables added
        -Should stay persistent across redeploys

MINOR:
    -Moved original miles.db and clean-miles.db into backups folder
        -Keeping for emergencies, in case we need the original DB
        -Both are included in .gitignore

TO DO:
    -Style the register page, still looks sad
    -Finish adding pagination buttons to gallery
        -Started this, but database migration and cloudinary addition took
        up a lot of time
    -On miles-tracker dashboard, capitalize first letter of username
    -Add feature that gives a random uploaded photo from uploaded photos (this
    is very last thing to be doing after everything else works well)
    -Tidy up html pages
    -Continued CSS styling

.
07/23/2026

MAJOR:
    -Changed entire authentication system
    -Added user and password creation
        -Users will now need to create an account to log into and use the site
        -Added register page
        -Index.html is now the default login page
    -Added JavaScript page to facilitate added eventListeners
        -Added eventListener verification for delete entry
        -Added eventListener to show password when inputting password

MINOR:
    -stylesheet cleanup
    -Minor bug fixes
    -Added script to base.html
    -DB schema should be solid, no need to add anymore columns or tables for this
    particular app
    -Logout feature is officially implemented
    -All history page now has filters (activity and year)

TO DO:
    -Omg please style the register page next time you open this, it looks so sad
    -Finish adding pagination buttons to gallery
    -On miles-tracker dashboard, capitalize first letter of username
    -Add feature that gives a random uploaded photo from uploaded photos
        -Could also do a random Toast feature with pictures of Toasty :D
    -Tidy up html pages
    -Continued CSS styling

.
07/20/2026

MAJOR:
    -Added a monthly total miles feature
        -Can be sorted by year
        -Stores the total of all logged miles for all months miles have been logged
        -Should only show years where miles were logged
    -Photos in personal gallery show only for the user that uploaded them
        -Previously, all photos were showing on all user accounts

MINOR:
    -Basic mobile layout fix
        -Items no longer stack on top of each other
        -Gallery changed to 2fr for mobile instead of 3fr
    -Minor CSS styling
    -HTML for gallery pagination started, but not finished
        -Got distracted by the monthly total feature

TO DO:
    -Logout feature (select different user)
        -Logic is implemented, still need HTML and styling
    -Finish adding pagination buttons to gallery
    -Add feature that gives a random uploaded photo from uploaded photos
        -Could also do a random Toast feature with pictures of Toasty :D
    -Tidy up html pages
    -Continued CSS styling

.
07/17/2026

MAJOR:
    -Gallery feature officially implemented!!!
        -Gave grid layout, 9 photos per page
        -Still need to add pagination buttons to gallery
    -History of all runs page added
        -This is separate from the small history of runs on the dashboard

MINOR:
    -Total miles added
    -Filter by activity works
    -Logout feature logic implemented
        -No HTML or CSS for this yet, only Python logic
    -Pagination logic added
        -Previous and Next buttons implemented on small history page
        -Made it 5 items per page
        -NO PAGINATION ON ALL HISTORY!!!
    -Organized CSS
        -History displays nicely now
        -Single column for each log
    -Python logic refactoring
        -Moved helper functions to flow better
        -Split get_runs from mile_tracker for a better logic flow

TO DO:
    -Pictures from all users appear on personal gallery!
        -For the Toast random photo, this is okay, but for individually uploaded photos it must
        only show photos uploaded by selected user
        -This is already implemented in the activity tracker, just need to add it to the gallery
    -Logout feature (select different user)
        -Logic is implemented, still need HTML and styling
    -Add pagination buttons to gallery
    -Add feature that gives a random uploaded photo from uploaded photos
        -Could also do a random Toast feature with pictures of Toasty :D
    -Tidy up html pages
    -Continued CSS styling
    -Mobile looks horrendous omg please fix soon

.
07/16/2026

MAJOR:
    -Added user selection to mile-tracker
        -Currently there are only two users (myself and Katie), there is no need to have
        more than those options right now just to simplify debugging right now
    - Fixed: Flask changes were not appearing and imports were failing
        -Confusion between Python interpreter environments and Flask's running server,
        plus a broken/mismatched virtual environment
        -Identified the correct environment, separated Flask server debugging from Python
        shell usage, verified that python, pip, and VS Code all point to the same interpreter

MINOR:
    -Basic logic cleanup
    -Added delete feature to history of runs
        -Users can now delete their own individual logged activities in the history

TO DO:
    -Filter does not actually display filtered runs/walks
    -Logout feature (select different user)
    -Add feature that gives a random uploaded photo from uploaded photos
    -Add gallery of all uploaded photos
    -Tidy up html pages
    -Further CSS styling
        -Fix 'runs-history' table, make display cleaner
        -I want the delete button to also be on the same row as the activity (more of a UI thing)
    -Add total miles to history of runs

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
