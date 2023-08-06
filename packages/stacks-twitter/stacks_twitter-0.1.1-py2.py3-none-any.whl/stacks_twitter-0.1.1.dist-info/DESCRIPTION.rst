# stacks-twitter

A Stacks apps for featuring tweets.

## Dependencies

* `django-textplusstuff` >= 0.4
* `python-twitter` >= 2.0
* `stacks-page` >= 0.1.1

## Release Notes

### 0.1.1

* Including templates in PyPI release.

### 0.1

* Initial open source release

## Running Tests

All commands below are run from within the `stacks-twitter` outer folder of this repo.

First create a new virtual environment and install the test requirements:

    $ pip install -r requirements.txt

Before running tests, first ensure this app passes a `flake8` linter check:

    $ flake8 stacks_twitter


## Settings

Only one required setting, `STACKS_TWITTER_API_KEYS`. You'll first need to setup a new Twitter application to get these values.

```
STACKS_TWITTER_API_KEYS = {
    'consumer_key': '<twitter consumer key>',
    'consumer_secret': '<twitter consumer secret>',
    'access_token_key': '<twitter consumer token key>',
    'access_token_secret': '<twitter consumer token secret>'
}
```


