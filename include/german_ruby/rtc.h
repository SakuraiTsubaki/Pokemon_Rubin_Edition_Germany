#ifndef GERMAN_RUBY_RTC_H
#define GERMAN_RUBY_RTC_H

#include <stdbool.h>
#include <stdint.h>

#define SIIRTCINFO_INTFE   0x01
#define SIIRTCINFO_INTME   0x02
#define SIIRTCINFO_INTAE   0x04
#define SIIRTCINFO_24HOUR  0x40
#define SIIRTCINFO_POWER   0x80

#define RTC_INIT_ERROR          0x0001
#define RTC_INIT_WARNING        0x0002
#define RTC_ERR_12HOUR_CLOCK    0x0010
#define RTC_ERR_POWER_FAILURE   0x0020
#define RTC_ERR_INVALID_YEAR    0x0040
#define RTC_ERR_INVALID_MONTH   0x0080
#define RTC_ERR_INVALID_DAY     0x0100
#define RTC_ERR_INVALID_HOUR    0x0200
#define RTC_ERR_INVALID_MINUTE  0x0400
#define RTC_ERR_INVALID_SECOND  0x0800
#define RTC_ERR_FLAG_MASK       0x0FF0

struct SiiRtcInfo
{
    uint8_t year;
    uint8_t month;
    uint8_t day;
    uint8_t dayOfWeek;
    uint8_t hour;
    uint8_t minute;
    uint8_t second;
    uint8_t status;
    uint8_t alarmHour;
    uint8_t alarmMinute;
};

void RtcDisableInterrupts(void);
void RtcRestoreInterrupts(void);
uint32_t ConvertBcdToBinary(uint8_t bcd);
bool IsLeapYear(uint8_t year);
uint16_t ConvertDateToDayCount(uint8_t year, uint8_t month, uint8_t day);
uint16_t RtcGetDayCount(struct SiiRtcInfo *rtc);
void RtcInit(void);
uint16_t RtcGetErrorStatus(void);
void RtcGetInfo(struct SiiRtcInfo *rtc);
void RtcGetDateTime(struct SiiRtcInfo *rtc);
void RtcGetStatus(struct SiiRtcInfo *rtc);
void RtcGetRawInfo(struct SiiRtcInfo *rtc);
uint16_t RtcCheckInfo(struct SiiRtcInfo *rtc);
void RtcReset(void);

#endif
