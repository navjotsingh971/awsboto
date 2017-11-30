#!/bin/python2
import boto3
print '''

       press '1' show all running instances 
       press '2' launch instance
       press '3' terminate instance


   '''



s= raw_input("enter the number ")
aakey=raw_input("enter the access key ")
askey=raw_input("enter the secret key ")


def fun():
  client = boto3.client('ec2',region_name='{0}'.format(reg),aws_access_key_id='%s'%(aakey),aws_secret_access_key='%s'%(askey))
  return client 

def image(client):                          ###########  image function     #################
    

     response = client.describe_images(
             Filters=[
           {
            'Name': 'name',
            'Values': [
                 'amzn-ami-hvm-2017.09.1.20171120-x86_64-gp2',
                 'RHEL-7.4_HVM_GA-20170808-x86_64-2-Hourly2-GP2',
                 'ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-20171121.1',

             ],

           },
          ]
       )

    
     aimageid=response['Images'][0]['ImageId']
     rimageid=response['Images'][1]['ImageId']
     uimageid=response['Images'][2]['ImageId']
     return aimageid,rimageid,uimageid


def launch(client,imageid,instkey):                      ###########define launch instance  function  ###################
    responce  =  client.run_instances(

    ImageId='{0}'.format(imageid),
    InstanceType='t2.micro',
    KeyName = '{0}'.format(instkey),
    MinCount = 1,
    MaxCount = 1
    )
    instid=responce['Instances'][0]['InstanceId']
    return instid




def key(client):                                                      ###########  define keypair function ##################
 
       response = client.describe_key_pairs()
       i = 0
       keys=[]
       while True: 
               try : 
                   key=response['KeyPairs'][i]['KeyName']
                   keys.append(key)
                   i = i+1
               except:
                   break 
 
       for i in range(len(keys)):
                print "press {0} choose '{1}'".format(i+1,keys[i])
                print ' '
       num=int(raw_input("enter the choose key "))
       instkey = keys[num-1]
       return instkey




def terinst(client):                                                                 #######define terminate instance function 
  teminst=raw_input("enter the ID of Instance ")

  terminat  = client.terminate_instances(



    InstanceIds=[
        '{0}'.format(teminst),
    ]

  )
  return terminat






if (s=='1'):

   ec2 = boto3.client('ec2',aws_access_key_id='%s'%(aakey),aws_secret_access_key='%s'%(askey))
   region= ec2.describe_regions()
   regionlist=[]

   for i in range(14):
       l=  region['Regions'][i]['RegionName']
       regionlist.append(l)
   for regi in regionlist:

       ec2 = boto3.client('ec2',region_name='{0}'.format(regi),aws_access_key_id='%s'%(aakey),aws_secret_access_key='%s'%(askey))
       install= ec2.describe_instances()
       reserve=install['Reservations']
       if(reserve==[]):
             print "no instance in '{0}' region".format(regi)
       else :
              i=0
              while True:
                try:
                   instid=install['Reservations'][i]['Instances'][0]
                   print  regi, ':', instid['InstanceId'],':',instid['State']['Name']
                   i=i+1
                except IndexError :
                    break







elif (s=='2'):
    
    reg=raw_input("enter the region ")
    print """
             enter the press 1 for amazon ami 
             enter the press 2 for redhat7.4
             enter the press 3 for ubuntu
        """
    os=raw_input("enter the choose ami ")
    client=fun()
    aimageid=image(client)
    instkey=key(client)
    if (os=='1'):
           imageid=aimageid[0]
           instid=launch(client,imageid,instkey)
           print instid
    elif (os=='2'):
           imageid=aimageid[1]
           instid=launch(client,imageid,instkey)
           print instid
    elif (os=='3'):
          imageid=aimageid[2]
          instid=launch(client,imageid,instkey)
          print instid
    else :
           print 'wrong choice'








elif (s=='3'):
  reg=raw_input("enter the region ")
  client=fun()
  terminat=terinst(client)
  print terminat
  
 










else:
   print 'no'

