#include <stdint.h>

/*
 * German Ruby new-game speech state map.
 *
 * Reconstruction scaffold: every entry is anchored to the supplied German
 * ROMs. Statement-level state bodies are promoted separately after German
 * text/data pointers and call targets are verified.
 */

struct NewGameSpeechStateInfo
{
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint8_t state;
};

const struct NewGameSpeechStateInfo gGermanNewGameSpeechStates[33] =
{
    { 0x0800A3C8u, 0x0800A5A8u, 1 },
    { 0x0800A4B4u, 0x0800A694u, 2 },
    { 0x0800A52Cu, 0x0800A70Cu, 3 },
    { 0x0800A59Cu, 0x0800A77Cu, 4 },
    { 0x0800A5E8u, 0x0800A7C8u, 5 },
    { 0x0800A618u, 0x0800A7F8u, 6 },
    { 0x0800A68Cu, 0x0800A86Cu, 7 },
    { 0x0800A6FCu, 0x0800A8DCu, 8 },
    { 0x0800A738u, 0x0800A918u, 9 },
    { 0x0800A780u, 0x0800A960u, 10 },
    { 0x0800A7F8u, 0x0800A9D8u, 11 },
    { 0x0800A83Cu, 0x0800AA1Cu, 12 },
    { 0x0800A8ECu, 0x0800AACCu, 13 },
    { 0x0800A930u, 0x0800AB10u, 14 },
    { 0x0800A970u, 0x0800AB50u, 15 },
    { 0x0800A9A8u, 0x0800AB88u, 16 },
    { 0x0800AA48u, 0x0800AC28u, 17 },
    { 0x0800AAF0u, 0x0800ACD0u, 18 },
    { 0x0800AB48u, 0x0800AD28u, 19 },
    { 0x0800AB88u, 0x0800AD68u, 20 },
    { 0x0800ABC0u, 0x0800ADA0u, 21 },
    { 0x0800AC80u, 0x0800AE60u, 22 },
    { 0x0800ACC0u, 0x0800AEA0u, 23 },
    { 0x0800AD0Cu, 0x0800AEECu, 24 },
    { 0x0800AD44u, 0x0800AF24u, 25 },
    { 0x0800ADF4u, 0x0800AFD4u, 26 },
    { 0x0800AE2Cu, 0x0800B00Cu, 27 },
    { 0x0800AF1Cu, 0x0800B0FCu, 28 },
    { 0x0800AFC8u, 0x0800B1A8u, 29 },
    { 0x0800B0A8u, 0x0800B288u, 30 },
    { 0x0800B158u, 0x0800B338u, 31 },
    { 0x0800B194u, 0x0800B374u, 32 },
    { 0x0800B208u, 0x0800B3E8u, 33 },
};

/*
 * Verified boundaries:
 * retail 0x0800A3C8..0x0800B233
 * debug  0x0800A5A8..0x0800B413
 * next function: 0x0800B234 retail / 0x0800B414 debug
 */
