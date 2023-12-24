import pytest
from utilfile import utils
from datetime import datetime,timezone
class TestA:
    global asgname,region_name
    asgname = ''
    region_name = ''
    
    def test_verify_ASG_desire_running_count_is_same_as_running_instances(self):
         # 1- ASG desire running count should be same as running instances. if mismatch fails
        
        util = utils()
        response = util.get_asg_describe(asgname,region_name)
        
        all_asg = response['AutoScalingGroups'][0]
        actual_desired_capacity = all_asg['DesiredCapacity']
        instance_list = all_asg['Instances']
        actual_asg_instance_count = len(instance_list)

        expected_desired_capacity = 2
        assert actual_desired_capacity == expected_desired_capacity, "ASG desired capacity is not as expected."
        assert actual_asg_instance_count == expected_desired_capacity , "ASG desire count does not match with running instances count"

    def test_verify_instances_are_distributed_on_multiple_az_when_multiple_instances_running_in_asg(self):
        ''' 2- If more than 1 instance running on ASG, 
        then the ec2 instance should on available and distributed on multiple availibity zones. '''
        
        util = utils()
        response = util.get_asg_describe(asgname,region_name)
        
        all_asg = response['AutoScalingGroups'][0]
        actual_desired_capacity = all_asg['DesiredCapacity']
        instance_list = all_asg['Instances']
        asg_instance_count = len(instance_list)

        if asg_instance_count > 1:
            az_list = []
            message = ""
            for i in range(asg_instance_count):
                instance_az = instance_list[i]['AvailabilityZone']
                if instance_az not in az_list:
                    az_list.append(instance_az)
                _message += "instance: {} and az: {} ".format(instance_list[i]['InstanceId'],instance_az)
            
            is_az_distributed = True if len(az_list) > 1 else False
            assert is_az_distributed, "ec2 instance should on available and distributed on multiple availibity zones.\n"+_message
        else:
            assert actual_desired_capacity == 1, "ASG desired capacity should be 1"
            assert asg_instance_count == 1 , "ASG running instances count should be 1"

    def test_verify_sg_imageid_and_vpcid_are_same_for_all_instances_running_in_asg(self):
        '''3- SecuirtyGroup, ImageID and VPCID should be same on ASG running instances. Do not just print.'''

        util = utils()
        instances =  util.get_instances_from_asg(asgname,region_name)

        # verify ImageID,VPCID and SecuirtyGroup matches for all the instances in ASG
        imageid_first_instance = instances[0]['ImageId']
        vpcid_first_instance = instances[0]['VpcId']
        sec_group_id_first_instance = instances[0]['SecurityGroups'][0]['GroupId']
        sec_group_name_first_instance = instances[0]['SecurityGroups'][0]['GroupName']
        for i in range(1,len(instances)):
            message = "instance-1 : "+instances[0]['InstanceId']
            imageid = instances[i]['ImageId']
            vpcid = instances[i]['VpcId']
            sec_group_id = instances[i]['SecurityGroups'][0]['GroupId']
            sec_group_name = instances[i]['SecurityGroups'][0]['GroupName']
            message+= "instance-2 : "+instances[i]['InstanceId']

            assert imageid_first_instance == imageid,"ImageId does not match for instances in the asg.\n"+message
            assert vpcid_first_instance == vpcid,"VpcId does not match for instances in the asg.\n"+message
            assert sec_group_id_first_instance == sec_group_id,"SecurityGroup id does not match for instances in the asg.\n"+message
            assert sec_group_name_first_instance == sec_group_name,"SecurityGroup name does not match for instances in the asg.\n"+message

    def test_display_uptime_of_asg_running_instances_and_the_longest_running_instance(self):
        '''4- Findout uptime of ASG running instances and get the longest running instance.'''

        util = utils()
        instances = util.get_instances_from_asg(asgname,region_name)
        
        instances_with_uptime_in_minutes = "instances with uptime in minutes: "
        longest_running_instance_time_in_minutes = 0
        longest_running_instance_id = 0
        
        current_time = datetime.now(timezone.utc)
        for i in range(len(instances)):
            instance_uptime = instances[i]['UsageOperationUpdateTime']
            instanceid = instances[i]['InstanceId']
            timedelta = current_time-instance_uptime
            total_time_in_minutes = timedelta.total_seconds() / 60

            if total_time_in_minutes > longest_running_instance_time_in_minutes:
                longest_running_instance_time_in_minutes = total_time_in_minutes
                longest_running_instance_id = instanceid
            
            instances_with_uptime_in_minutes+= "\n "+str(instanceid)+" : uptime "+str(total_time_in_minutes)
        
        print("longest running instance : "+longest_running_instance_id)
        print("ASG running instances : \n"+instances_with_uptime_in_minutes)
        

        