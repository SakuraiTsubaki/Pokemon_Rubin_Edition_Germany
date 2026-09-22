#!/usr/bin/env python3
import argparse, hashlib, json, struct
from pathlib import Path

REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
NAMES=["PlayerHandleGetAttributes","PlayerHandleGetRawMonData","PlayerHandleSetAttributes","PlayerHandlecmd3","PlayerHandleLoadPokeSprite","PlayerHandleSendOutPoke","PlayerHandleReturnPokeToBall","PlayerHandleTrainerThrow","PlayerHandleTrainerSlide","PlayerHandleTrainerSlideBack","PlayerHandlecmd10","PlayerHandlecmd11","PlayerHandlecmd12","PlayerHandleBallThrow","PlayerHandlePuase","PlayerHandleMoveAnimation","PlayerHandlePrintString","PlayerHandlePrintStringPlayerOnly","PlayerHandlecmd18","PlayerHandlecmd19","PlayerHandlecmd20","PlayerHandleOpenBag","PlayerHandlecmd22","PlayerHandlecmd23","PlayerHandleHealthBarUpdate","PlayerHandleExpBarUpdate","PlayerHandleStatusIconUpdate","PlayerHandleStatusAnimation","PlayerHandleStatusXor","PlayerHandlecmd29","PlayerHandleDMATransfer","PlayerHandlecmd31","PlayerHandlecmd32","PlayerHandlecmd33","PlayerHandlecmd34","PlayerHandlecmd35","PlayerHandlecmd36","PlayerHandlecmd37","PlayerHandlecmd38","PlayerHandlecmd39","PlayerHandlecmd40","PlayerHandleHitAnimation","PlayerHandlecmd42","PlayerHandleEffectivenessSound","PlayerHandlecmd44","PlayerHandleFaintingCry","PlayerHandleIntroSlide","PlayerHandleTrainerBallThrow","PlayerHandlecmd48","PlayerHandlecmd49","PlayerHandlecmd50","PlayerHandleSpriteInvisibility","PlayerHandleBattleAnimation","PlayerHandleLinkStandbyMsg","PlayerHandleResetActionMoveSelection","PlayerHandlecmd55","PlayerHandlecmd56"]
PROFILES={
 "retail":{"sha1":REV1_SHA1,"table":0x207D68},
 "debug":{"sha1":DEBUG_SHA1,"table":0x220F00},
}

def sha1(x): return hashlib.sha1(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("rom",type=Path)
 p.add_argument("--profile",choices=PROFILES,required=True)
 a=p.parse_args()
 data=a.rom.read_bytes(); prof=PROFILES[a.profile]
 if sha1(data)!=prof["sha1"]: raise SystemExit("ROM SHA-1 mismatch")
 rows=[]
 for i,name in enumerate(NAMES):
  ptr=struct.unpack_from("<I",data,prof["table"]+4*i)[0]
  rows.append({"command":i,"command_hex":f"0x{i:02X}","name":name,"thumb_pointer":f"0x{ptr:08X}","entry":f"0x{ptr-1:08X}"})
 print(json.dumps(rows,indent=2))
if __name__=="__main__": main()
