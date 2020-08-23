## dataengineerguideindex
1. [Ingestion](#Ingestion)
    - [Pubsub](#Pubsub)
    - Appengine
    - Kubernetes Engine
    - Cloud Transfer Services
    - Transfer Appliance
2. [Storage](#Storage)
    - Cloud Storage
    - Cloud SQL
    - Cloud Bigtable
    - Cloud Datastore
    - Cloud Spanner
    - Cloud Bigquery
3. [Processing&nbsp;&amp;&nbsp;Analyze](#Process&nbsp;&amp;&nbsp;Analyze)
    - [Dataflow](#Dataflow)
    - Dataproc
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
- Alternate of Apache Kafka
- Use for stream ingestion
- Pull and Push subscription method
- Support customer managed key
- We can connect existing Kafka integration with pubsub with kafka connector
- IAM Roles: Permission apply to project level not individual topic.
    - Publisher: Can only publish message to topic
    - Subscriber, Editor, Admin
- Examples:  
    - [Publish Message (python SDK)](examples/pubsub/publishMessage.py)
    - [Pull Message (python SDK)](examples/pubsub/pullMessage.py)
    
[Top](#dataengineerguideindex)

# Storage

[Top](#dataengineerguideindex)
# Process&nbsp;&amp;&nbsp;Analyze

[Top](#dataengineerguideindex)
# Expore&nbsp;&amp;&nbsp;Visualize

[Top](#dataengineerguideindex)
<hr/>

## Dataflow
- **Basics of Apache Flink:** Distributed processing engine for stateful computations over unbounded and bounded data streams.
  - **Unbounded streams:** Unbounded streams have a start but no defined end. They do not terminate and provide data as it is generated. Unbounded streams must be continuously processed,
  - **Bounded Stream:** have a defined start and end. Bounded streams can be processed by ingesting all data before performing any computations. Ordered ingestion is not required to process bounded streams because a bounded data set can always be sorted. Processing of bounded streams is also known as batch processing.
- **Understand Apache Beam:** Ingest batch & stream processing data and transform those data as required and store into appropriate storage eg. Bigquery, Cloud Storage etc.
 - Apache beam can run on top of **Google Cloud Dataflow**, spark, **Flink** etc.
 -  **Supported SDK**:
    * Python
    * Java
    * Go
- So, what is DataFlow? 
  - Managed data processing services by google based on **Apache Beam**
  - Horizontal autoscaling
  - Pay as you use
  - Pre-defined data processing pipeline template managed by google.
  - Can create own data processing pipeline in any of supported SDK.
- Dataflow window types
- Handle late arrival data
