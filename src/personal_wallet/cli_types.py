import datetime
import re
from gettext import ngettext

import click


class StringOrPatternParamType(click.types.StringParamType):
    name = "text or pattern"

    def convert(self, value, param, ctx) -> str | re.Pattern:
        if value.startswith("%") and value.endswith("%"):
            return re.compile(rf".*?{value[1:-1]}")
        if value.startswith("%"):
            return re.compile(rf".*?{value[1:]}$")
        if value.endswith("%"):
            return re.compile(rf"^{value[:-1]}.*?")
        return super().convert(value, param, ctx)

    def __repr__(self) -> str:
        return "STRING|Pattern"


class NonNegIntOrIntRangeParamType(click.types.ParamType):
    name = "non-negative integer or from..to integer range"

    def convert(self, value, param, ctx) -> int | tuple[int, int]:
        if isinstance(value, int):
            if value < 0:
                self.fail(f"{value!r} is not in the range x>=0.", param, ctx)
            return value

        try:
            # Value is single and positive int.
            if isinstance(value, float):
                raise ValueError
            if ".." not in value:
                if "." in value:
                    raise ValueError
                value = int(value)
                if value < 0:
                    self.fail(f"{value!r} is not in the range x>=0.", param, ctx)
                return value

            # It's a range of two values.
            values = value.split("..", 1)
            if len(values) != 2:
                raise ValueError

            # Values are positive int.
            nums = [int(num) for num in values]
            for num in nums:
                if num < 0:
                    self.fail(f"{num!r} is not in the range x>=0.", param, ctx)

            # From range <= To range.
            start, end = nums
            if start > end:
                self.fail(
                    f"start value {start!r} is greater than end value {end!r} in " f"integer range",
                    param,
                    ctx,
                )
            return start, end

        except ValueError:
            self.fail(f"{value!r} is not a valid integer or from..to integer range", param, ctx)

    def __repr__(self) -> str:
        return "INT|[INT..INT]"


class DateTimeOrDateTimeRange(click.types.DateTime):
    name = "datetime or from..to datetime range"

    def __init__(self, formats):
        super().__init__(formats)

    def convert(
        self, value, param, ctx
    ) -> datetime.datetime | tuple[datetime.datetime, datetime.datetime]:
        if isinstance(value, datetime.datetime):
            return value

        try:
            # Value is single and valid date.
            if ".." not in value:
                return super().convert(value, param, ctx)

            # It's a range of two values.
            values = value.split("..", 1)
            if len(values) != 2:
                raise ValueError

            # Values are valid dates.
            dates = []
            for val in values:
                for date_format in self.formats:
                    date = self._try_to_convert_date(val, date_format)
                    if date is not None:
                        dates.append(date)
                        break
            if len(dates) != 2:
                raise ValueError

            # From range <= To range.
            start, end = dates
            if start > end:
                self.fail(
                    f"start date is greater than end date in date range {value!r}.",
                    param,
                    ctx,
                )
            return start, end

        except ValueError:
            formats_str = ", ".join(map(repr, self.formats))
            self.fail(
                ngettext(
                    "{value!r} does not match the format {format} or from..to date range.",
                    "{value!r} does not match the formats {formats} or from..to date range.",
                    len(self.formats),
                ).format(value=value, format=formats_str, formats=formats_str),
                param,
                ctx,
            )

    def __repr__(self) -> str:
        return "DateTime|[DateTime..DateTime]"


NON_NEG_INT_OR_INT_RANGE = NonNegIntOrIntRangeParamType()
STRING_OR_PATTERN = StringOrPatternParamType()
