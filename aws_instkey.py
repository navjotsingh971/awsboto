import boto3
aakey=raw_input('enter the access-key ')
askey=raw_input('enter the security key ')
region= raw_input('enter the region ')
ec2 = boto3.client('ec2',region_name='%s'%(region),aws_access_key_id='%s'%(aakey),aws_secret_access_key='%s'%(askey))
response = ec2.describe_key_pairs()
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
    print "    press {0} choose '{1}'".format(i+1,keys[i])

print '    press another number to create new key pair' 

num=int(raw_input("enter the choose key  "))
try :  
   l = keys[num-1]
   print l
except IndexError:
   keyname=raw_input("enter the name of keypair ")
   res=ec2.create_key_pair(KeyName='{0}'.format(keyname))
   print res['KeyMaterial']
   print ' '
   print ' ' 
   print "Note:  key_material save in file with file permission 400"
