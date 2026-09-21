#include "german_ruby/rtc.h"

#define REG_IME (*(volatile uint16_t *)0x04000208u)

/* German retail RAM addresses recovered from literal pools. */
static uint16_t sErrorStatus;      /* 0x03000458 */
static struct SiiRtcInfo sRtc;     /* 0x03000460 */
static uint8_t sProbeResult;       /* 0x0300046C */
static uint16_t sSavedIme;         /* 0x0300046E */

/* ROM 0x081F458C: year 0, January 1, remaining fields zero. */
static const struct SiiRtcInfo sRtcDummy = {0, 1, 1, 0, 0, 0, 0, 0, 0, 0};

/* External RTC-library entry points observed in the German retail binary. */
extern void SiiRtcUnprotect(void);  /* 0x081ECE84 */
extern uint8_t SiiRtcProbe(void);   /* 0x081ECEB4 */
extern bool SiiRtcReset(void);      /* 0x081ECF8C */
extern bool SiiRtcGetStatus(struct SiiRtcInfo *rtc);   /* 0x081ED010 */
extern bool SiiRtcGetDateTime(struct SiiRtcInfo *rtc); /* 0x081ED184 */

/* German retail ROM 0x080092C0. */
void RtcDisableInterrupts(void)
{
    sSavedIme = REG_IME;
    REG_IME = 0;
}

/* German retail ROM 0x080092D8. */
void RtcRestoreInterrupts(void)
{
    REG_IME = sSavedIme;
}

/* German retail ROM 0x080092EC. */
uint32_t ConvertBcdToBinary(uint8_t bcd)
{
    if (bcd > 0x9F)
        return 0xFF;

    if ((bcd & 0xF) <= 9)
        return 10 * ((bcd >> 4) & 0xF) + (bcd & 0xF);

    return 0xFF;
}

static const int32_t sNumDaysInMonths[12] =
{
    31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
};

/* German retail ROM 0x08009314. */
bool IsLeapYear(uint8_t year)
{
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0)
        return true;

    return false;
}

/* German retail ROM 0x0800934C. */
uint16_t ConvertDateToDayCount(uint8_t year, uint8_t month, uint8_t day)
{
    int32_t i;
    uint16_t dayCount = 0;

#if defined(GERMAN_RUBY_REV0)
    for (i = (int32_t)year - 1; i > 0; i--)
#elif defined(GERMAN_RUBY_REV1)
    for (i = (int32_t)year - 1; i >= 0; i--)
#else
#error "Select GERMAN_RUBY_REV0 or GERMAN_RUBY_REV1"
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

/* German retail ROM 0x080093D8. */
uint16_t RtcGetDayCount(struct SiiRtcInfo *rtc)
{
    uint8_t year = (uint8_t)ConvertBcdToBinary(rtc->year);
    uint8_t month = (uint8_t)ConvertBcdToBinary(rtc->month);
    uint8_t day = (uint8_t)ConvertBcdToBinary(rtc->day);

    return ConvertDateToDayCount(year, month, day);
}

/* German retail ROM 0x08009414. */
void RtcInit(void)
{
    sErrorStatus = 0;

    RtcDisableInterrupts();
    SiiRtcUnprotect();
    sProbeResult = SiiRtcProbe();
    RtcRestoreInterrupts();

    if (!(sProbeResult & 0x0F))
    {
        sErrorStatus = RTC_INIT_ERROR;
        return;
    }

    if (sProbeResult & 0xF0)
        sErrorStatus = RTC_INIT_WARNING;
    else
        sErrorStatus = 0;

    RtcGetRawInfo(&sRtc);
    sErrorStatus = RtcCheckInfo(&sRtc);
}

/* German retail ROM 0x08009474. */
uint16_t RtcGetErrorStatus(void)
{
    return sErrorStatus;
}

/* German retail ROM 0x08009480. */
void RtcGetInfo(struct SiiRtcInfo *rtc)
{
    if (sErrorStatus & RTC_ERR_FLAG_MASK)
        *rtc = sRtcDummy;
    else
        RtcGetRawInfo(rtc);
}

/* German retail ROM 0x080094B0. */
void RtcGetDateTime(struct SiiRtcInfo *rtc)
{
    RtcDisableInterrupts();
    SiiRtcGetDateTime(rtc);
    RtcRestoreInterrupts();
}

/* German retail ROM 0x080094C8. */
void RtcGetStatus(struct SiiRtcInfo *rtc)
{
    RtcDisableInterrupts();
    SiiRtcGetStatus(rtc);
    RtcRestoreInterrupts();
}

/* German retail ROM 0x080094E0. */
void RtcGetRawInfo(struct SiiRtcInfo *rtc)
{
    RtcGetStatus(rtc);
    RtcGetDateTime(rtc);
}

/* German retail ROM 0x080094F4. */
uint16_t RtcCheckInfo(struct SiiRtcInfo *rtc)
{
    uint16_t errorFlags = 0;
    int32_t year;
    int32_t month;
    int32_t value;

    if (rtc->status & SIIRTCINFO_POWER)
        errorFlags |= RTC_ERR_POWER_FAILURE;

    if (!(rtc->status & SIIRTCINFO_24HOUR))
        errorFlags |= RTC_ERR_12HOUR_CLOCK;

    year = (int32_t)ConvertBcdToBinary(rtc->year);
    if (year == 0xFF)
        errorFlags |= RTC_ERR_INVALID_YEAR;

    month = (int32_t)ConvertBcdToBinary(rtc->month);
    if (month == 0xFF || month == 0 || month > 12)
        errorFlags |= RTC_ERR_INVALID_MONTH;

    value = (int32_t)ConvertBcdToBinary(rtc->day);
    if (value == 0xFF)
        errorFlags |= RTC_ERR_INVALID_DAY;

    if (month == 2)
    {
        if (value > (int32_t)IsLeapYear((uint8_t)year) + sNumDaysInMonths[month - 1])
            errorFlags |= RTC_ERR_INVALID_DAY;
    }
    else
    {
        if (value > sNumDaysInMonths[month - 1])
            errorFlags |= RTC_ERR_INVALID_DAY;
    }

    value = (int32_t)ConvertBcdToBinary(rtc->hour);
    if (value > 24)
        errorFlags |= RTC_ERR_INVALID_HOUR;

    value = (int32_t)ConvertBcdToBinary(rtc->minute);
    if (value > 60)
        errorFlags |= RTC_ERR_INVALID_MINUTE;

    value = (int32_t)ConvertBcdToBinary(rtc->second);
    if (value > 60)
        errorFlags |= RTC_ERR_INVALID_SECOND;

    return errorFlags;
}

/* German retail ROM 0x080095F4. */
void RtcReset(void)
{
    RtcDisableInterrupts();
    SiiRtcReset();
    RtcRestoreInterrupts();
}
