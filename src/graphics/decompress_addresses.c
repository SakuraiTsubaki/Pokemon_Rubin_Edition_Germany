#include <stdint.h>

struct GermanDecompressSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t codeSize;
};

const struct GermanDecompressSymbol gGermanDecompressSymbols[] =
{
    { "LZDecompressWram", 0x0800D40Cu, 0x0800D628u, 12 },
    { "LZDecompressVram", 0x0800D418u, 0x0800D634u, 12 },
    { "LoadCompressedObjectPic", 0x0800D424u, 0x0800D640u, 44 },
    { "LoadCompressedObjectPicOverrideBuffer", 0x0800D450u, 0x0800D66Cu, 40 },
    { "LoadCompressedObjectPalette", 0x0800D478u, 0x0800D694u, 52 },
    { "LoadCompressedObjectPaletteOverrideBuffer", 0x0800D4ACu, 0x0800D6C8u, 48 },
    { "DecompressPicFromTable_2", 0x0800D4DCu, 0x0800D6F8u, 44 },
    { "HandleLoadSpecialPokePic", 0x0800D508u, 0x0800D724u, 68 },
    { "LoadSpecialPokePic", 0x0800D54Cu, 0x0800D768u, 168 },
    { "Unused_LZDecompressWramIndirect", 0x0800D5F4u, 0x0800D810u, 12 },
    { "unref_sub_800D42C", 0x0800D600u, 0x0800D81Cu, 600 },
};

const unsigned int gGermanDecompressSymbolCount =
    sizeof(gGermanDecompressSymbols) / sizeof(gGermanDecompressSymbols[0]);
