#include <stdint.h>

struct GermanBattleControllerSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
};

const struct GermanBattleControllerSymbol gGermanBattleControllerFoundation[] =
{
    { "HandleLinkBattleSetup", 0x0800BA2Cu, 0x0800BC0Cu },
    { "SetUpBattleVarsAndBirchPoochyena", 0x0800BA58u, 0x0800BC38u },
    { "sub_800B950", 0x0800BB24u, 0x0800BD40u },
    { "InitSinglePlayerBtlControllers", 0x0800BB7Cu, 0x0800BD98u },
    { "InitLinkBtlControllers", 0x0800BC4Cu, 0x0800BE68u },
    { "SetBattlePartyIds", 0x0800BF28u, 0x0800C144u },
    { "PrepareBufferDataTransfer", 0x0800C070u, 0x0800C28Cu },
    { "CreateTasksForSendRecvLinkBuffers", 0x0800C0FCu, 0x0800C318u },
    { "PrepareBufferDataTransferLink", 0x0800C1C4u, 0x0800C3E0u },
    { "Task_HandleSendLinkBuffersData", 0x0800C37Cu, 0x0800C598u },
    { "sub_800C35C", 0x0800C530u, 0x0800C74Cu },
    { "Task_HandleCopyReceivedLinkBuffersData", 0x0800C650u, 0x0800C86Cu },
    { "BtlController_EmitGetMonData", 0x0800C7ECu, 0x0800CA08u },
};

const unsigned int gGermanBattleControllerFoundationCount =
    sizeof(gGermanBattleControllerFoundation) /
    sizeof(gGermanBattleControllerFoundation[0]);
