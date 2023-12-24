import pytest
from utilfile import utils
from datetime import datetime,timezone,timedelta
class TestA:
    global asgname,region_name
    asgname = ''
    region_name = ''
    
    def _test_verify_ASG_desire_running_count_is_same_as_running_instances(self):
        ''' Find the Scheduled actions of the given ASG 
        which is going to run next and calculate elapsed in hh:mm: ss from the current time.'''

        _util = utils()
        _response = _util.get_scheduled_actions_describe(asgname,region_name)
        _scheduled_actions = _response['ScheduledUpdateGroupActions']
        _dic_elapsed_time = {}
        _current_time = datetime.now(timezone.utc)
        message = "next scheduled action and elapsed time in hh:mm: ss from current time. "
        for a in _scheduled_actions:
            _starttime = a['StartTime']
            _elapsed_time =  abs(_current_time - _starttime)
            message+= "action : "+a['ScheduledActionName']+"time : "+str(_elapsed_time)
        
        print(message)

        ''' output:
        'next scheduled action and elapsed time in hh:mm: ss from current time. 
        action : action1time : 13:21:17.889035action : action2time : 14:11:17.889035'
        '''

    def _test_verify_ASG_desire_running_count_is_same_as_running_instances(self):
        ''' Calculate the total number of instances launched and terminated on the current day for the given ASG. '''

        _util = utils()
        _start_date = datetime.now().date()
        _end_date = _start_date
        _launched_and_terminated_today = _util.get_activities_from_asg(asgname,region_name,_start_date,_end_date)
        
        msg1 = "total instances : "+ str(len(_launched_and_terminated_today))
        print("instances launched and terminated on the current day: "+msg1)
        msg2=""
        for i in _launched_and_terminated_today:
            msg2+= " StartTime : "+str(i['StartTime'])+" EndTime : "+str(i['EndTime'])
        print(" Start and End time : "+msg2)

        '''
        output:
        message1 - 
        'total instances : 2'

        message2 -  
        StartTime : 2023-12-24 00:50:01.661000+00:00 EndTime : 2023-12-24 00:50:01+00:00
        StartTime : 2023-12-24 00:00:05.893000+00:00 EndTime : 2023-12-24 00:00:05+00:00
        '''

        
    