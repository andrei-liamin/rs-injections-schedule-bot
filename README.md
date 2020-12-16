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

## How to deploy

deploy on heroku with github connected
then activate script with command in heroku CLI:
```
heroku ps:scale worker=1
```
turn off heroku dyno to test bot locally
```
heroku ps:scale worker=0
```
