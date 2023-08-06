# README

This is a python library and sample scripts to handle OpenDayLight instance.

## Installing

This is a python module, you can install into your system, running:

```
$ python setup.py install
```

## Examples

For examples, please visit the `scripts` folder.

In order to run the examples inside the `scripts` folder, you need to export the
variables with the server address/port and your credentials:

```
$ export ODL_URL="http://127.0.0.1:8080"
$ export ODL_USER="admin"
$ export ODL_PASS="admin"
```

## Running queries from curl

To insert and remove flows, you can use this library (see `scripts` folder), but
if you need to test using curl directly please open `CURL.md`.
