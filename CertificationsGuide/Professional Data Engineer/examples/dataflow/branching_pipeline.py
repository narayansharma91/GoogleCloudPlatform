import apache_beam as beam
import json
# Apache Beam Job
def loadFile():
  with open('inputs/input.json') as f:
    return json.load(f)

with beam.Pipeline() as pipeline:
  commonPipeline = (#common pipeline(transformation can be implement in common pipeline)
      pipeline
        | beam.Create(loadFile()) #load whole json file at once
  )
  groupByCostName = (
      commonPipeline
        | "convert data to tuple" >> beam.Map(lambda element: (element['cost_name'], element['amount']))#lamda function implementation
        | "grouping cost values with key" >> beam.GroupByKey()
        | beam.Map(lambda element: (element[0], sum(element[1]))) #lamda function implement alternate of function calling
  )
  groupByDate = (
      commonPipeline
        | beam.Map(lambda element: (element['date'], element['amount']))#lamda function implementation
        | "grouping date values with key" >> beam.GroupByKey()
        | beam.Map(lambda element: (element[0], sum(element[1]))) #lamda function implement alternate of function calling
  )
  combineResult = (
    (groupByCostName, groupByDate)
    | beam.Flatten()
    |"write final data" >> beam.io.WriteToText('outputs/final_output.txt')
  )

        