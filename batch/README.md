## mf batch

run docker:
```
docker build -t kimura/mf_batch .
docker run --name mf_batch --net="bridge-xxxxxxxx" -v ~/workspace/python_lang/mf/batch:/src -d kimura/mf_batch
```

exec btach:
```
python3 mf.py
```
