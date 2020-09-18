import apache_beam as beam
import json
from google.cloud import pubsub_v1
from apache_beam.options.pipeline_options import PipelineOptions
from datetime import datetime
from apache_beam import window
from apache_beam.transforms.trigger import AfterWatermark, AfterProcessingTime, AccumulationMode, AfterCount


pipeline_options = PipelineOptions(
        None, streaming=True, save_main_session=True
    )

def calculateProfit(elements):
    buy_rate = elements[5]
    sell_price = elements[6]
    products_count = int(elements[4])
    profit = (int(sell_price) - int(buy_rate)) * products_count
    elements.append(str(profit))
    return elements

def customTimestamp(elements):
  unix_timestamp = elements[7]
  return beam.window.TimestampedValue(elements, int(unix_timestamp))

def encodeByteString(element):
    element = str(element)
    print(element)
    return element.encode('utf-8')

class BuildRecordFn(beam.DoFn):
    def process(self, element, window=beam.DoFn.WindowParam):
      print(element)
      window_start = window.start
      window_end = window.end
      return [element + (window_start,) + (window_end,)]

with beam.Pipeline(options=pipeline_options) as pipeline:
  readPubSub = (
                pipeline
                | 'Read from pub sub' >> beam.io.ReadFromPubSub(subscription='<subscription url>')
                | 'Remove extra chars' >> beam.Map(lambda data: (data.rstrip().lstrip()))
                | 'Split Row' >> beam.Map(lambda row : row.decode().split(','))
                | 'Filter By Country' >> beam.Filter(lambda elements : (elements[1] == "Mumbai" or elements[1] == "Bangalore"))
                | 'Create Profit Column' >> beam.Map(calculateProfit)
                | 'Apply custom timestamp' >> beam.Map(customTimestamp) 
                | 'Form Key Value pair' >> beam.Map(lambda elements : (elements[0], int(elements[8])))
                # Please change the time of gap of window duration and period accordingly
                | 'Window' >> beam.WindowInto(window.FixedWindows(10))
                | 'Sum values' >> beam.CombinePerKey(sum)
                | 'add timestamp' >> beam.ParDo(BuildRecordFn())
                | 'Encode to byte string' >> beam.Map(encodeByteString)
                | 'Write to pus sub' >> beam.io.WriteToPubSub('<output topic>')
              )

        