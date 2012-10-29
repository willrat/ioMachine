#!/bin/bash

# halcmd show pin machineOff				
# halcmd show pin machineOn				
# halcmd show pin isMachineOn				
# halcmd show pin runProgram				
# halcmd show pin isRunProgram			
# halcmd show pin isModeAuto				
# halcmd show pin isModeManual			
# halcmd show pin modeAuto				
# halcmd show pin modeManual				

halcmd show | grep -i isMachineOn

halcmd show | grep -i runProgram
halcmd show | grep -i isRunningSeen

halcmd show | grep -i cycleStatus
halcmd show | grep -i currentState


