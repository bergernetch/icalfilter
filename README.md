# icalfilter
Filter out old ical events from a calendar.

The main use case for this script is to filter out old events from a cluttered, slow-performing calendar that contains years of events.

This script filters out events that are older than the specified year. This includes recurrent events that have an *until* date earlier than that year. Events that have no *until* date or where the *until* date is not earlier than the specified year are preserved.

## Installation
Using your python 3 installation run:

```
pip install pytz icalendar
```

## Usage
* Download calendar from icloud with wget
* Run `python3 icalfilter.py infile.ics outfile.ics`, a filtered version of the calendar named `out.ics` is produced, events older than the current year will be filtered out
* Use the file for magicmirror or similar

The script can be integrated to automatically produce a smaller file and called by cron:
```
*/15 * * * * wget -O ~/magicmirror/mounts/modules/ics/mycal.ics.raw https://p16-caldav.icloud.com/published/2/MTASDF-YOUR-CALENDAR-URL >/dev/null 2>&1 && python3 ~/icalfilter/icalfilter.py ~/magicmirror/mounts/modules/ics/mycal.ics.raw ~/magicmirror/mounts/modules/ics/mycal.ics >/dev/null 2>&1 || rm -rf ~/magicmirror/mounts/modules/ics/mycal.ics
```
