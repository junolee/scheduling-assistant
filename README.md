## Goals
* A web app that provides one place to manage your agenda and turn your goals into reality
* Calendar has a beautiful, minimalist design that is useful and intuitive to use
* Planner lets you focus to plan and breakdown your goals even better than you can with pen and paper
* Intuitive way to turn objectives into actionable tasks in your agenda
* Analytics provides feedback that helps you plan better and learn more about yourself
* Helps you schedule your weekly and daily routines automatically and learns from your adjustments/habits
* Generates schedules to work towards your goals around your events (?)
* Suggestion pop ups - you seem to [...] , why don't you work on [...] today? - can turn this on or off
* Add calendar events and reminders easily with NLP/speech recognition
* Ask free/busy or agenda on a given day - NLP
* Shortcuts like `!c` for creating event, `!r` for creating reminder. eg. `!r feed dog 3:00pm every sunday`

## Timeline
* Phase 1: NLP Sidebar
    - Collect data
    - Spell check - use spacey to automate - aspell, ispell - to create spell checkers
    - NLP - Classify intent & extract entities (for all actions)
    - Side bar - Design user interface for chat
    - Connect to Google Calendar API
    - Implement actions 1 & 2
    - popups to show events/reminders objects for confirmation
    - Webapp - insert monthly & weekly view next to sidebar that shows output - prototype (embed google calendar)

    Two approaches
     - text parser - heuristics
     - survey data - how would you create an event (4 typical, 2 crazy ways you wouldn't expect)

* Phase 2: Simple routines page
    - Implement NLP action 3
    - Add simple mouse interaction
* Phase 3: Schedule Generation
    - Implement NLP action 4
    - Add button to generate
* Phase 4: Create weekly view & mouse interaction
* Phase 5: Advanced routines page -- Add visualization & advanced mouse interaction
* Phase 6: Create monthly view & mouse interaction
* Phase 7: Planner - all goals, monthly, weekly, daily tasks/todos -- drag to calendar in weekly view
* Phase 8: Check tasks complete/incomplete
* Phase 9: User analytics
* Phase 10: Advanced NLP - answer questions about the app, welcome message, fun features, etc

## Machine Learning
#### NLP:

Procedure:
- Classify intent
- Extract entities
- Show outcome and confirm
- Execute action
- (Testing phase) If wrong classification, ask - which action were you trying to do? - collect this data

Possible Actions:
- add, edit, delete calendar events and reminders
- ask questions about availability, certain events/reminders
- add, edit, delete daily and weekly routines
- generate weekly schedule
- ask questions about the app

1. set calendar events and reminders
    - add/edit/delete
2. ask about availability, events, and reminders
    - ask if anything/what is scheduled at a certain time and day (returns events/reminders or none)
    - ask if anything/what is scheduled for a day (returns agenda w/ reminders or none)
    - ask what reminders today
    - when a certain event or reminder is scheduled for
    (all return nice looking event/reminder/agenda object)
3. set routines
    - add/edit/delete daily and weekly routines
4. generate weekly schedule (when automatic scheduling feature is complete)
    - something
5. answer questions about the app
    - what categories can I have for a routine
    - how do I add an event?
    - if question not recognized: sorry, I don't know the answer to that question. Would you like to submit your question to our support team? > show text box for a message    

#### Automatic Scheduling:

- add locations to routines -- default is home (or mark as anywhere)
- each fixed event is treated as just a time block with a location
* at start: (use to create initial distribution of start times)
    - what is one way you would schedule your routines in a typical day?
    - what is one way you would schedule your routines in a typical week?
        - can adjust daily routines for different days

* Procedure: (for the week)
    - schedule determined at each minute from morning to evening each day - recommends a routine (or none) based on highest probability value (random when two routines/empty have very similar values - this can vary in regeneration) - if a routine is chosen, skip to minute when routine ends
    - skip time blocks taken by fixed events
    - can regenerate week's schedule at any point, starts generation at time now until end of the week
    - can adjust start time and length of routines

* Outcome at a given time based on:
    - highest probabilities from distributions of start times for routines for that day of the week
    - yes/no values of routines that have been scheduled before it on that day
    - (?) clusters of routines -- if routines before it is in the same cluster
    - location - distance to event location near it + time between the events before/after it
    - value of none decreases towards the end of the day

If time encounters fixed time event -- rewind and pull routines that would be schedule during that time before, or push after, or push to evening, or don't include -- check option: include all daily routines

First treat all fixed events as one type -- eventually categorize?

When no fixed events in the way, which routines are fixed and which have more variance in times
Regenerate button changes options that were random -- become less random with more common times, fixed routine times respond to adjustments

features: classifier for category (eg. daily: morning, afternoon, evening weekly: mon evening, wed afternoon, etc -- identify clusters unsupervised) -- then regression for each for specific time
classifier - how much time available that day in each time block, how many fixed events(?)

mean/mode time, variance, time blocked by fixed event, time right next to fixed event, time right next to fixed event with far location, how many routines in that time block, yes/no values of other routines in that time block -- execute in order of importance of routines

#### Routines view:
- Each routine represented by a circle
- size determined by length - can adjust by stretching circle
- drag one circle on top of another to group together
- can choose a category for circle represented by color/icon - spaces out circles into clusters - check: usually done together? or other -- collect this
- can select one of common categories that comes with color & icon or customize name and choose icon (optional). app collects data on custom inputs and groups together by similarities. developers can learn from these (eg. see what the top few custom inputs are and turn it into a category if popular)

---
#### Subdomains
* Calendar
    - yearly
    - monthly
    - weekly + daily tasks
    - natural language processing to edit calendar
    - minibar activates at smallest size
* Planner
    - goals
    - objectives timeline
    - daily and weekly (by day or frequency) routines
* Analytics
    - track weekly and daily routines - how well you are following them
        -> if perfect, anything you'd like to add to help move towards goal
    - track regenerations
        - how many tasks planned but not completed
    - track how many daily tasks moved to the next day
    - track how well your goals are being meet
    - track if you plan tasks beforehand or check off throughout the day -> can use this to help generate schedules in the future (for routines)
* Schedule Generator
    - schedule routines and daily tasks around fixed events + preferences
    - regenerate during the day based on actual completions

#### Old Timeline
*  Stage 1: Create calendar and integrate google calendar
*  Stage 2: Add ai chat sidebar and natural language processing to add events & email
*  Stage 3: Generate schedules based on preferences and activity feedback
*  Stage 4: Integrate Google Maps for event locations


#### Stage 1: Create calendar and integrate google calendar

1.  Calendar web app
2.  Minimalist design
3.  Integration with google calendar
4.  Add events and details on command line
5.  View daily schedules by hovering over and add by clicking #
6.  Click to view event details
7.  Make it easy to send out your availability to others

#### Stage 2: Add ai chat sidebar and natural language processing to add events & email
1.  Add ai chat sidebar - toggle on/off
2.  Welcome message at start
3.  Ability to add events and details in chat
4.  Show preview of event - ask to confirm or edit information
5.  Ability to send google calendar event invites
6.  Integration with Gmail - send emails, view inbox in chat bar
7.  Integration with Slack - view channels and send messages

#### Potential Features:
* Collect data on GPS location to analyze and adjust times
* Add features specific to Denver, CO - eg. Bike routes, buses, food suggestions

#### Business Plan
3 Plans: Free, Professional, Business


1. Scheduling - recommend schedule to meet goals with events, optimize daily workflow, learn your preferences
2. Goal Tracking - view analytics/progress
3. Planning
4. Communicating

Calendar (W, M, Y)
Planning Space
Goal Tracking

Monthly Goals > Weekly Objectives > Daily Tasks and Todo's

Toggle space to view tasks and todo's with weekly agenda

Events -- Y, M, W
Goals -- Y, M, W

Side Bar -- Overview (set options), Agenda View (set options), reminders, natural language processing

Be easy to use without always being active with goal planning

Can see both or one at a time (one on top of the other or side by side)

- monthly, weekly, planner, agenda view, yearly
- Natural language processing - add events (show preview and edit, confirm), change settings
- Reminders - add with nlp
- Side bar - consistent, minimize to just side bar
- integrate with google maps
- route planning
- send availability to others
- view coworkers availability (team feature)
- send event invites
- send emails, view inbox - integration with gmail
- predict when to work, eat, exercise
- optimize on a day basis
- set personal goals throughout the week that the calendar optimizes/recommends schedules for
- view analytics and progress
- convert planner tasks to timed plans on calendar
- check off planner tasks in work blocks (or customizable blocks) on calendar (drag and drop tasks to calendar events)
- customizable block types with customized NLP key words
- plan events with friends = send through messaging - fb/email/imessage/textmessage

- completed todos >

planner items > calendar
multiple calendars/accounts in one
track - work, exercise, eat

** checkout successful progress tracking sites

#### Why are you building this?
- easy to use
- beautiful, minimalistic interface
- *one organized place* for your yearly to daily planning and all your calendars
- *optimizes* your agenda to help you work towards your goals & meet your responsibilities
- *feedback* on progress - view analytics
- *understands you* - natural language processing
- connect with others easily - send/receive availabilities, send event invites
- community - feedback from users, vote things, contribute to new features, share examples, good systems
- potential: integrated with all your fav apps - gmail, drive, slack, etc
- potential: create calendar specific plans (for business, for particular department)

A personal assistant that helps you schedule, plan, connect, and optimize
