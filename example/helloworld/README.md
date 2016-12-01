# hello example

## How to run

**In Development**

Please run with wsgicli.

```console
$ pip install kobin wsgicli
$ wsgicli hello.py app --reload
```

**In Production**

And if you want to run in production, please run with gunicorn.

```console
$ pip install kobin gunicorn
$ gunicorn -w 1 hello:app
```
