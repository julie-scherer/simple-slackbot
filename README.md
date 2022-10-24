# Welcome Bot 

This is a very simple Slack bot for sending a welcome message to a channel and displaying the message in the app's home. The current app is designed for the Coding Temple Alumni Slack, but everything is stored in `app.py` so that you can easily reconfigure the functionality or UI for your app. I used the **[Slack Block Kit Builder](https://app.slack.com/block-kit-builder/)** to build out the welcome message and home view, and highly recommend utilizing this resource when building and designing your app.


## Set up and installation


### Configuring your local environment

1. Clone/fork the git repo and create a virtual environment

    ```
    git clone https://github.com/schererjulie/WelcomeBot.git
    cd WelcomeBot
    python3 -m venv venv
    ```

2. Activate the virtual environment

    ```
    . venv/bin/activate
    ```

3. Install packages

    ```
    pip install -r requirements.txt
    ```

4. Create `.env` file to store your bot's token and signing secret

    ```
    touch .env
    open .env
    ```

    Copy and paste this text into the `.env` file (you will replace the values with the bot's token and signing secret later)

    ```
    SLACK_BOT_TOKEN=xoxb-your_bots_token
    SLACK_SIGNING_SECRET=signing_secret
    ```


5. Download [ngrok](https://ngrok.com/download) to use as local proxy for setup

    (Later you try running the app in [Glitch](https://glitch.com/)!)



### Creating and installing your Slack app

1. Visit [api.slack.com](api.slack.com) and create your Slack app


2. Enable the app's home tab

    - Go to **Features** > **App Home** 
    - Enable the Home Tab
    - Make sure the **Home Tab** is turned ON and **Messages Tab** is turned OFF


3. Install to workspace

    - This should be a workspace where you have admin access. Otherwise, you will need to ask an admin to install the app for you.


4. Configure the local environment with the app's credentials
  
    - Go to **Features** > **OAuth & Permissions** and get the **Bot User OAuth Token**
    - Go to **Settings** > **Basic Information** and get the **Signing Secret** 
    - Save the token and signing secret in the `.env` file you created earlier
    - For more information, visit:
        * _https://api.slack.com/start/building/bolt-python#credentials_
        * _https://api.slack.com/start/building/bolt-python#initialize_
    


5. Run the app on your local computer

    ```python3 app.py```


6. Run ngrok on port 3000

    ```ngrok http 3000```


7. Enable bot events

    - Go back to [api.slack.com](api.slack.com)
    - Go to **Event Subscriptions** and turn **Enable Events** on
    - Add the request URL with the `slack/events` endpoint, which will be the ngrok forwarding address followed by '/slack/events'
    - After the server responds the challenge parameter, a green checkmark should appear
    - Save changes and continue

    _Note ngrok URL will expire after 2 hours and every time you restart ngrok, it will generate a new URL that you will have to update as the Request URL_


8. Subscribe to bot events

    - Go to **Event Subscriptions** > **Subscribe to Bot Events**
    - Subscribe to the 'app_home_opened' event


9. Add permission scopes
    
    - Go to the **OAuth & Permissions** > **Scopes**
    - Add the following Bot Token Scopes:
        1. chat:write (_Send messages as @WelcomeBot_)
        2. commands (_Add shortcuts and/or slash commands that people can use_)
        3. groups:read (_View basic information about private channels that WelcomeBot has been added to_)
        4. mpim:read (_View basic information about group direct messages that WelcomeBot has been added to_)
    - Save changes and reinstall the app to your workspace

    _Note anytime you add an event listener, you need to make sure your bot is subscribed to that type of event and it has the appropriate permission scopes. You will need to reinstall the app each time_


10. Create Slack command

    - Go to **Slash Commands** and click **Create New Command**
    - The command is **/welcome**
    - The request URL is the request URL with the endpoint `slack/events`
    - Add a short description and usage hint if you'd like
    - Click save


11. Add action listener endpoint (optional; if needed later)

    - Go to **Interactivity & Shortcuts** and turn **Enable Interactivity** on
    - Add the request URL with the `slack/actions` endpoint


#####
----------------------------------------------------------------
## Helpful resources for getting started

### Building out your bot with Bolt and Flask in Python

**Steps to get started**
  https://github.com/slackapi/bolt-python or
  https://api.slack.com/start/building/bolt-python#start 

**Bolt Python**
  https://slack.dev/bolt-python/concepts

**Python Slack SDK**
  https://slack.dev/python-slackclient/basic_usage.html

**Configuring with Flask**
  https://slack.dev/bolt-python/concepts#adapters or
  https://github.com/slackapi/bolt-python/tree/main/examples/flask or
  https://python.plainenglish.io/lets-create-a-slackbot-cause-why-not-2972474bf5c1


### Designing your bot's UI

**Slack Block Kit Builder for building out messages**
  https://app.slack.com/block-kit-builder/

**Building a home for your app**
  https://api.slack.com/tutorials/app-home-with-modal


### Setting up for public distribution

**Deploying a Slack Bolt app with Gunicorn**
  https://blog.tryfrindle.com/deploying-a-slack_bolt-app-with-gunicorn/

**Installing to a workspace**
  https://python-slackclient.readthedocs.io/en/latest/auth.html
