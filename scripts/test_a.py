import pytest
from utilfile import utils
from datetime import datetime,timezone
class TestA:
    global asgname,region_name
    asgname = ''
    region_name = ''
    
    def _test_verify_ASG_desire_running_count_is_same_as_running_instances(self):
         # 1- ASG desire running count should be same as running instances. if mismatch fails
        
        _util = utils()
        _response = _util.get_asg_describe(asgname,region_name)
        
        _all_asg = _response['AutoScalingGroups'][0]
        _actual_desired_capacity = _all_asg['DesiredCapacity']
        _instance_list = _all_asg['Instances']
        _actual_asg_instance_count = len(_instance_list)

        _expected_desired_capacity = 2
        assert _actual_desired_capacity == _expected_desired_capacity, "ASG desired capacity is not as expected."
        assert _actual_asg_instance_count == _expected_desired_capacity , "ASG desire count does not match with running instances count"

    def _test_verify_instances_are_distributed_on_multiple_az_when_multiple_instances_running_in_asg(self):
        ''' 2- If more than 1 instance running on ASG, 
        then the ec2 instance should on available and distributed on multiple availibity zones. '''
        
        _util = utils()
        _response = _util.get_asg_describe(asgname,region_name)
        
        _all_asg = _response['AutoScalingGroups'][0]
        _actual_desired_capacity = _all_asg['DesiredCapacity']
        _instance_list = _all_asg['Instances']
        _asg_instance_count = len(_instance_list)

        if _asg_instance_count > 1:
            _az_list = []
            _message = ""
            for i in range(_asg_instance_count):
                _instance_az = _instance_list[i]['AvailabilityZone']
                if _instance_az not in _az_list:
                    _az_list.append(_instance_az)
                _message += "instance: {} and az: {} ".format(_instance_list[i]['InstanceId'],_instance_az)
            
            is_az_distributed = True if len(_az_list) > 1 else False
            assert is_az_distributed, "ec2 instance should on available and distributed on multiple availibity zones.\n"+_message
        else:
            assert _actual_desired_capacity == 1, "ASG desired capacity should be 1"
            assert _asg_instance_count == 1 , "ASG running instances count should be 1"

    def _test_verify_sg_imageid_and_vpcid_are_same_for_all_instances_running_in_asg(self):
        '''3- SecuirtyGroup, ImageID and VPCID should be same on ASG running instances. Do not just print.'''

        _util = utils()
        _instances =  _util.get_instances_from_asg(asgname,region_name)

        # verify ImageID,VPCID and SecuirtyGroup matches for all the instances in ASG
        _imageid_first_instance = _instances[0]['ImageId']
        _vpcid_first_instance = _instances[0]['VpcId']
        _Sec_group_id_first_instance = _instances[0]['SecurityGroups'][0]['GroupId']
        _Sec_group_name_first_instance = _instances[0]['SecurityGroups'][0]['GroupName']
        for i in range(1,len(_instances)):
            message = "instance-1 : "+_instances[0]['InstanceId']
            _imageid = _instances[i]['ImageId']
            _vpcid = _instances[i]['VpcId']
            _Sec_group_id = _instances[i]['SecurityGroups'][0]['GroupId']
            _Sec_group_name = _instances[i]['SecurityGroups'][0]['GroupName']
            message+= "instance-2 : "+_instances[i]['InstanceId']

            assert _imageid_first_instance == _imageid,"ImageId does not match for instances in the asg.\n"+message
            assert _vpcid_first_instance == _vpcid,"VpcId does not match for instances in the asg.\n"+message
            assert _Sec_group_id_first_instance == _Sec_group_id,"SecurityGroup id does not match for instances in the asg.\n"+message
            assert _Sec_group_name_first_instance == _Sec_group_name,"SecurityGroup name does not match for instances in the asg.\n"+message

    def test_display_uptime_of_asg_running_instances_and_the_longest_running_instance(self):
        '''4- Findout uptime of ASG running instances and get the longest running instance.'''

        _util = utils()
        _instances = _util.get_instances_from_asg(asgname,region_name)
        
        _instances_with_uptime_in_minutes = "instances with uptime in minutes: "
        _longest_running_instance_time_in_minutes = 0
        _longest_running_instance_id = 0
        
        _current_time = datetime.now(timezone.utc)
        for i in range(len(_instances)):
            _instance_uptime = _instances[i]['UsageOperationUpdateTime']
            _instanceid = _instances[i]['InstanceId']
            _timedelta = _current_time-_instance_uptime
            _total_time_in_minutes = _timedelta.total_seconds() / 60

            if _total_time_in_minutes > _longest_running_instance_time_in_minutes:
                _longest_running_instance_time_in_minutes = _total_time_in_minutes
                _longest_running_instance_id = _instanceid
            
            _instances_with_uptime_in_minutes+= "\n "+str(_instanceid)+" : uptime "+str(_total_time_in_minutes)
        
        print("longest running instance : "+_longest_running_instance_id)
        print("ASG running instances : \n"+_instances_with_uptime_in_minutes)
        

        