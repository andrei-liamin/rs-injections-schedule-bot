# ms-injection-instruction-tgbot
Telegram bot which sends a place for Glatiramera Acetate injection every day

---
## How to activate python environment

at first fix Execution Policy on Windows: 
```
Set-ExecutionPolicy Unrestricted -Scope Process
```

then activate environment:
```
env\Scripts\activate
```

deactivate environment:
```
deactivate
```

## How to stop/start bot service on VPS when test the bot locally

```
systemctl stop rs-injections-schedule-bot
```
```
systemctl start rs-injections-schedule-bot
```
get service status description:
```
systemctl status rs-injections-schedule-bot
```

## How to deploy on VPS

copy changed files on VPS to:
/home/dron/tg-bots/rs-injections-schedule-bot/

then restart service:
```
systemctl restart rs-injections-schedule-bot
```

## Question template for AI (Copilot, chatGPT or another)

```
Context:
# here explain your context, e.g
I'm writing a code in python for my telegram bot. I'm using telebot library for that.

Goal:
# here explain your goal to achive, e.g
Can you please fix and explain why I don't receive images in my bot.

# then paste snippet within triple ` brackets

```

# Useful resources

Telegram API
https://core.telegram.org/bots/api

pyTelegramBotAPI docs
https://github.com/eternnoir/pyTelegramBotAPI

APScheduler docs
https://apscheduler.readthedocs.io/en/stable/