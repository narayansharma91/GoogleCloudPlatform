# Dataflow Example
- Install airflow on local system
    ```py
    pip install --upgrade virtualenv
    pip install --upgrade setuptools
    virtualenv /path/to/directory
    . /path/to/directory/bin/activate
    pip install apache-beam
    pip install apache-beam[gcp] //if you want to run local workflow pipeline on GCP platform
    ```
- Run simple existing pipelines
    ```py
    python -m apache_beam.examples.wordcount --input inputs/wordcount.txt --output outputs/output.txt

    ```
- Core Concept/Component of Apache-Beam
    - **Pipelines:** A pipeline encapsulates the entire series of computations involved in reading input data, transforming that data, and writing output data.
    - **PCollection:** A PCollection represents a potentially distributed, multi-element dataset that acts as the pipeline's data. Apache Beam transforms use PCollection objects as inputs and outputs for each step in your pipeline. 
    - **Transforms:** A transform represents a processing operation that transforms data. A transform takes one or more PCollections as input, process and produce one or more `PCollection` as output.
    -  **ParDo:** `ParDo` is the core parallel processing operation in the Apache Beam SDKs, invoking a user-specified function on each of the elements of the input PCollection.
    - **Pipelines I/O:** Apache Beam I/O connectors let you read data into your pipeline and write output data from your pipeline. An I/O connector consists of a source and a sink.
    - **Runner:** Runners are the software that accepts a pipeline and executes it. 
    - **Event time:** The time a data event occurs, determined by the timestamp on the data element itself. This contrasts with the time the actual data element gets processed at any stage in the pipeline.
    - **Windowing:** Windowing enables grouping operations over unbounded collections by dividing the collection into windows of finite collections according to the timestamps of the individual elements. 
    - **Watermarks:** Apache Beam tracks a watermark, which is the system's notion of when all data in a certain window can be expected to have arrived in the pipeline.
    - **Trigger:** Triggers determine when to emit aggregated results as data arrives. For bounded data, results are emitted after all of the input has been processed. For unbounded data, results are emitted when the watermark passes the end of the window, indicating that the system believes all input data for that window has been processed. 
