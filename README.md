# karby
競馬用スクレイピング


ネット競馬は特殊なのでSeleniumが必要

localだとdriverとかめんどくさいのでDocker使い。ますた


```
$ docker built -t unko .
$ docker run --rm -v "$PWD:/work" unko python endpoints.py
```