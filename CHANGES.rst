CHANGES
=======

0.1.6 (2017-01-03)
------------------

* Fix the critical bug in request.forms.
* Flexible template settings.

0.1.5 (2017-01-01)
------------------

* Refactor Response classes.
* Split environs to requests.py and responses.py
* Remove Config class.

0.1.4 (2017-01-01)
------------------

Happy New Year! This is a first release in 2017.
We hope kobin helps your web development.

* Enhancement coverage.
* Add some refactoring changes.
* Set Cookie encryption using `config['SECRET_KEY']` .


0.1.3 (2016-12-30)
------------------

* End of support python3.5
* Add accept_best_match function
* Refactor config object.
* Modify after request hook


0.1.2 (2016-12-18)
------------------

* Support cookie encrypting.
* Add BaseResponse class.

0.1.1 (2016-12-17)
------------------

* Response class can return bytes.
* Fix stub files.

0.1.0 (2016-12-07)
------------------

* Add before_request / after_request hook
* Update docs.

0.0.7 (2016-12-05)
------------------

* headers property in Request object.
* raw_body property in Request object.
* Remove jinja2 from install_requires.
* Update docs.

0.0.6 (2016-12-04)
------------------

* Integrating wsgicli.
* Alter sphinx theme.
* Update documentations.
* View functions must return Response or its child class.
* Make Request object to No thread local
* Add Response, JSONResponse, TemplateResponse, RedirectResponse.
* Refactor error handling.
* Add stub files (`.pyi`).
* Python3.6 testing in travis-ci.org.
* Add API documentation.

0.0.5 (2016-11-28)
------------------

* Replace regex router with new style router.
* Correspond reverse routing.
* Remove serving static file. Please use wsgi-static-middleware.
* Remove server adapter.
* Support only Jinja2.
* Refactoring.

0.0.4 (2016-02-28)
------------------

* Expect the types of routing arguments from type hints.
* Implement template adapter for jinja2.
* Server for static files such as css, images, and so on.
* Manage configuration class.
* Support gunicorn.
* Error handling.
* Fix several bugs.

0.0.3 (2016-02-08)
------------------

* Request and Response object.
* tox and Travis-CI Integration.

0.0.2 (2015-12-03)
------------------

* Publish on PyPI.

0.0.0 (2015-09-14)
------------------

* Create this project.
