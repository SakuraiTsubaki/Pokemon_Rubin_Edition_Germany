#ifndef GERMAN_RUBY_MAIN_MENU_H
#define GERMAN_RUBY_MAIN_MENU_H

#include <stdbool.h>
#include <stdint.h>

typedef void (*TaskFunc)(uint8_t taskId);

struct Task
{
    TaskFunc func;
    uint8_t isActive;
    uint8_t prev;
    uint8_t next;
    uint8_t priority;
    int16_t data[16];
};

void CB2_MainMenu(void);
void VBlankCB_MainMenu(void);
void CB2_InitMainMenu(void);

#endif
