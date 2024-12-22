from datetime import date, datetime

def time_to_minutes(time_str: str) -> int:
    """Convierte una cadena de tiempo en formato HH:MM a minutos."""
    if not time_str:
        return 0
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_time(minutes: int) -> str:
    """Convierte minutos a una cadena de tiempo en formato HH:MM."""
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"

def getPeriodTime(periodo: int, year: int):
    period = {
        1: {
            'start': date(year, 1, 1),
            'end': date(year, 3, 31)
        },
        2: {
            'start': date(year, 4, 1),
            'end': date(year, 6, 30)
        },
        3: {
            'start': date(year, 7, 1),
            'end': date(year, 9, 30)
        },
        4: {
            'start': date(year, 10, 1),
            'end': date(year, 12, 31)
        }
    }

    return period[periodo]

def calculete_service_year(date_admission):
    """Calcula los años de servicio a partir de una fecha de adhesión.

    Args:
        fecha_adhesion: Un objeto datetime.date que representa la fecha de adhesión.

      Returns:
        Un entero que representa los años de servicio.
    """
    today = datetime.today()
    years = today.year - date_admission.year

    # Si aún no ha pasado el mes de nacimiento en el año actual, restamos un año
    if today.month < date_admission.month or (today.month == date_admission.month and today.day < date_admission.day):
        years -= 1

    return years

def getAgeEmployer(birthday):
    dateBirthday = datetime(int(birthday[0]), int(birthday[1]), int(birthday[2]))
    dateToday = datetime.now()
    age = dateToday.year - dateBirthday.year - ((dateToday.month, dateToday.day) < (dateBirthday.month, dateBirthday.day))
    return age
