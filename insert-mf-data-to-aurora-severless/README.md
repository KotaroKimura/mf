# insert-mf-data-to-aurora-severless

# layer
``` bash
[layer/chrome/chromedriver v2.43]
https://chromedriver.storage.googleapis.com/2.43/chromedriver_linux64.zip

[layer/chrome/headless-chromium v1.0.0-55]
https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-55/stable-headless-chromium-amazonlinux-2017-03.zip

[layer/python(selenium)]
pip3 install -t ./python/lib/python3.6/site-packages selenium==3.141.0
```

# invoke on local
``` bash
sam build
sam local invoke
```
