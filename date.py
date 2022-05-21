from datetime import date

def Count_Days(d):
	future_date = date(d[0], d[1], d[2])
	today = date.today()
	_days = (future_date - today).days
	return _days
