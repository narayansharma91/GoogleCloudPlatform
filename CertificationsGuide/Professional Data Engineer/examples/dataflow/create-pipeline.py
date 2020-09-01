import apache_beam as beam

def combinedObject(element):#read each element and transform as required
    return 'The student name is {0}, he/she is {1} years old, and rollno is {2}'.format(element['name'], element['age'], element['Rollno'])

p1 = beam.Pipeline()

createPipeline = (
    p1
    | beam.Create([
        {"age": 10, "name": "Narayan Sharma", "Rollno": 34},
        {"age": 26, "name": "Pardeep Sharma", "Rollno": 50}
        ])
    | beam.Map(combinedObject)
    | beam.io.WriteToText('outputs/1.txt')
)
p1.run()