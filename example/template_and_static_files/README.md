# Static files and template example

## How to run

**In Development**

Please run with wsgicli.

```console
$ pip install kobin wsgicli jinja2
$ wsgicli app.py app --reload --static --static-root /static/ --static-dirs ./static/
```

**In Production**

And if you want to run in production, please run with gunicorn.

```console
$ pip install kobin gunicorn
$ gunicorn -w 1 app:app
```

And static files are return with reverse proxy (ex: Nginx).
