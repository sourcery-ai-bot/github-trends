from src.models import UserPackage, WrappedPackage
from src.subscriber.aggregation.wrapped.time import get_month_data, get_day_data
from src.subscriber.aggregation.wrapped.calendar import get_calendar_data
from src.subscriber.aggregation.wrapped.numeric import get_numeric_data
from src.subscriber.aggregation.wrapped.langs import get_lang_data
from src.subscriber.aggregation.wrapped.repos import get_repo_data
from src.subscriber.aggregation.wrapped.timestamps import get_timestamp_data

# from src.processing.user.follows import get_user_follows


def main(user_package: UserPackage, year: int) -> WrappedPackage:
    """packages all processing steps for the user query"""

    month_data = get_month_data(user_package)
    day_data = get_day_data(user_package)
    calendar_data = get_calendar_data(user_package, year)
    numeric_data = get_numeric_data(user_package, year)
    repo_data = get_repo_data(user_package)
    lang_data = get_lang_data(user_package)
    timestamp_data = get_timestamp_data(user_package)

    return WrappedPackage(
        month_data=month_data,
        day_data=day_data,
        calendar_data=calendar_data,
        numeric_data=numeric_data,
        repo_data=repo_data,
        lang_data=lang_data,
        timestamp_data=timestamp_data,
        incomplete=user_package.incomplete,
    )
