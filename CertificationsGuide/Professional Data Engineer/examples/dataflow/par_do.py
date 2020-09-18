import apache_beam as beam
import json

def loadFile():
  with open('inputs/input.json') as f:
    return json.load(f)

class convertToTuple(beam.DoFn):

    def process(self, element):
        return [(element['cost_name'], element['amount'])]

with beam.Pipeline() as pipeline:
  sample = (
      pipeline
        | beam.Create(loadFile())#load whole json file at once
        | beam.ParDo(convertToTuple())
        | beam.GroupByKey()
        | beam.Map(lambda element: (element[0], sum(element[1]))) #lamda function implement alternate of function calling
        | beam.io.WriteToText('outputs/output.txt')
  )