from datetime import datetime
from datetime import timedelta


def suite_active_without_overnight_stay(entry_datetime, exit_datetime) -> int:
    now = datetime.now()

    reservation_passed = now > exit_datetime
    reservation_entry_passed = now > entry_datetime
    suite_in_use = not reservation_passed and reservation_entry_passed

    if suite_in_use:
        return 2

    if not reservation_passed:
        return 1

    return 0


def suite_active_overnight_stay(date_of_overnight_stay) -> int:
    now = datetime.now()

    reservation_passed = now > date_of_overnight_stay
    reservation_happn = date_of_overnight_stay + timedelta(hours=15) > now
    suite_in_use = reservation_passed and reservation_happn

    if suite_in_use:
        return 2

    if not reservation_passed:
        return 1

    return 0


def suite_active(date_of_overnight_stay, entry_datetime, exit_datetime):
    if not date_of_overnight_stay:
        return suite_active_without_overnight_stay(entry_datetime, exit_datetime)

    return suite_active_overnight_stay(date_of_overnight_stay)


def format_date(date):
    if not date:
        return None

    return date.strftime('%d/%m/%Y %H:%M:%S')
