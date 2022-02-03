import icalendar
import datetime
import pytz
import sys
infile = sys.argv[1]
outfile = sys.argv[2]

utc = pytz.utc

d = datetime.date.today()
year = d.strftime("%Y")
YEAR = int(year) - 1

def main():
    with open(infile, 'r', encoding='utf-8') as f:
        cal = icalendar.Calendar.from_ical(f.read())
        outcal = icalendar.Calendar()

        for name, value in cal.items():
            outcal.add(name, value)

        def active_event(item):
            start_date = item['dtstart'].dt

             # recurrent
            if 'RRULE' in item:
                rrule = item['RRULE']
                # print (rrule)
                if 'UNTIL' not in rrule:
                    return True
                else:
                    assert len(rrule['UNTIL']) == 1
                    until_date = rrule['UNTIL'][0]

                    if type(until_date) == datetime.datetime:
                        return until_date.timestamp() >= datetime.datetime(YEAR, 1, 1).timestamp()

                    if type(until_date) == datetime.date:
                        return until_date >= datetime.date(YEAR, 1, 1)

                    raise Exception('Unknown date format for "UNTIL" field')

            # not reccurrent
            if type(start_date) == datetime.datetime:
                return start_date.timestamp() >= datetime.datetime(YEAR, 1, 1).timestamp()

            if type(start_date) == datetime.date:
                return start_date >= datetime.date(YEAR, 1, 1)

            raise Exception('ARGH')


        for item in cal.subcomponents:
            if item.name == 'VEVENT':
                start_date = item['dtstart'].dt
                if active_event(item):
                    print ('INCLUDE', item['summary'], repr(start_date))
                    outcal.add_component(item)
                else:
                    print ('EXCLUDE', item['summary'], repr(start_date))
                    pass
            else:
                outcal.add_component(item)

        with open(outfile, 'wb') as outf:
            outf.write(outcal.to_ical(sorted=False))

main()
