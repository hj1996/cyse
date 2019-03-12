import time
import downdetector_graber
import internettrafficreport_graber
import Isitdown_graber
import istheservicedown
import outage_report_grabber
import data.combiner_v2

while 1==1:
	downdetector_graber.downdetector()
	internettrafficreport_graber.internettrafficreport()
	Isitdown_graber.isitdown()
	istheservicedown.istheservicedown()
	outage_report_grabber.outage()
	data.combiner_v2.combiner()
	time.sleep(900)