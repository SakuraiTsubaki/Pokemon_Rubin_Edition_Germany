#!/usr/bin/env python3
import argparse, hashlib, json, struct
from pathlib import Path

REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
NAMES=["OpponentHandleGetAttributes","OpponentHandlecmd1","OpponentHandleSetAttributes","OpponentHandlecmd3","OpponentHandleLoadPokeSprite","OpponentHandleSendOutPoke","OpponentHandleReturnPokeToBall","OpponentHandleTrainerThrow","OpponentHandleTrainerSlide","OpponentHandleTrainerSlideBack","OpponentHandlecmd10","OpponentHandlecmd11","OpponentHandlecmd12","OpponentHandleBallThrow","OpponentHandlePuase","OpponentHandleMoveAnimation","OpponentHandlePrintString","OpponentHandlePrintStringPlayerOnly","OpponentHandlecmd18","OpponentHandlecmd19","OpponentHandlecmd20","OpponentHandleOpenBag","OpponentHandlecmd22","OpponentHandlecmd23","OpponentHandleHealthBarUpdate","OpponentHandleExpBarUpdate","OpponentHandleStatusIconUpdate","OpponentHandleStatusAnimation","OpponentHandleStatusXor","OpponentHandlecmd29","OpponentHandleDMATransfer","OpponentHandlecmd31","OpponentHandlecmd32","OpponentHandlecmd33","OpponentHandlecmd34","OpponentHandlecmd35","OpponentHandlecmd36","OpponentHandlecmd37","OpponentHandlecmd38","OpponentHandlecmd39","OpponentHandlecmd40","OpponentHandleHitAnimation","OpponentHandlecmd42","OpponentHandleEffectivenessSound","OpponentHandlecmd44","OpponentHandleFaintingCry","OpponentHandleIntroSlide","OpponentHandleTrainerBallThrow","OpponentHandlecmd48","OpponentHandlecmd49","OpponentHandlecmd50","OpponentHandleSpriteInvisibility","OpponentHandleBattleAnimation","OpponentHandleLinkStandbyMsg","OpponentHandleResetActionMoveSelection","OpponentHandlecmd55","OpponentHandlecmd56"]
PROFILES={
 "retail":{"sha1":REV1_SHA1,"table":0x207F2C},
 "debug":{"sha1":DEBUG_SHA1,"table":0x2210C4},
}

def sha1(x): return hashlib.sha1(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("rom",type=Path)
 p.add_argument("--profile",choices=PROFILES,required=True)
 a=p.parse_args(); data=a.rom.read_bytes(); prof=PROFILES[a.profile]
 if sha1(data)!=prof["sha1"]: raise SystemExit("ROM SHA-1 mismatch")
 rows=[]
 for i,name in enumerate(NAMES):
  ptr=struct.unpack_from("<I",data,prof["table"]+4*i)[0]
  rows.append({"command":i,"command_hex":f"0x{i:02X}","name":name,"thumb_pointer":f"0x{ptr:08X}","entry":f"0x{ptr-1:08X}"})
 print(json.dumps(rows,indent=2))
if __name__=="__main__": main()
