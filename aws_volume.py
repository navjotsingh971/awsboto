import boto3
aakey=raw_input('enter the access-key ')
askey=raw_input('enter the security key ')
while True: 
  print '''

  press 1 for show volumes in particular region 
  press 2 for create new volume
  press 3 attach the volume with instance 
  press 4 detach the volume 
  press 5 delete the volume

'''
  choice=raw_input('enter the number ')

  def secure():
    region=raw_input('enter the region  ')
    ec2=boto3.client('ec2',region_name='{0}'.format(region),aws_access_key_id='%s'%(aakey),aws_secret_access_key='%s'%(askey))
    return ec2

  def zones(ec2):
     response=ec2.describe_availability_zones()
     i=0
     zonelist=[]
     while True:
       try: 
         zone=response['AvailabilityZones'][i]['ZoneName']
         i=i+1
       except IndexError:
             break
       zonelist.append(zone)
     return zonelist



  def showvol(ec2):
  
  
     response = ec2.describe_volumes()
     volumelist=[]
     i = 0
     while True:
        try :
           vol = response['Volumes'][i]
           attachment=vol['Attachments']

           if (attachment==[]):

              volume=vol["VolumeId"],vol['Size'],vol['AvailabilityZone'],vol['State']
              volumelist.append(volume)
           else:

              volume=vol["VolumeId"],vol['Size'],vol['AvailabilityZone'],vol['State'],attachment[0]['InstanceId']
              volumelist.append(volume)
           i = i+1
        except IndexError :
               break

     return volumelist


  def crevol(zonename):
      vols=int(raw_input('enter the volume size '))
      vol1=ec2.create_volume(
             AvailabilityZone='{0}'.format(zonename),
             Size=vols,
             VolumeType='standard'           

      )
      return vol1

  def reginame(ec2):            

     responce = ec2.describe_instances()
     instidlist=[]
     i = 0
     while True:
         try :
             regizone=responce['Reservations'][i]['Instances'][0]['Placement']['AvailabilityZone']
             instid=responce['Reservations'][i]['Instances'][0]['InstanceId']
             l=regizone,instid
             instidlist.append(l)

             i= i+1

         except IndexError:
             break

     return  instidlist


  def volname(ec2,zonename):

     responce = ec2.describe_instances()
     volidlist=[]
     i = 0
     while True:
         try :
             regizone=responce['Reservations'][i]['Instances'][0]['Placement']['AvailabilityZone']
             if (regizone==zonename):
                    instid=responce['Reservations'][i]['Instances'][0]['InstanceId']
                    instidlist.append(instid)
             else :
                   pass

             i= i+1

         except IndexError:
             break

     return  instidlist



  def attvol(ec2,instid,volid):
      device=raw_input('enter the device_name(for ex:- /dev/sdh) ')
      response = ec2.attach_volume(
           Device='{0}'.format(device),
           InstanceId='{0}'.format(instid),
           VolumeId='{0}'.format(volid)

      )
      result=response
      return result

  def detvol(ec2,volid):
   
       response = ec2.detach_volume(
       Force=False ,
       VolumeId='{0}'.format(volid),
       )
     
       return response
     

  def delvol(ec2,volid):
       response = ec2.delete_volume(
       VolumeId='{0}'.format(volid),
       )
       return response


  if (choice=='1'):
               ec2=secure()
               volumelist=showvol(ec2)
               print volumelist  
             


  elif (choice=='2'):
     ec2=secure()
     zonelist=zones(ec2)

     print  '' 

     for i in range(len(zonelist)):
       print '''press {0} for '{1}' zone   '''.format(i+1,zonelist[i])

     print ' '

     zonesel=int(raw_input("enter the number for zone "))
     zonename=zonelist[zonesel-1]
     vol1=crevol(zonename)
     print vol1

  elif(choice=='3'):
     ec2=secure()
  
     instidlist=reginame(ec2)
     for i in range(len(instidlist)):
            insid=instidlist[i][1]
            zonename=instidlist[i][0]
            print '''press {0} for ({1} : {2}) zone  '''.format(i+1,zonename,insid)
     print ' '
     if (instidlist==[]):
            print 'no instance in this zone'
          
     else:
       choice=int(raw_input('enter the number for choose instance ')) 
       zonename=instidlist[choice-1][0]
       instid=instidlist[choice-1][1]
       volumelist=showvol(ec2)
  	
       volidlist=[]
       for i in range(len(volumelist)):
               volzone=volumelist[i][2]
               volstate=volumelist[i][3]
               volidp=volumelist[i][0]
               if (volzone==zonename) & (volstate=='available'):
                        volidlist.append(volidp)     
               elif (volzone==zonename) & (volstate=='in-use'):
                         pass
               else:
                         pass
       if (volidlist==[]):
           print 'no volume in zone '
           vol1=crevol(zonename)
           volid=vol1['VolumeId']
 
       else:
          print ' '
          for i in range(len(volidlist)):
                print '''press {0}  for volume-id: '{1}' '''.format(i+1,volidlist[i])
          print ' '
  
          volidsel=int(raw_input("enter the number for volume-id "))
          volid=volidlist[volidsel-1]
       result=attvol(ec2,instid,volid)
       print result

  elif (choice=='4'):
      ec2=secure()
      volumelist=showvol(ec2)
      volidlist=[]
      for i in range(len(volumelist)):
              volids=volumelist[i][0] 
              volsize=volumelist[i][1]
              volzone=volumelist[i][2]
              volstate=volumelist[i][3]
              instid=volumelist[i][4]
              if (volstate=='in-use'):
                    voldict={'volid':volids,'volsize':volsize,'ava_zone':volzone,'instanceid':instid}
                    volidlist.append(voldict)       
              else: 
                    pass
      print ' '
      for i in range(len(volidlist)):
            print ''' press {0} for detach volume with instance ({1} : {2}) '''.format(i+1,volidlist[i]['volid'],volidlist[i]['instanceid'])
      print ' '
      if(volidlist==[]):
           print    "no volume for detach"
      else :
           choice=int(raw_input('enter the number for detach volume '))
           volid=volidlist[choice-1]['volid']
           response=detvol(ec2,volid)
           print response

  elif (choice=='5'):
      ec2=secure()
    
      volumelist=showvol(ec2)
      volidlist=[]
   
      for i in range(len(volumelist)):
              volids=volumelist[i][0]
              volsize=volumelist[i][1]
              volzone=volumelist[i][2]
              volstate=volumelist[i][3]
              if (volstate=='available'):
                    voldict={'volid':volids,'volsize':volsize,'ava_zone':volzone}
                    volidlist.append(voldict)
             # elif(volstate=='in-use'):
             #         print 'Warning:-- please detech the volume {0}'.format(volids)
              else:
                    pass
    
      if (volidlist==[]):
                     print "no 'available state volume' in this region"
 
      else :

         print ' '
         for i in range(len(volidlist)):
               print ''' press {0} for delete volume {1}'''.format(i+1,volidlist[i]['volid'])
         print ' '

         choice=int(raw_input('enter the number for delete volume '))
         volid=volidlist[choice-1]['volid']
         response=delvol(ec2,volid)
         print response
  print ' '
  print ' '
  print "###again choose the option or cltr+c for close########"
  print ' '
