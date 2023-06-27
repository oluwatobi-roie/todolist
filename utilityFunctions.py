from datetime import datetime, date

"""
Date Modifier helps convert the date from the SQL line, 
Deletes it, and 
"""


def dateFormater(ndate):
    current_time = datetime.now()
    enterDate, enterTime = ndate.split()
    year, month, day = enterDate.split("-")
    Hour, Minute, Second = enterTime.split(":")
    item_time = datetime(int(year), int(month), int(day), int(Hour), int(Minute), int(Second))
    duration = current_time - item_time
    duration = duration.total_seconds() - 3600
    print(duration)
    if 0 < duration < 60:
        return "Just Now"
    elif 60 <= duration < 3600:
        return "Some Minutes Ago"
    else:
        return "{:.0f} Hours ago".format(duration/3600)
