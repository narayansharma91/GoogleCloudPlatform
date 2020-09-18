from google.cloud import pubsub_v1
import os
import time

project_id=os.getenv('PROJECT_ID')
topic_id='test-topic'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
file = open('store_sales.csv', 'r') 
for line in file:
    data = line.encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    print('message published: {}'.format(str(future.result())))
    time.sleep(2)

file.close()
