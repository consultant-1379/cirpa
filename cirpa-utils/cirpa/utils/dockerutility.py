def save_container_id(containerId):
  '''Function to maintain list of the spawned
     containers by cirpa to be used in case of
     job abort'''
  with open('/tmp/container_ids','a') as fo:
         fo.write('{0}{1}'.format(containerId, '\n'))