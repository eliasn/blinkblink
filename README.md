A simple macOS app which reminds you to take breaks from looking at your
screen.


# Features

- Sends a macOS notification every 20 minutes (or whatever interval you
  set)
- Can be paused for a given period (e.g. for meetings, pair programming
  sessions etc.)
- Simple uncluttered interface
- Simple JSON config file


# Requirements

- python3
- rumps
- py2app


# Building

```shell
python3 setup.py py2app
```


# Installation

Just drop the app to your Applications folder.


# Configuration

All configuration is done by editing the JSON file. It is located in
`~/.local/blinkblink/config.json`. Here is an example:

```json
{
    "interval": 1200,
    "pause": 3600,
    "reminder": "Move your eyes away from the screen :)"
}
```

Both intervals are in seconds. The default values are as per this
example, that is, 20 minutes for the reminder interval and 1 hour for
pause.