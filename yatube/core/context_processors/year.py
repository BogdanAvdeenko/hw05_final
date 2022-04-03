import datetime as dt

now_date = dt.datetime.now()


def year(request):

    return {
        'year': int(now_date.strftime('%Y'))
    }
