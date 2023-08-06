PushOverflow
============

[![PyPI version](https://badge.fury.io/py/PUSHOVERFLOW.svg)](http://badge.fury.io/py/PUSHOVERFLOW)
[![Build Status](https://travis-ci.org/amcintosh/PushOverflow.svg?branch=master)](https://travis-ci.org/amcintosh/PushOverflow)
[![codecov.io](http://codecov.io/github/amcintosh/PushOverflow/coverage.svg?branch=master)](http://codecov.io/github/amcintosh/PushOverflow?branch=master)

Send Pushover notifications of new questions posted to StackExchange

### Installation and Requirements

PushOverflow has been written for Python (tested with Travis CI on 2.7 and 3.2+, and I personally run it with Python3.2 on Ubuntu). 

To install:
```
$ python setup.py install
```
or alternatively:
```
$ pip install pushoverflow
```

### Setup

- Copy and rename `pushoverflow.ini.sample` to `pushoverflow.ini`. By default PushOverflow will look for the file in the current directory (eg. `./pushoverflow.ini`) or you can specify the path at runtime (eg. `pushoverflow /path/to/pushoverflow.ini`). 

- Edit the configuration for the StackExchange sites you would like notifications. `tags` allows you to filter questions with one of those tags (comma separated tags treated as boolean OR). `exclude` will filter out questions with any oof those tags. Both are optional.

  Each configuration section will check a specific StackExchange site. For instance `[scifi]` will check for new questions in http://scifi.stackexchange.com/ (Science Fiction & Fantasy).

- You will need to specify your Pushover user key in the configuration (in `userkey`), as well as [register an application](https://pushover.net/api#registration) with Pushover and specify the application's API token (in `appkey`).

- Set `time_delta_minutes` to the number of minutes you would like between each check.

- Setup a cron job (`crontab -e`) to run `pushoverflow.py` with the same frequency as `time_delta_minutes`.

  Eg. For `time_delta_minutes = 20`:

  ```
  */20 * * * * pushoverflow /path/to/config_file
  ```
or
  ```
  */20 * * * * cd /path/to/config_directory && pushoverflow
  ```

### Todo

- Some code cleanup
- Allow boolean AND of multiple tags
- More granular priority settings
