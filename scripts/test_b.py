import pytest
from utilfile import utils
from datetime import datetime,timezone,timedelta
class TestA:
    global asgname,region_name
    asgname = ''
    region_name = ''
    
    def test_verify_ASG_desire_running_count_is_same_as_running_instances(self):
        ''' Find the Scheduled actions of the given ASG 
        which is going to run next and calculate elapsed in hh:mm: ss from the current time.'''

        util = utils()
        response = util.get_scheduled_actions_describe(asgname,region_name)
        scheduled_actions = response['ScheduledUpdateGroupActions']
        dic_elapsed_time = {}
        current_time = datetime.now(timezone.utc)
        message = "next scheduled action and elapsed time in hh:mm: ss from current time. "
        for a in scheduled_actions:
            starttime = a['StartTime']
            elapsed_time =  abs(current_time - starttime)
            message+= "action : "+a['ScheduledActionName']+"time : "+str(elapsed_time)
        
        print(message)

        ''' output:
        'next scheduled action and elapsed time in hh:mm: ss from current time. 
        action : action1time : 13:21:17.889035action : action2time : 14:11:17.889035'
        '''

    def test_verify_ASG_desire_running_count_is_same_as_running_instances(self):
        ''' Calculate the total number of instances launched and terminated on the current day for the given ASG. '''

        util = utils()
        start_date = datetime.now().date()
        end_date = start_date
        launched_and_terminated_today = util.get_activities_from_asg(asgname,region_name,start_date,end_date)
        
        msg1 = "total instances : "+ str(len(launched_and_terminated_today))
        print("instances launched and terminated on the current day: "+msg1)
        msg2=""
        for i in launched_and_terminated_today:
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

        
    