#!/usr/bin/env python3
import argparse
import hashlib
import json
import struct
from pathlib import Path

REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
COUNT=248
PROFILES={
    "retail":{"sha1":REV1_SHA1,"table":0x20770C},
    "debug":{"sha1":DEBUG_SHA1,"table":0x2208A4},
}
NAMES=["atk00_attackcanceler","atk01_accuracycheck","atk02_attackstring","atk03_ppreduce","atk04_critcalc","atk05_damagecalc","atk06_typecalc","atk07_adjustnormaldamage","atk08_adjustnormaldamage2","atk09_attackanimation","atk0A_waitanimation","atk0B_healthbarupdate","atk0C_datahpupdate","atk0D_critmessage","atk0E_effectivenesssound","atk0F_resultmessage","atk10_printstring","atk11_printselectionstring","atk12_waitmessage","atk13_printfromtable","atk14_printselectionstringfromtable","atk15_seteffectwithchance","atk16_seteffectprimary","atk17_seteffectsecondary","atk18_clearstatusfromeffect","atk19_tryfaintmon","atk1A_dofaintanimation","atk1B_cleareffectsonfaint","atk1C_jumpifstatus","atk1D_jumpifstatus2","atk1E_jumpifability","atk1F_jumpifsideaffecting","atk20_jumpifstat","atk21_jumpifstatus3condition","atk22_jumpiftype","atk23_getexp","atk24","atk25_movevaluescleanup","atk26_setmultihit","atk27_decrementmultihit","atk28_goto","atk29_jumpifbyte","atk2A_jumpifhalfword","atk2B_jumpifword","atk2C_jumpifarrayequal","atk2D_jumpifarraynotequal","atk2E_setbyte","atk2F_addbyte","atk30_subbyte","atk31_copyarray","atk32_copyarraywithindex","atk33_orbyte","atk34_orhalfword","atk35_orword","atk36_bicbyte","atk37_bichalfword","atk38_bicword","atk39_pause","atk3A_waitstate","atk3B_healthbar_update","atk3C_return","atk3D_end","atk3E_end2","atk3F_end3","atk40_jumpifaffectedbyprotect","atk41_call","atk42_jumpiftype2","atk43_jumpifabilitypresent","atk44_endselectionscript","atk45_playanimation","atk46_playanimation2","atk47_setgraphicalstatchangevalues","atk48_playstatchangeanimation","atk49_moveend","atk4A_typecalc2","atk4B_returnatktoball","atk4C_getswitchedmondata","atk4D_switchindataupdate","atk4E_switchinanim","atk4F_jumpifcantswitch","atk50_openpartyscreen","atk51_switchhandleorder","atk52_switchineffects","atk53_trainerslidein","atk54_playse","atk55_fanfare","atk56_playfaintcry","atk57","atk58_returntoball","atk59_handlelearnnewmove","atk5A_yesnoboxlearnmove","atk5B_yesnoboxstoplearningmove","atk5C_hitanimation","atk5D_getmoneyreward","atk5E","atk5F_swapattackerwithtarget","atk60_incrementgamestat","atk61_drawpartystatussummary","atk62_hidepartystatussummary","atk63_jumptorandomattack","atk64_statusanimation","atk65_status2animation","atk66_chosenstatusanimation","atk67_yesnobox","atk68_cancelallactions","atk69_adjustsetdamage","atk6A_removeitem","atk6B_atknameinbuff1","atk6C_drawlvlupbox","atk6D_resetsentmonsvalue","atk6E_setatktoplayer0","atk6F_makevisible","atk70_recordlastability","atk71_buffermovetolearn","atk72_jumpifplayerran","atk73_hpthresholds","atk74_hpthresholds2","atk75_useitemonopponent","atk76_various","atk77_setprotectlike","atk78_faintifabilitynotdamp","atk79_setatkhptozero","atk7A_jumpifnexttargetvalid","atk7B_tryhealhalfhealth","atk7C_trymirrormove","atk7D_setrain","atk7E_setreflect","atk7F_setseeded","atk80_manipulatedamage","atk81_trysetrest","atk82_jumpifnotfirstturn","atk83_nop","atk84_jumpifcantmakeasleep","atk85_stockpile","atk86_stockpiletobasedamage","atk87_stockpiletohpheal","atk88_negativedamage","atk89_statbuffchange","atk8A_normalisebuffs","atk8B_setbide","atk8C_confuseifrepeatingattackends","atk8D_setmultihitcounter","atk8E_initmultihitstring","atk8F_forcerandomswitch","atk90_tryconversiontypechange","atk91_givepaydaymoney","atk92_setlightscreen","atk93_tryKO","atk94_damagetohalftargethp","atk95_setsandstorm","atk96_weatherdamage","atk97_tryinfatuating","atk98_updatestatusicon","atk99_setmist","atk9A_setfocusenergy","atk9B_transformdataexecution","atk9C_setsubstitute","atk9D_mimicattackcopy","atk9E_metronome","atk9F_dmgtolevel","atkA0_psywavedamageeffect","atkA1_counterdamagecalculator","atkA2_mirrorcoatdamagecalculator","atkA3_disablelastusedattack","atkA4_trysetencore","atkA5_painsplitdmgcalc","atkA6_settypetorandomresistance","atkA7_setalwayshitflag","atkA8_copymovepermanently","atkA9_trychoosesleeptalkmove","atkAA_setdestinybond","atkAB_trysetdestinybondtohappen","atkAC_remaininghptopower","atkAD_tryspiteppreduce","atkAE_healpartystatus","atkAF_cursetarget","atkB0_trysetspikes","atkB1_setforesight","atkB2_trysetperishsong","atkB3_rolloutdamagecalculation","atkB4_jumpifconfusedandstatmaxed","atkB5_furycuttercalc","atkB6_happinesstodamagecalculation","atkB7_presentdamagecalculation","atkB8_setsafeguard","atkB9_magnitudedamagecalculation","atkBA_jumpifnopursuitswitchdmg","atkBB_setsunny","atkBC_maxattackhalvehp","atkBD_copyfoestats","atkBE_rapidspinfree","atkBF_setdefensecurlbit","atkC0_recoverbasedonsunlight","atkC1_hiddenpowercalc","atkC2_selectfirstvalidtarget","atkC3_trysetfutureattack","atkC4_trydobeatup","atkC5_setsemiinvulnerablebit","atkC6_clearsemiinvulnerablebit","atkC7_setminimize","atkC8_sethail","atkC9_jumpifattackandspecialattackcannotfall","atkCA_setforcedtarget","atkCB_setcharge","atkCC_callenvironmentattack","atkCD_cureifburnedparalysedorpoisoned","atkCE_settorment","atkCF_jumpifnodamage","atkD0_settaunt","atkD1_trysethelpinghand","atkD2_tryswapitems","atkD3_trycopyability","atkD4_trywish","atkD5_trysetroots","atkD6_doubledamagedealtifdamaged","atkD7_setyawn","atkD8_setdamagetohealthdifference","atkD9_scaledamagebyhealthratio","atkDA_tryswapabilities","atkDB_tryimprison","atkDC_trysetgrudge","atkDD_weightdamagecalculation","atkDE_assistattackselect","atkDF_trysetmagiccoat","atkE0_trysetsnatch","atkE1_trygetintimidatetarget","atkE2_switchoutabilities","atkE3_jumpifhasnohp","atkE4_getsecretpowereffect","atkE5_pickup","atkE6_docastformchangeanimation","atkE7_trycastformdatachange","atkE8_settypebasedhalvers","atkE9_setweatherballtype","atkEA_tryrecycleitem","atkEB_settypetoenvironment","atkEC_pursuitrelated","atkEF_snatchsetbattlers","atkEE_removelightscreenreflect","atkEF_handleballthrow","atkF0_givecaughtmon","atkF1_trysetcaughtmondexflags","atkF2_displaydexinfo","atkF3_trygivecaughtmonnick","atkF4_subattackerhpbydmg","atkF5_removeattackerstatus1","atkF6_finishaction","atkF7_finishturn"]

def sha1(x): return hashlib.sha1(x).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument("--profile",choices=PROFILES,required=True)
    a=p.parse_args()
    data=a.rom.read_bytes()
    prof=PROFILES[a.profile]
    if sha1(data)!=prof["sha1"]:
        raise SystemExit("ROM SHA-1 does not match selected profile")
    result=[]
    for i,name in enumerate(NAMES):
        ptr=struct.unpack_from("<I",data,prof["table"]+4*i)[0]
        result.append({
            "id":i,
            "opcode":f"0x{i:02X}",
            "name":name,
            "thumb_pointer":f"0x{ptr:08X}",
            "entry":f"0x{ptr-1:08X}",
        })
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
