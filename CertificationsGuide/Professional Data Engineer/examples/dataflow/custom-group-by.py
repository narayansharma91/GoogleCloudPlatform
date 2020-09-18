import apache_beam as beam
import json

def mapElement(element):
  return (element[0], sum(element[1]))

def convertToTuple(element):
  return (element['cost_name'], element['amount'])

def loadFile():
  with open('inputs/input.json') as f:
    return json.load(f)

with beam.Pipeline() as pipeline:
  sample = (
      pipeline
        #| beam.io.ReadFromText('inputs/input.json')//read file line by line
        | beam.Create(loadFile())#load whole json file at once
        #| beam.Map(convertToTuple) #calling function
        | beam.Map(lambda element: (element['cost_name'], element['amount']))#lamda function implementation
        | beam.GroupByKey()
        #| beam.Map(mapElement)#calling function
        | beam.Map(lambda element: (element[0], sum(element[1]))) #lamda function implement alternate of function calling
        | beam.io.WriteToText('outputs/output.txt')
  )