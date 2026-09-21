#ifndef GERMAN_RUBY_BATTLE_ACTIONS_H
#define GERMAN_RUBY_BATTLE_ACTIONS_H

#include <stdint.h>

enum GermanBattleActionId
{
    GERMAN_B_ACTION_0 = 0, /* HandleAction_UseMove */
    GERMAN_B_ACTION_1 = 1, /* HandleAction_UseItem */
    GERMAN_B_ACTION_2 = 2, /* HandleAction_Switch */
    GERMAN_B_ACTION_3 = 3, /* HandleAction_Run */
    GERMAN_B_ACTION_4 = 4, /* HandleAction_WatchesCarefully */
    GERMAN_B_ACTION_5 = 5, /* HandleAction_SafariZoneBallThrow */
    GERMAN_B_ACTION_6 = 6, /* HandleAction_ThrowPokeblock */
    GERMAN_B_ACTION_7 = 7, /* HandleAction_GoNear */
    GERMAN_B_ACTION_8 = 8, /* HandleAction_SafriZoneRun */
    GERMAN_B_ACTION_9 = 9, /* HandleAction_Action9 */
    GERMAN_B_ACTION_10 = 10, /* sub_801B594: battle script action */
    GERMAN_B_ACTION_11 = 11, /* HandleAction_Action11 */
    GERMAN_B_ACTION_12 = 12, /* HandleAction_ActionFinished */
    GERMAN_B_ACTION_13 = 13, /* HandleAction_NothingIsFainted */
    GERMAN_B_ACTION_COUNT = 14
};

struct GermanBattleActionHandler
{
    uint8_t actionId;
    uint32_t retailThumbPointer;
    uint32_t debugThumbPointer;
};

extern const struct GermanBattleActionHandler gGermanBattleActionHandlers[GERMAN_B_ACTION_COUNT];

#endif
