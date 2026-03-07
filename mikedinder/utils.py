import re

from datetime import datetime

from .models import Restaurant


class RestaurantSearchService:
    """
    Util Class to Parse Hours and Search for Open Restaurants.
    """

    # Day Name to Number Mapping
    DAY_MAP = {
        'sun': 0, 'sunday': 0,
        'mon': 1, 'monday': 1,
        'tue': 2, 'tues': 2, 'tuesday': 2,
        'wed': 3, 'wednesday': 3,
        'thu': 4, 'thurs': 4, 'thursday': 4,
        'fri': 5, 'friday': 5,
        'sat': 6, 'saturday': 6
    }

    @classmethod
    def parse_time(cls, time_str) -> int:
        """
        Parse Time String Like '11:00 am', '11 am', '12 pm' to Minutes From Midnight.

        Args:
            time_str: String Like "11:00 am" or "11 am"

        Returns:
            Integer Minutes Since Midnight (0-1439)
        """
        time_str = time_str.strip().lower()

        # Match Patterns Like "11:00 am", "11 am", "12:30 pm"
        match = re.match(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', time_str)
        if not match:
            return None

        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        period = match.group(3)

        # Convert to 24-Hour Format
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0

        return hour * 60 + minute

    @classmethod
    def parse_day_range(cls, day_str) -> list:
        """
        Parse Day Range Like 'Mon-Fri' or Single Day Like 'Sat'.

        Args:
            day_str: String Like "Mon-Fri" or "Sat"

        Returns:
            List of Day Numbers (0=Sunday, 6=Saturday)
        """
        day_str = day_str.strip().lower()

        if '-' in day_str:
            # Day Range Like "Mon-Fri"
            start_day, end_day = day_str.split('-')
            start_day = start_day.strip()
            end_day = end_day.strip()

            start_num = cls.DAY_MAP.get(start_day)
            end_num = cls.DAY_MAP.get(end_day)

            if start_num is None or end_num is None:
                return []

            # Handle Wraparound (e.g., Mon-Sat Would Be [1, 6])
            if start_num <= end_num:
                return list(range(start_num, end_num + 1))
            else:
                # Wraparound Case (e.g., Sat-Sun Would Be [6, 0])
                return list(range(start_num, 7)) + list(range(0, end_num + 1))
        else:
            # Single Day Like "Sat"
            day_num = cls.DAY_MAP.get(day_str)
            return [day_num] if day_num is not None else []

    @classmethod
    def parse_hours(cls, hours_str) -> list[tuple[list, int, int]]:
        """
        Parse the Hours String and Return a List of Operating Periods.

        Args:
            hours_str: String Like "Mon-Fri 11 am - 10 pm / Sat 11 am - 12 pm"

        Returns:
            List of Tuples: [(days_list, start_minutes, end_minutes), ...]
        """
        periods = []

        # Split by '/' to Handle Multiple Schedules
        segments = hours_str.split('/')

        for segment in segments:
            segment = segment.strip()

            # Pattern: "Mon-Fri, Sat 11 am - 10 pm" or "Mon-Sun 11:00 am - 10 pm"
            # First, try to find the time range (looking for the dash between times)
            time_match = re.search(
                r'(\d{1,2}(?::\d{2})?\s*(?:am|pm))\s*-\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm))',
                segment,
                re.IGNORECASE
            )

            if not time_match:
                continue

            start_time_str = time_match.group(1)
            end_time_str = time_match.group(2)

            # Parse Times
            start_minutes = cls.parse_time(start_time_str)
            end_minutes = cls.parse_time(end_time_str)

            if start_minutes is None or end_minutes is None:
                continue

            # Handle Midnight Crossing (e.g., 11 pm - 12:30 am)
            # If End Time is Less than Start Time, it Crosses Midnight
            crosses_midnight = end_minutes < start_minutes

            # Extract Day Portion (Everything Before the Time Range)
            day_portion = segment[:time_match.start()].strip()

            # Split by Comma to Handle Multiple Day Ranges
            day_parts = [d.strip() for d in day_portion.split(',')]

            all_days = []
            for day_part in day_parts:
                days = cls.parse_day_range(day_part)
                all_days.extend(days)

            # Remove Duplicates
            all_days = list(set(all_days))

            if crosses_midnight:
                # For times that cross midnight, we need to handle it specially
                # The restaurant is open on the specified days until midnight,
                # and open on the next day from midnight to the end time
                periods.append((all_days, start_minutes, 1440))  # Until Midnight
                next_days = [(d + 1) % 7 for d in all_days]  # Next day
                periods.append((next_days, 0, end_minutes))  # From Midnight
            else:
                periods.append((all_days, start_minutes, end_minutes))

        return periods

    @classmethod
    def is_restaurant_open(cls, restaurant, check_datetime) -> bool:
        """
        Check if a Restaurant is Open at the Given datetime.

        Args:
            restaurant: Restaurant Model Instance
            check_datetime: datetime Object to Check

        Returns:
            Boolean Indicating if Restaurant is Open
        """
        day_of_week = check_datetime.weekday()  # 0=Sunday, 6=Saturday
        check_minutes = check_datetime.hour * 60 + check_datetime.minute

        periods = cls.parse_hours(restaurant.hours)

        for days, start_minutes, end_minutes in periods:
            if day_of_week in days:
                if start_minutes <= check_minutes < end_minutes:
                    return True

        return False

    @classmethod
    def search_open_restaurants(cls, datetime_str) -> list:
        """
        Search for Restaurants Open at the Given datetime.

        Args:
            datetime_str: String datetime (e.g., "2024-03-15 14:30" or any Format Parseable by Datetime)

        Returns:
            List of Restaurant Names That Are Open
        """
        # Parse the datetime String
        try:
            # Try Common Formats
            for fmt in ['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M', '%d/%m/%Y %H:%M']:
                try:
                    check_dt = datetime.strptime(datetime_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                # If None of the Formats Work, Raise an Error
                raise ValueError(f'Unable to Parse datetime String: {datetime_str}')
        except Exception as e:
            raise ValueError(f'Invalid datetime Format: {e}')

        # Query All Restaurants
        # Real World, I would not store my Hours field/column this way to prevent having to search in this manner.
        # Instead I would break down columns by day and include the hours open per day of the week in this kind of
        # Data format. Then I would filter by column if hours match etc... I might have to think about that a little.
        all_restaurants = Restaurant.objects.all()

        open_restaurants = []

        for restaurant in all_restaurants:
            if cls.is_restaurant_open(restaurant, check_dt):
                open_restaurants.append(restaurant.name)

        return open_restaurants
