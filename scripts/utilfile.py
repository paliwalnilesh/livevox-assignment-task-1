import boto3
import os
import sys

class utils:
    global aws_access_key_id,aws_secret_access_key,region_name
    aws_access_key_id=''
    aws_secret_access_key=''
    region_name = ''

    def get_asg_describe(self,asgname,region_name):
        asg_client = boto3.client('autoscaling',aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name)
        asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asgname])
        return asg_response
    
    def get_scaling_activities_describe(self,asgname,region_name):
        asg_client = boto3.client('autoscaling',aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name)
        asg_response = asg_client.describe_scaling_activities(AutoScalingGroupName = asgname)
        return asg_response
    
    def get_scheduled_actions_describe(self,asgname,region_name):
        asg_client = boto3.client('autoscaling',aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name)
        asg_response = asg_client.describe_scheduled_actions(AutoScalingGroupName = asgname)
        return asg_response 

    def get_instances_describe(self,InstanceIds,region_name):
        asg_client = boto3.client('ec2',aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name)
        asg_instances_response = asg_client.describe_instances(InstanceIds=InstanceIds)

        return asg_instances_response
    
    def get_instances_from_asg(self,asgname,region_name):
        response = self.get_asg_describe(asgname,region_name)
        all_asg = response['AutoScalingGroups'][0]
        instance_ids = [x['InstanceId'] for x in all_asg['Instances']]
        response_instance = self.get_instances_describe(instance_ids,region_name)
        instances =  [x['Instances'][0] for x in response_instance['Reservations']] 

        return instances

    def get_activities_from_asg(self,asgname,region_name,start_date,end_date):
        response = self.get_scaling_activities_describe(asgname,region_name)
        asg_activities = response['Activities']
        (asg_activities[0]['StartTime']).date()
        
        activities = list(
            filter(lambda x: 
                   (x['StartTime']).date() == start_date
                   and (x['EndTime']).date() == end_date
                   , asg_activities)
                   )

        return activities