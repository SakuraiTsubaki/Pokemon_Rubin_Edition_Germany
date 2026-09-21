#include <stdbool.h>
#include <stdint.h>

#if !defined(GERMAN_RUBY_REV0) && !defined(GERMAN_RUBY_REV1)
#error "Select GERMAN_RUBY_REV0 or GERMAN_RUBY_REV1"
#endif

#if defined(GERMAN_RUBY_REV0) && defined(GERMAN_RUBY_REV1)
#error "Select only one German retail revision"
#endif

static const int32_t sNumDaysInMonths[12] =
{
    31,
    28,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31,
};

/*
 * German retail ROM address: 0x08009314
 *
 * High-level reconstruction from the German binary. Build matching is not yet
 * claimed.
 */
bool IsLeapYear(uint8_t year)
{
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0)
        return true;

    return false;
}

/*
 * German retail ROM address: 0x0800934C
 *
 * Rev 0 and Rev 1 differ only in the lower bound of the first year loop.
 */
uint16_t ConvertDateToDayCount(uint8_t year, uint8_t month, uint8_t day)
{
    int32_t i;
    uint16_t dayCount = 0;

#if defined(GERMAN_RUBY_REV0)
    for (i = (int32_t)year - 1; i > 0; i--)
#else
    for (i = (int32_t)year - 1; i >= 0; i--)
#endif
    {
        dayCount += 365;

        if (IsLeapYear((uint8_t)i))
            dayCount++;
    }

    for (i = 0; i < (int32_t)month - 1; i++)
        dayCount += (uint16_t)sNumDaysInMonths[i];

    if (month > 2 && IsLeapYear(year))
        dayCount++;

    dayCount += day;
    return dayCount;
}
