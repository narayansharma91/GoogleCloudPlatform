import apache_beam as beam
import json
from google.cloud import pubsub_v1
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam.transforms.window as window

pipeline_options = PipelineOptions(
        None, streaming=True, save_main_session=True
    )

def calculateProfit(element):
     print('this is final output {}'.format(str(element)))
     return element

with beam.Pipeline(options=pipeline_options) as pipeline:
  readPubSub = (
       pipeline
       | beam.io.ReadFromPubSub(subscription='projects/sumithra-first-project/subscriptions/final-topic-subscription')
       | beam.Map(calculateProfit)
    )

        