# Byoyomi


## Requirement

* Win10 have japanese lang installed

## try usage:

start backend:
```
$ exec.bat
```


```
$ curl -X POST -H "Content-Type: application/json" -d @- <<< '{"text": "日本"}'  http://localhost:28641/tts/
```