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

copy changed files on VPS
then restart service:
```
systemctl restart rs-injections-schedule-bot
```

# Useful resources

Telegram API
https://core.telegram.org/bots/api

pyTelegramBotAPI docs
https://github.com/eternnoir/pyTelegramBotAPI

APScheduler docs
https://apscheduler.readthedocs.io/en/stable/