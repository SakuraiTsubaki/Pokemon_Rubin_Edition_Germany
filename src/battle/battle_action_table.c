#include "german_ruby/battle_actions.h"

const struct GermanBattleActionHandler gGermanBattleActionHandlers[GERMAN_B_ACTION_COUNT] =
{
    { 0, 0x080141BDu, 0x08017245u }, /* HandleAction_UseMove */
    { 1, 0x08014975u, 0x080179FDu }, /* HandleAction_UseItem */
    { 2, 0x080148C9u, 0x08017951u }, /* HandleAction_Switch */
    { 3, 0x08014DC9u, 0x08017E51u }, /* HandleAction_Run */
    { 4, 0x08014F25u, 0x08017FADu }, /* HandleAction_WatchesCarefully */
    { 5, 0x08014F6Du, 0x08017FF5u }, /* HandleAction_SafariZoneBallThrow */
    { 6, 0x08014FCDu, 0x08018055u }, /* HandleAction_ThrowPokeblock */
    { 7, 0x08015091u, 0x08018119u }, /* HandleAction_GoNear */
    { 8, 0x08015155u, 0x080181DDu }, /* HandleAction_SafriZoneRun */
    { 9, 0x08015191u, 0x08018219u }, /* HandleAction_Action9 */
    { 10, 0x0801B769u, 0x0801ECBDu }, /* sub_801B594: battle script action */
    { 11, 0x08015209u, 0x08018291u }, /* HandleAction_Action11 */
    { 12, 0x08015269u, 0x080182F1u }, /* HandleAction_ActionFinished */
    { 13, 0x08015235u, 0x080182BDu }, /* HandleAction_NothingIsFainted */
};
