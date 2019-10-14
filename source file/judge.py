#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Judge.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import re
import math
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import datetime
import time
from time import sleep


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
Judge_spec = ["implementation_id", "Judge", 
		 "type_name",         "Judge", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Shinden", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class Judge
# @brief ModuleDescription
# 
# 
class Judge(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		data_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_data = RTC.TimedString(*data_arg)
		"""
		"""
		self._dataIn = OpenRTM_aist.InPort("data", self._d_data)
		sign_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_sign = RTC.TimedString(*sign_arg)
		"""
		"""
		self._signIn = OpenRTM_aist.InPort("sign", self._d_sign)		
		result_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_result = RTC.TimedLong(*result_arg)
		"""
		"""
		self._resultOut = OpenRTM_aist.OutPort("result", self._d_result)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("data",self._dataIn)
		self.addInPort("sign",self._signIn)		
		# Set OutPort buffers
		self._resultOut = RTC.TimedLong(RTC.Time(0,0),0)
		self._outport = OpenRTM_aist.OutPort("out", self._resultOut)
		self.addOutPort("result",self._outport)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		#global
		global switch
		global countsign
		switch = "off"
		countsign = "yet"
		return RTC.RTC_OK


	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
		global switch
		print("activate Judge")
		switch = "off"
		
		
		
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
		print("deactivate Judge")
	
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
		#立ち上がり判定
		#データ読込
		global switch
		if self._signIn.isNew():
			self._d_sign = self._signIn.read()
			sign = self._d_sign.data
			print(sign)
			#data = re.split("[,']", sign_str)
			#signn = data[3]

			#print(signn)
			
			if sign == "kaishi":
				switch = "on"
				print("on")
			

		if switch == "on":
			line = self._dataIn.read()
		#print(line)
			line_str = str(line)
			data = re.split("[,']", line_str)
			FSR_dic = {}
			for i in range (1,16,1):
				FSR_dic.setdefault(("FSR" + str(i)), float(data[i+2]))
				#print(FSR_dic)
			print(FSR_dic)
			i = 0
			for i in range (1,16,1):
				if FSR_dic["FSR" + str(i)] == 0:
					FSR_dic["FSR" + str(i)] = 0
				elif (1 <= FSR_dic["FSR" + str(i)]) and (FSR_dic["FSR" + str(i)] < 990):
					FSR_dic["FSR" + str(i)] = 0.069*math.exp(0.0044*FSR_dic["FSR" + str(i)])*9.8 
				elif( 990 <= FSR_dic["FSR" + str(i)]) and (FSR_dic["FSR" + str(i)] <= 1024): 
					FSR_dic["FSR" + str(i)] = 3E-06*math.exp(0.0145*FSR_dic["FSR" + str(i)])*9.8
			print("oooooooooo", FSR_dic)

			FSR_left_front =  FSR_dic['FSR3'] + FSR_dic['FSR4'] + FSR_dic['FSR5'] + FSR_dic['FSR6']
			FSR_right_front =  FSR_dic['FSR9'] + FSR_dic['FSR10'] + FSR_dic['FSR11'] + FSR_dic['FSR12']
		#判定
			if FSR_dic["FSR5" ] > 20 :
				print(FSR_dic["FSR5"])
				self._resultOut.data = 1
				#OpenRTM_aist.setTimestamp(self._resultOut)
				print("Sending: ", self._resultOut.data)
				self._outport.write()
			elif FSR_left_front > FSR_right_front + 10:
				self._resultOut.data = 2
				#OpenRTM_aist.setTimestamp(self._resultOut)
				print("Sending: ", self._resultOut.data)
			elif FSR_right_front > FSR_left_front + 10:
				self._resultOut.data = 2
				#OpenRTM_aist.setTimestamp(self._resultOut)
				print("Sending: ", self._resultOut.data)

			else :
				self._resultOut.data = 0
				#OpenRTM_aist.setTimestamp(self._resultOut)
				print("Sending: ", self._resultOut.data)
				self._outport.write()


		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def JudgeInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=Judge_spec)
    manager.registerFactory(profile,
                            Judge,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    JudgeInit(manager)

    # Create a component
    comp = manager.createComponent("Judge")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

