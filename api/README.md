## mf api

run docker:
```
docker build -t kimura/mf_api .
docker run --name mf_api --net="bridge-xxxxxxxx" -v ~/workspace/python_lang/mf/api:/app -p xxxxxx:xxxxxx -d kimura/mf_api
```

exec api:
```
gunicorn application:application -b 0.0.0.0:8888 --reload --workers=1
```
