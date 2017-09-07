# Reminder Bot
## An event based reminder bot for Slack, by Jacob Stoebel

There are lots of reminder apps out there, but none that I found were able to organize reminders the way I needed them. As a new parent, I need to keep to a schedule but I also need to be flexible. For example, when my son was a newborn, he needed to eat every three hours. In a traditional reminder app I would set reminders at 6am, 9am, noon, etc. But this isn't exactly right. If everything goes according to plan, the reminders work just fine. As any parent knows however, things never go exactly according to plan. If my son gets hungry at 8am, the entire schedule is thrown off.

Really, we don't need a schedule. We need a way to keep track of recent events, and know when a particular item is due to happen. Instead of setting reminders to go off at set times, I enter events when they happen, and the app tells me when something needs to happen again.

# Set up

## Install Dependencies
First install your dependencies: `pip install -r requirements.txt`

## Setup

First we need to get things setup on Heroku. From the root of your app:

- `heroku create [your-app-name]`
- `heroku addons:create mongolab`
- `heroku app:info` and copy the value for `Web URL`. You'll need it in a minute.

Unfortunately, Slack apps are not a one click deploy. You need to head over to [https://api.slack.com/apps](https://api.slack.com/apps) to create a new app. Once you've done that:

 - click add features and functionality -> Slash Commands. Register the following slash commands. Each commands should be mapped to <your-url>/<command_name>
     + /new_task
         * description: creates a new task
         * Usage Hint: name=eat pizza freq=3
     + /task_status
         * description: get status on a task 
         * Usage hint: name of task to check
     + /new_event
         * description: add a new event
         * Usage hint: task=name of task time=8:30
     + /remove_task
        * description: removes a task
        * Usage hint: task to remove
- Finally, you'll need to grab your Slack token so the bot can post hourly status updates. Add that token to your Heroku environment by typing - `heroku config:set <your slack token >`
- And last but not least we are ready to deploy: `git push heroku master`

Have fun!

