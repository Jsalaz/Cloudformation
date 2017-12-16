'''
Created on Oct 27, 2017

@author: j_sal
'''

from troposphere import Template, Output, Join, Ref, Parameter, Tags
from troposphere.s3 import Bucket, LifecycleConfiguration, LifecycleRule, LifecycleRuleTransition, BucketPolicy
import troposphere.s3 as s3
import sys, json, os


template = Template()

template.add_description(
    "This is an test of how to create an S3 bucket with Cloudformation "
    "I will try to make adding policies functions for lifeCycle policies "
    "Date 10-27-2017"
    )


bucketName= template.add_parameter(Parameter(
    "BucketName",
    Description = "My s3 Bucket Name",
    Type= "String",
    Default = "jhs-personal-bucket"
    ))


def CreateLifecycleRuleTransition(storageClass, transitionInDays):
    transition= s3.LifecycleRuleTransition(
        StorageClass = storageClass,
        TransitionInDays = transitionInDays
        )
    return (transition)


lifeCycleRules = []
def CreateLifeCycleRules(id, prefix, expirationInDay, status, transitions=None):
    if (transitions != None):
        myRule = s3.LifecycleRule(
            Id = id,
            Prefix = prefix,
            ExpirationInDays = expirationInDay,
            Status = status,
            Transitions = transitions
        )
    else:
        myRule = s3.LifecycleRule(
            Id = id,
            Prefix = prefix,
            ExpirationInDays = expirationInDay,
            Status = status
        )
    return (myRule)


lifeCycleRules.append(CreateLifeCycleRules("Christina", "/Christina/Pics", "3650", "Enabled"))
lifeCycleRules.append(CreateLifeCycleRules("Jorge", "/Jorge/Pics", "3650", "Enabled"))
lifeCycleRules.append(CreateLifeCycleRules("Hazel", "/Hazel/Pics", "3650", "Enabled"))

# miscTransitions = []
# lifeCycleRules.append(CreateLifeCycleRules("Misc", "/Misc/Pics", "3650", "Enabled", miscTransitions))
# miscTransitions.append(CreateLifecycleRuleTransition("STANDARD_IA", "90"))
# miscTransitions.append(CreateLifecycleRuleTransition("GLACIER", "365"))


lifeCycleConfiguration = s3.LifecycleConfiguration(
    Rules = lifeCycleRules
    )


template.add_resource(Bucket(
    "JHSBucket",
    BucketName = Ref(bucketName),
    LifecycleConfiguration = lifeCycleConfiguration
    ))


#Adding Output By Passing Object
myOutput = Output("JHSBucketName")
myOutput.Description = "This is the name of personal bucket"
myOutput.Value = Ref(bucketName)
template.add_output(myOutput)


#Adding Output Directly
template.add_output(Output(
    "DirectOutput",
    Description = "This is an alternative form of adding outputs",
    Value = Join("", ["BucketName is ", Ref(bucketName), " On S3"])
    ))


def CreateTemplate(filename, t):
    os.chdir("..")
    try:
        os.mkdir("templates")
    except OSError as exc:
        print("Template directory already exists. It will be overriden")
    finally:
        os.chdir("templates")
        with open(filename+".json", "w") as outfile:
            outfile.write(template.to_json())
            outfile.close()
        print("CloudFormation template created at %s\\" %os.getcwd())


baseFile=os.path.splitext((os.path.basename(__file__)))[0]
CreateTemplate(baseFile, template)

# fullPath=os.getcwd()
# print(os.getcwd())
# os.chdir("..")
# print(os.getcwd())
# #os.mkdir("templates")
# #os.chdir("templates2")
# print(os.getcwd())
# print("Cloudformation template could not be saved.")