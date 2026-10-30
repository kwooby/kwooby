# Mile-Tracker - DEVNOTES

*****TURN DEBUG OFF BEFORE DEPLOYING*****

## CURRENT STATUS

Current State: IN RE-PRODUCTION
    - Full redesign in progress
    - This is a temporary development enviroment I am using to refactor and redesign my mile-tracker web app!
    - I told you I'd be back after i was done with the Hub c:< and I have so much more KNOWLEDGE

## 10/30/2026

NOTES:

    - Redesign for all pages has been finished*
        * Still need to test the pictures once live
    - Made footer sticky
        - Tried making it a fixed footer but I did not like it, sticky feels much better

## 10/29/2026

NOTES:

    - Add `editRun(id)` script to facilitate inline editing for all input values (editmode)
        - All three fields are editable
        - Edit button switches between edit and save depending on if user is in the editing form
        - Flask route is ready to recieve updated values
        - TEST OK
    - Add delete run button
        - Just needed to add jinja html since the delete run logic is already there
        - TEST OK CONINUE
    - Add cancel button in edit mode
        - This one gave me a rough time
        - Logic implemented quickly, css making me want to eat my keyboard
        - 45 minutes of debugging later, buttons are stacked properly in and outside edit mode
            - A lot of containers and css restrictions to make it work
    - Dashboard redesign done (allegedly) c:
    - Added run and walk totals to all history page in order to display them in relevant areas
    - All history redesign done (allegedly) c:
    - Mobile layouts done:
        - Dashboard: GOOD
        - All History: GOOD

NEXT:

    - Finish redesign for rest of pages:
        - Login
        - Register
        - Settings
    - Connect to portfolio without compromising backend data
    
## 10/28/2026

NOTES:

    - Really good progress today
    - Total run miles and total walk miles have been separated as well as the monthly totals being streamlined
        - Added activity params to the `get_total_miles` function
        - Adjusted monthlies to be a dictionary containing all runs, get with `monthly_totals` dict
    - Dashboard redesign 90% done!**
        - *Cannot test that the photos work until I connect to cloudinary
        - *Need to add delete and edit buttons to history runs
            - Will have to figure out a non-invasice way to set up the edit run
            - Perhaps on edit the text becomes editable? Think on it.
        - Doing basic testing until then, will go more in depth in final stages
        - Made Activity History show 9 most recent runs rather than 6 since the design allows it

NEXT:
    - Add delete button to recent history runs
    - Add `edit_run` to recent history runs
        - Need to build the function still in `app.py`
        - Need to figure out easiest and least invasive way to edit items without it taking up an unnecessary amount of space
    - After all that is done, move to `All History` page redesign
        - I'm thinking I want this page to mimic either the monthly totals or the compressed summary, still unsure which
        - I guess it could be both on one page?

## 10/27/2026

NOTES:

    - One comma was ruining my day c':
    - Realized I need to actually put data in to test it correctly
        - Adding a couple sections in the hopes it works after giving it data
        - I realize what is going on now

    - Monthly miles code only grabs the amount of miles by each month, I was looking at the wrong this the entire time
        - I need to get the total amount of miles of all time, one is run miles one is walk miles
        - This is going to be in just total miles, I just need to separate by activity like I did with the monthly totals
        - I think there should also be an option to reset the miles! Might just be good considering Katie is using it to track how many miles are on her shoes as well
    
    - The log activity is looking good and works as expected, not much else to say
    - Activity by month:
        - I only got around to adding the filter selection before straying to mess around with the total walk/run at the hero

NEXT:
    - Continue working on redesign
    - Clean and add to app.py as needed
    - Make sure all sections work as intended after redesign!

    - Fix walk/run totals at hero not loading correctly

## 10/26/2026

NOTES:
    - Enviroment is connected to a temporary development database on Render just to test while the web app is still live and working
    - Katie is actively using the mile tracker, so it's imperitive that we keep that data safe, therefore a separate testing branch on a separate testing database seemed
    best bet

    -'ashboard.html' is the old dashboard file (lol)
        - I wanted to keep is as a reference of the placing of things since I enjoyed how that was structured
        - Will delete when done referencing
    - Currently working on redesigning the landing section (now correctly renamed 'hero-section')
        - Honestly, it's looking really nice
        - Following the same design motifs as the folio seems to be the way to go, just making the design to fit the tracker's section structure
    
    - Seems like there's a disconnect for the run and walk totals in the frontend
        - I am not surprised at this, I will probably come into a lot of messiness in the backend app.py while I redesign
        - This was my first shot at a full stack application after all
        - That's definitely something that will need to be looked at before moving to the other sections down the dashboard
    - The colors are feeling good too c:
        - Doing ocean/mermaid themes in the root because Katie loves mermaids
        - I'm liking this like warm ocean/seaweed kind of vibe its got going on tbh
    - This is probably going to take a lot longer than I'm thinking since there are 4 other pages I need to redesign but its okay
        - Honestly, the only page that needs a HUGE revamp is the Dashboard, so once that's done I actually expect the rest to go quite quickly

NEXT:
    - Continue working on Dahboard/Hero Section
    - Fix total miles for each activity not showing before continuing onto next section once done with hero

.
08/04/2026

-Fixed confirm delete bug
    -Updated the JavaScript to iterate over all delete forms using forEach(), allowing a confirmation event listener to be attached to each delete button individually
    -All routes updated
-Navbar padding and gap for dropdown reduced
    -Dropdown looks more compressed now, feels better to look at
    -nav li padding reduced from 7px to 4px
    -nav ul gap reduced from 20px to 7px

.
07/30/2026

MAJOR:
    -Settings page works!
        -Change username changes username
            -Does not allow change if current username is same as new username
            -Added password confirmation for extra validation
        -Delete account deletes account
            -Added password confirmation and confirm delete account eventListener in JS
        -Flash added at the top of every page
    -Delete photo button added
        -Deletes from both the Database and Cloudinary

MINOR:
    -Padding on dashboard elements fixed
        -They not sit centered and close to each other, this avoids larger screens having large gaps between the sections
    -Show password was not working on the confirm password on the register page
        -Just needed to implement the event listener in JS and change the ID for the confirm password
        -confirm password still has 'show-password' class to keep CSS consistent
    -Home page footer was link to dashboard; fixed
        -a tag not closed
    -Home page restyled
        -Centered all content
        -Added 'functional projects' and 'in progress' lists
        -Any projects that are already functional and working have links attached for easy access from the home page
    -Settings page restyled
        -Mobile functional, single column
    -Made nav bar dropdown slide into a nice fade transition, looks wonerful

TO DO:
    MAJOR:
        -Confirm delete DOES NOT WORK FOR EITHER
            -QueryAll makes neither work, not even the first element is confirmed on delete
            -QuerySelector works as expected, only prompting confirm for first of its kind
    MINOR:
        -Take videos and screenshots for those who just want to see what it looks like and what it does
        -Nav gap between links looks a little excessive

NOTES:
    -We are about 96%-98% done with the mile tracker!!
    -Extra features and improvements will be low priority
        -All important features are functional and application is ready to be used :)

.
07/29/2026

NOTES:
    -Usernames are now case-insensitive
        -Usernames are stored in the database by default with .lower()
        -Also added .strip()

TO DO:
    HIGH PRIORITY:
        -Finish setting up the settings page
            -still need to create 'delete_account' function
        -Create a demo page with items filled out already so that employers can look
        around without having to create an account
            -Make it read-only
            -If anyone wants to actively use the tracker or any other apps, they must make an account
    MINOR:
        -Add max-width to monthly-miles, all-history CSS
        -Make a little delete button that appears on hover over the pictures
            -Small, non-intrusive button in the upper right corner feels like it could work

.
07/28/2026

MAJOR:
    -Refactored template pages
        -Added mile-tracker folder in templates with related html pages
        -Added portfolio folder for basic templates
    -Login is specific to the Mile Tracker, the rest of the site is accessible without a password now
    -Renamed mile_tracker to dashboard for clarity
    -Gave nav tabs dropdown option
        -Mile Tracker now drops down to options for 'dashboard', 'settings', 'history', and 'logout'

MINOR:
    -Changed home page visuals
        -Added direct link to mile tracker (this is a bit unnecessary since it's on the navbar but for now it's fine)
    -The logs on the all runs history is fixed :')
        -I mispelled container T-T
        -It works as expected now with the proper name attached to the CSS
    -Log activity form feels much better
        -Added divs to each form label and input in order to align them properly
    -Mobile layout is now one single, centered column
    -CSS changes:
        -Link hover changed to a darker blue
        -Visited links now show as a lighter blue

TO DO:
    HIGH PRIORITY:
        -Finish setting up the settings page
            -still need to create 'delete_account' function
        -Create a demo page with items filled out already so that employers can look
        around without having to create an account
            -Make it read-only
            -If anyone wants to actively use the tracker or any other apps, they must make an account
    MINOR:
        -Create extra validation in registration page
            -Currently I believe different capitalizations work with any username, this is not good
            -Make it so that if the username is taken in any capitalization, it will not allow creation
        -Add max-width to monthly-miles, all-history

NOTES:
    -Good workday, mainly fixing UX and UI problems, making things more accessible and readable
    -Biggest win is refactoring the templates folder, this reads much better now
    -Very happy about how the mile tracker looks now
    -Debating whether or not tomove some of the dashboard around on the desktop layout, but thats a far away issue
    -I still want to maybe do a random photo, but that might also be something I have on the lowest priority

.
07/27/2026

MAJOR:
    -Date format changed
        -In small history: month, day (Jul 27)
        -In all history: month, day, year (July 27, 2026)
    -Started working on mobile layout for mile-tracker app

MINOR:
    -Changed log activity template
        -Might change later, I don't think I like the all vertical it feels too tall

TO DO:
    HIGH PRIORITY:
        -Fix All History page
            -I messed up on some CSS somewhere when I was editing the small-info container
            -Added a new class ".all-info-container" use this to create new ruleset that only applies to all history page
        -Finish setting up the settings page
            -still need to create 'delete_account' function
        -Make login specific to mile-tracker
        -Create a demo page with items filled out already so that employers can look
        around without having to create an account
            -Make it read-only
            -If anyone wants to actively use the tracker or any other apps, they must make an account
    MINOR:
        -Changed small history to read [ Date  Activity/Miles  Delete]
            -More readable with the smaller format
        -Create extra validation in registration page
            -Currently I believe different capitalizations work with any username, this is not good
            -Make it so that if the username is taken in any capitalization, it will not allow creation
        -Honestly I really don't like how it looks after changing the CSS, fix it

NOTES:
        -Small workday today, main priority was formatting the date correctly on the
        app
        -Played around with the layout a bit, fixed the weird padding issue on the small activity history (bless, that was really bothering me)
            -It was because of a weird 95% width rule in the child container CSS

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
        -Fix mobile layout
            -Section element (especially on the mile tracker dash) padding is too thick
            -Settings gets crazy if you scale it too small
            -Reduce mobile gallery to 4 pictures, currently it's 6 per page

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
