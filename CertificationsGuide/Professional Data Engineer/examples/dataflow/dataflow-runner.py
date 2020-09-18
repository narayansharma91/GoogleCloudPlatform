import apache_beam as beam
from datetime import datetime
from apache_beam.io.gcp.internal.clients import bigquery
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.options.pipeline_options import SetupOptions
import argparse

table_spec = bigquery.TableReference(
    projectId='sumithra-first-project',
    datasetId='corona_dataset',
    tableId='corona_reports_country_and_month_wise')

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
    }, {
        'name': 'total_deaths',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }, {
        'name': 'total_recovery',
        'type': 'INTEGER',
        'mode': 'NULLABLE'
    }, {
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


# options = PipelineOptions(
#     flags=argv,
#     runner='DataflowRunner',
#     project='sumithra-first-project',
#     job_name='tranform-corona-data',
#     temp_location='gs://sumithra-first-project-dataflow-temp-location/temp',
#     region='asia-south1')
def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        #required=True,
        default='gs://<bucket path>',
        help='Input file to process.')

    parser.add_argument(
        '--output',
        dest='output',
        #required=True,
        default='gs://<bucket path>',
        help='Output file to write results to.')

    # parser.add_argument(
    #     '--region',
    #     dest='location',
    #     default='asia-south1',
    #     help='Output file to write results to.')

    path_args, pipeline_args = parser.parse_known_args()

    input_pattern = path_args.input
    output_prefix = path_args.output


    options = PipelineOptions(pipeline_args)
    #pipeline_options.view_as(SetupOptions).save_main_session = True
    with beam.Pipeline(options=options) as pipeline:
        commonTransformation = (
            pipeline
            | "read data from csv file" >>
            beam.io.ReadFromText(input_pattern)
            | "transform single row to array" >> beam.Map(SplitRow)
            | "remove first row of csv file" >> beam.Filter(RemoveHeader)
            | "select only required fiels which is required" >> beam.Map(SelectFields)
            | "write file" >> beam.io.WriteToText(output_prefix))
run()

