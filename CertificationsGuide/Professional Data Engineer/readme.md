## Data Engineer Guide
1. [Ingestion](#Ingestion)
    - [Pubsub](#Pubsub)
    - [Storage Transfer Services](#storage-transfer-services)
    - App Engine
    - Kubernetes Engine
2. [Storage](#Storage)
    - Cloud Storage
    - Cloud SQL
    - Cloud Bigtable
    - Cloud Datastore
    - Cloud Spanner
    - Cloud Bigquery
3. [Processing&nbsp;&amp;&nbsp;Analyze](#Process&nbsp;&amp;&nbsp;Analyze)
    - [Dataflow](#Dataflow)
    - [Dataproc](#Dataproc) 
    - Dataprep
    - Bigquery
    - Cloud ML
    - Cloud Vision API
    - Cloud Speech API
    - Translate API
    - Cloud Natural Language API
    - Cloud Video Intelligence API
 4. [Explore&nbsp;&amp;&nbsp;Visualize]()
    - Cloud Datalab
    - Google Data Studio
    - Google Sheets

# Ingestion
### Pubsub
- Alternate of Apache Kafka (Publisher and Subscriber model)
- Use for streaming data ingestion at any scale
- Fully managed service (no ops. required)
- Pull(pull message in regular interval) and Push(Pubsub will post request to specific URL when message published to topic) subscription method
- Support customer managed key(Cloud KMS)
- Maximum retention period is 7 days.
- Global availability
- Guaranteed delivery of message at least one
- Once acknowldge of message reciving it get removed from pubsub queue.
- Retry Policy (immediately, exponential backoff delay) 
- We can connect existing Kafka integration with pubsub with kafka connector(With on-prem Kafka)
- Monitor the health of pubsub topics and messages using stackdriver monitoring.
- IAM Roles: Permission can apply to project, topic level as well.
    - Publisher: Can only publish message to topic
    - Subscriber, Editor, Admin
- Examples:  
    - [Publish Message (python SDK)](examples/pubsub/publishMessage.py)
    - [Pull Message (python SDK)](examples/pubsub/pullMessage.py)

[Top](#data-engineer-guide)

### Storage Transfer Services
- Online Transfer Services
    - Gsutil/agent (if data is less than 1 TB, used to transfer on-prem data center to cloud): Best practice while using gsutil: https://cloud.google.com/storage/docs/best-practices
    - Drag & Drop & via API
- Transfer Service
    - One cloud services to another cloud services (eg. S3 bucket to GCS bucket)
    - One bucket to another bucket (eg. GCS bucket to GCS)
    - From public url.
    - Can schedule uploading time based on requirements (eg. Every morning 5 AM)
    - Can filter out the file (based on prefix) while uploading (eg. only file started with config_ etc)
- Transfer Appliance
    - Physical google provided secured device
    - when you have very large set of data to upload into cloud eg. more than 1 TB 


[Top](#data-engineer-guide)

# Storage

[Top](#data-engineer-guide)
# Process&nbsp;&amp;&nbsp;Analyze

[Top](#data-engineer-guide)
# Expore&nbsp;&amp;&nbsp;Visualize

[Top](#data-engineer-guide)
<hr/>

## Dataflow
- **Basics of Apache Flink:** Distributed processing engine for stateful computations over unbounded and bounded data streams.
  - **Unbounded streams:** 
    - kind of streaming data
    - no start and no end (continuously processed)
  - **Bounded Stream:** 
    - Batch processing
- **Understand Apache Beam:** 
    - Based on unified models(single api for streaming and batch processing).
    - write once and run on multiple execution engine eg. google cloud dataflow, flink, spark etc
 - Apache beam can run on top of **Google Cloud Dataflow**, spark, **Flink** etc.
 -  **Supported SDK**:
    * Python
    * Java
    * Go
- So, what is DataFlow? 
  - Managed data processing services(engine) by google based on **Apache Beam**
  - Horizontal autoscaling
  - Pay as you use
  - Pre-defined data processing pipeline template managed by google.
  - Can create own data processing pipeline in any of supported SDK.
- Dataflow window types (for stream processing)
    - Fixed windows (Tumbling windows)
    - Sliding windows (Hopping windows)
    - Session windows
- Handle late arrival data(watermark)
- Understand event time vs processing time
- Use to ingest (from bucket, pubsub etc), transform and store somewhere as required (eg. cloud storage, bigquery, bigtable etc)
- **Access Control**
    - Dataflow Developer: Provide necessary permission to execute & manipulate dataflow jobs.
    - Dataflow Worker: Provide necessary permission to execute dataflow pipeline 

## Dataproc
- Managed Apache Spark, Hadoop on Google Cloud Platform having pre-installed software for batch, stream, quering and machine learning processing.
    - Resizable clusters
    - Autoscalling clusters
    - Pay what you use
    - Easy to spin up clusters in 1 or 2 minutes.
- **Understand the Hadoop Components**
    - HDFS: 
    - MapReduce: 
    - Yarn: 
    - Pig: 
    - Hive: 
    - Spark: 