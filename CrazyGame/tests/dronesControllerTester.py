#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from fixSysPath import test_sys_path
test_sys_path()
from CrazyGame import logger
from CrazyGame.dronesController import DronesController

cf_logger = logger.get_logger(__name__) # debug(), info(), warning(), error(), exception(), critical()

COMMANDS = ["crazyflie2$Register", "crazyflie3$Register", "crazyflie2$TakeOff$7$7", "crazyflie3$TakeOff$3$3",
            "crazyflie3$UP", "crazyflie2$UP", "crazyflie3$UP", "crazyflie2$UP", "crazyflie3$DOWN", "crazyflie2$DOWN",
			"crazyflie3$LEFT", "crazyflie2$DOWN", "crazyflie3$DOWN", "crazyflie2$UP", "crazyflie3$DOWN", "crazyflie2$DOWN",
			"crazyflie3$RIGHT", "crazyflie3$UP",
            "crazyflie2$Land", "crazyflie3$Land", "crazyflie2$UnRegister", "crazyflie3$UnRegister"]

def main():
	dronesController = DronesController() # Optional variables: "ip", "port" and "buffer_size"
	if not dronesController.connect(number_of_trials=5, time_between_trails=3):
		cf_logger.critical("Communication error")
		return
	for command in COMMANDS:
		loop_status = dronesController.send(command) # Return 0 on success, 1 if the VM report on an error and -1 if the connection is closed
		if loop_status == 1:
			cf_logger.error("dronesControllerTester: Failed to execute command: {}".format(command))
		elif loop_status == -1:
			cf_logger.critical("Communication error")
			exit(0)
		time.sleep(1)
	dronesController.disconnect()

if __name__ == "__main__":
	cf_logger.info("######################################################")
	cf_logger.info("####                   Started                    ####")
	cf_logger.info("######################################################")
	main()
