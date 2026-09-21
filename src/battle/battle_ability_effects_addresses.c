#include <stdint.h>

struct GermanAbilityDispatcherBoundary
{
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint32_t retailSize;
    uint32_t debugSize;
};

const struct GermanAbilityDispatcherBoundary gGermanAbilityBattleEffects =
{
    0x080184F8u,
    0x0801B580u,
    7308u,
    8536u,
};

const uint32_t gGermanBattleScriptExecuteRetail = 0x0801A184u;
const uint32_t gGermanBattleScriptExecuteDebug = 0x0801D6D8u;
const uint32_t gGermanBattleScriptPushCursorCallbackRetail = 0x0801A1C0u;
const uint32_t gGermanBattleScriptPushCursorCallbackDebug = 0x0801D714u;
