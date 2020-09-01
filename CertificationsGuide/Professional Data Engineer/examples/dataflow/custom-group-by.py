import apache_beam as beam
import json

def getElement(element):
  return element['cost_name'] == 'clothes' or element['cost_name'] == 'vegetables'

def mapElement(element):
  return (element[0], sum(element[1]))

def convertToDictory(element):
  return (element['cost_name'], element['amount'])

def loadFile():
  with open('inputs/input.json') as f:
    return json.load(f)

with beam.Pipeline() as pipeline:
  sample = (
      pipeline
        #| beam.io.ReadFromText('inputs/input.json')//read file line by line
        | beam.Create(loadFile())
        #| beam.Map(convertDictionary)
        | beam.Map(convertToDictory)
        | beam.GroupByKey()
        | beam.Map(mapElement)
        | beam.io.WriteToText('outputs/output.txt')
  )
  print(sample)