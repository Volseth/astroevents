import datetime
import math

MJD_JD_CONVERSION_VALUE = 2400000.5
LONGITUDE_MINUTES_VALUE = 4.0
DEFAULT_DATE_FORMAT = "%Y-%m-%d"

AUTO_CONVERSION_JD_MJD_VALUE = 1721060.5


def find_corresponding_night(JD: float, Lon: float) -> datetime:
    """
    From range [0,AUTO_CONVERSION_JD_MJD_VALUE] JD is treated as MJD (years 4713 BC to year 0 AC)
    From range [AUTO_CONVERSION_JD_MJD_VALUE, inf) there is no conversion
    Supported MJD years are from 1858-11-17 0:00:00 to 6570-12-24 12:00:00
    Years are configurable via AUTO_CONVERSION_JD_MJD_VALUE
    """
    if JD - AUTO_CONVERSION_JD_MJD_VALUE <= 0:
        JD = mjd_to_jd(JD)

    greenwich_date_time = jd_to_datetime_object(JD)
    longitude_time_difference = abs(Lon * LONGITUDE_MINUTES_VALUE)

    time_delta = datetime.timedelta(minutes=longitude_time_difference)

    local_solar_time = greenwich_date_time + time_delta if Lon >= 0.0 else greenwich_date_time - time_delta
    if local_solar_time.hour >= 12:
        night = local_solar_time.strftime(DEFAULT_DATE_FORMAT)
    else:
        night = (local_solar_time - datetime.timedelta(days=1)).strftime(DEFAULT_DATE_FORMAT)
    return night


def mjd_to_jd(MJD: float) -> float:
    return MJD + MJD_JD_CONVERSION_VALUE


def jd_to_date(JD: float) -> (int, int, float):
    # Conversion to Greenwich calendar date using method from book "Practical Astronomy with your
    # Calculator or Spreadsheet"
    # math.trunc -> remove fractional part of a number
    if JD < 0:
        raise ValueError("Invalid argument for JD to date conversion")
    JD = JD + 0.5
    fractional_part, integer_part = math.modf(JD)
    integer_part = int(integer_part)

    if integer_part > 2299160:
        A = math.trunc((integer_part - 1867216.25) / 36524.25)
        B = integer_part + 1 + A - math.trunc(A / 4.)
    else:
        B = integer_part

    C = B + 1524
    D = math.trunc((C - 122.1) / 365.25)
    E = math.trunc(365.25 * D)
    G = math.trunc((C - E) / 30.6001)

    day = C - E + fractional_part - math.trunc(30.6001 * G)
    month = G - 1 if G < 13.5 else G - 13
    year = D - 4716 if month > 2.5 else D - 4715
    return year, month, day


def day_to_hour_minutes_seconds(day: float) -> (int, int, int):
    if day > 1.0:
        raise ValueError("Invalid argument for day conversion")
    # Get hours from day, fractional part is minutes left, then fractional part from minutes is seconds
    hours = day * 24.
    hours, hour = math.modf(hours)

    minutes = hours * 60.
    minutes, mins = math.modf(minutes)

    seconds = minutes * 60.
    seconds, sec = math.modf(seconds)

    return int(hour), int(mins), int(sec)


def jd_to_datetime_object(JD: float) -> datetime:
    year, month, day = jd_to_date(JD)

    fractional_day, day = math.modf(day)
    day = int(day)

    hours, minutes, seconds = day_to_hour_minutes_seconds(fractional_day)

    return datetime.datetime(year, month, day, hours, minutes, seconds)
