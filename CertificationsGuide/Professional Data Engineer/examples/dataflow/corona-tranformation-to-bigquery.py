import apache_beam as beam
from datetime import datetime
from apache_beam.io.gcp.internal.clients import bigquery

table_spec = bigquery.TableReference(
    projectId='<project id>',
    datasetId='<big query dataset>',
    tableId='<big query table id>')


table_schema = {
    'fields': [{
        'name': 'country_name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'month',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'total_cases',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    },{
        'name': 'total_deaths',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    },{
        'name': 'total_recovery',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    },{
        'name': 'total_tested',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }]
}


def SplitRow(element):
    return element.split(',')

#remove first row of csv file
def RemoveHeader(element):
    return element[0] != 'date'

#select only required fields which required for tranformation rest left as it is
def SelectFields(element):
    dt = datetime.strptime(element[0], "%Y-%m-%d")
    key = str(dt.year) + '-' + str(dt.month) + '_' + element[3]
    return (key, element[11], element[12], element[13], element[14])

# merge all transformation into single object so that we can store it into bigquery
def FinalOutput(element):
    explode = element[0].split('_')
    return {
        'month': explode[0],
        'country_name': explode[1],
        'total_cases': sum(element[1]['cases']),
        'total_deaths': sum(element[1]['deaths']),
        'total_recovery': sum(element[1]['recovery']),
        'total_tested': sum(element[1]['tested'])
    }

#pipeline started 
with beam.Pipeline() as pipeline:
    commonTransformation = (
        pipeline
        | "read data from csv file" >> beam.io.ReadFromText('inputs/covid19-public-data-zip.csv')
        | "transform single row to array" >> beam.Map(SplitRow)
        | "remove first row of csv file" >> beam.Filter(RemoveHeader)
        | "select only required fiels which is required">> beam.Map(SelectFields)
    )
    groupByConfirmedCases = (
        commonTransformation
        | "select only those rows which is having confirmed cases" >> beam.Filter(lambda element: element[1] != '' and int(element[1]) > 0)
        | "select only confirmed cases column out of multiple" >> beam.Map(lambda element: (element[0], int(element[1])))
        | "group by for confirmed cases" >> beam.GroupByKey()
        | "sum the confirmed result based on key" >> beam.Map(lambda element: (element[0], sum(element[1])))
    )
    groupByDeath = (
        commonTransformation
        | "select only those rows which is having death cases" >> beam.Filter(lambda element: element[2] != '' and int(element[2]) > 0)
        | "select only death cases column out of multiple" >> beam.Map(lambda element: (element[0], int(element[2])))
        | "group by for death cases" >> beam.GroupByKey()
        | "sum the death result based on key" >> beam.Map(lambda element: (element[0], sum(element[1])))
    )

    groupByRecovery = (
            commonTransformation
            | "select only those rows which is having recover cases"  >> beam.Filter(lambda element: element[3] != '' and int(element[3]) > 0)
            | "select only recover cases column out of multiple" >> beam.Map(lambda element: (element[0], int(element[3])))
            | "group by for recovery" >> beam.GroupByKey()
            | "sum the recovery result based on key" >> beam.Map(lambda element: (element[0], sum(element[1])))
        )

    groupByNewTested = (
            commonTransformation
            | "select only those rows which is having test records" >> beam.Filter(lambda element: element[4] != '' and int(element[4]) > 0)
            | "select only test recors column out of multiple" >> beam.Map(lambda element: (element[0], int(element[4])))
            | "group by for new tested" >> beam.GroupByKey()
            | "sum the tested result based on key" >> beam.Map(lambda element: (element[0], sum(element[1])))
        )
    
    mergeRecords = (({
            'cases': groupByConfirmedCases,
            'deaths': groupByDeath,
            'recovery': groupByRecovery,
            'tested': groupByNewTested
        })
                | 'Merge all result' >> beam.CoGroupByKey()
                | 'transform the final output for bigquery storage' >> beam.Map(FinalOutput)
                | 'store final output to bigquery' >> beam.io.WriteToBigQuery(
                    table_spec,
                    schema=table_schema,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
                    )
    )
