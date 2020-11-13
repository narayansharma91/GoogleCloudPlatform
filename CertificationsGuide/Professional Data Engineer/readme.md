
## Data Engineer Guide 

## Data Life Cycle
   1. [STORAGE](#Storage)
        - [Cloud Storage](#cloud-storage)
        - [Cloud SQL](#cloud-sql)
        - [Cloud Bigtable](#cloud-bigtable)
        - [Cloud Datastore](cloud-datastore)
        - [Cloud Spanner](cloud-spanner)
        - [Cloud Bigquery](#BigQuery)
   2. [INGESTION & PROCESS](#INGESTION-&-PROCESS)
        - [Compute Engine](#Compute-Engine)
        - [Kubernetes Engine](#Kubernetes-Engine)
        - [App Engine](#App-Engine)
        - [Cloud Functions](#Cloud-Functions)
        - [Pubsub](#Pubsub)
        - [Dataflow](#Dataflow)
        - [Cloud Composer](#Cloud-Composer:)
        - [Storage Transfer Services](#storage-transfer-services)
        - [Dataprep](#Dataprep)
        - [BigQuery](#BigQuery)

   3. [MACHINE LEARNING](#MACHINE-LEARNING)
        -  [ML/AI [Basics terms and terminologies]](#ML/AI-[Basics-terms-and-terminologies])
        - [Dataproc](#Dataproc) 
        - [BigQuery ML](#BigQuery-ML)
        - [Cloud ML](#ML/AI-[Basics-terms-and-terminologies])
        - [Prebuild ML products](#Prebuild-ML-products)
        - [Cloud Auto ML](#Cloud-Auto-ML)

   4. [EXPLORE & VISUALIZE](#EXPLORE-&-VISUALIZE)
        - [Google Data Studio](#Google-Data-Studio)
        - Cloud Datalab
        - Google Sheets

## Miscellaneous Terms
 - [Roles of Data enginneer](#Roles-of-Data-Enginneer)
 - [Data Lake](#Data-Lake)
 - [Data warehouse](#Data-warehouse)
 - [Batch Processing](#Batch-Processing) 
 - [EL/ELT/ETL Tranformation](#EL/ELT/ETL-Tranformation)

## **Data Life Cycle**
### STORAGE
#### Cloud Storage
- Used to store any type of data(objects) with unlimited storage.
    #### Key points:
    - Bucket name is global(you can't create a bucket which is already being created by others and you)
    - Lifecycle management
        - You can change the storage class/Delete based on different condition (age, versioning, previous class, etc)
        - The best way to save your storage cost
        - Retrieval charge will be applied if your storage class is other than standard.
        - Best for backup, archival storage.
        - Can't change the bucket from regional to multi-regional and vice/versa.
    - Access Control
        - Bucket Level permission managed by IAM
        - Object-level permission managed by ACL.
        - **Object Creator:** (allow create an object but not allowed delete, view  or replace object)
        - **Storage Object Viewer:** (allow list the objects and allow to view metadata)
        - **Storage Object Admin:** (allow users to manage (add, delete, replace) objects in the bucket)
        - **Storage Admin:** (allow users to manage full all objects and buckets)
    - Requestor Pay:
        - If you want to provide the data to others and you don't want to pay for associate charge with that operations eg. Data retrieval, operational charges, network charges.
    - Support Composite Objects:
        - Create a new composite object whose contents are concatenation of multiple objects.
    - Data secure at rest:
        - Encryption support (GME, CME, and CSE)
        - Configure CSE in the boto configuration file
        - Encrypted with Data Encryption Key(DEK) and DEK is further encrypted with (KEK)
    - gsutil command
        - ACL management
        - Download, upload the objects
        - Create buckets etc
    - Transfer services
        - From another cloud and public URL (eg. S3)
        - From another GCP cloud bucket.
        - From on-premises (using agent)
        - Transfer appliance (if you have data more than 20 TB or its take more than 7 days to upload)
            - Secure device(which you can lease the device from google), Good for a very large amount of transfer.
            - Transfer from device to your project is called dehydration.
    - Data Locking (eg. retention policy)
        - This allows, we can't delete/replace until it's reached the specified age.
        - Apply at the bucket level.
    - Support CORS: (use cases: website hosting)
    - Support versioning: (Active version is called live version)
    - Support zip compression:
    - Resumable upload:
        - Recommended to upload large files.
        - It will automatically pick from where it's gets failed.
        - Best suite for slow internet connection 
        - Completed these operations consider as **Class A** operations.
    - Support stream transfer: 
        - You can upload/download from/to bucket without saving first.
    - Multipart Uploads:
        - Useful if you have many small files to upload
        - Consider as **Class A** operations.
    - Signed URL
        - If you want to share your object with someone for particular periods only eg. 1 hour, 1 day, etc.
    - Consider this as a stagging area of all data storage (**known as datalake**)
    
    [Top](#data-engineer-guide)

#### Cloud SQL
- Managed RDBMS by Google
    #### Key points:
    - Best use for OLTP (Online Transactional Processing), Support Fast insertion 
    - Support MySQL, Postgres-SQL, and SQL-Server
    - Automate most of the operations (eg. patching, backup, storage management)
    - High availability
        - Create a read-only server to a different zone. (only read-only access, no write, you have to enable binary logging)
        - Create a failover replica in a different zone. (automatic connect with a different instance with same configurations)
    - Support up to 30TB of database size.
    - Support point-in-recovery.
    - Securely connect DB without whitelisting IP.
    - Only vertical scaling

    [Top](#data-engineer-guide)
#### Cloud Bigtable
- Google own No-Sql bigdata database services.
    ### Key points:
    - Handle millions of requests per second (milliseconds IOPS) with low latency.
    - Good fit for time series data, fintech, digital media, etc.
    - Can have billions of rows and thousands of columns(wide columns database).
    - Incredible scaling without downtime.
    - Each row only have one index is called row key.
    - Columns are group together by column family (and sorted lexicographical order)
    - Cloud Bigtable tables are sparse(empty cell doesn't take space)
    - Best practice to store only 10MB on a single cell and 100MB for a single row.
    - The table is sharded into multiple tablets.
    - Choose HDD/SSD
        - Choose HDD if you have data more than 10TB and infrequent access.(eg. Data archival)
        - Choose SSD for high performance if you have data less than 10TB.
    - Choosing row key
        - Good row key help to search result efficiently.(eg.username#timestamp)
        - Keep in mind the query of the table while creating the row key.
        - User reverse timestamps when you need the most common query for the latest values.
    - Choose narrow and table structure when you are working with time series data.
    - Hotspotting:
        - Rows in Bigtable stored lexicographically(lowest to the highest byte string) by row key. It allows store related information into a single region/node. this behavior request goes to a particular server and there is a chance of overload and creating hotspots.
        - Prevent hot-spotting:
            - Field Promotion: Move columns data to row data
            - Salting: Add an additional calculated element to the row key to artificially make writes non-contiguous.
    - Instance: Consider a container of your data. One instance contains more than 1 cluster and 1 cluster can have multiple nodes.
        - Table belong to instances, not clusters, and node.
    - Clusters: It's considered as service in a specific location.
        - Clusters belongs to an instance.
        - Located in a single zone.
    - Node: Part of clusters and known as compute resources.
        - Which is used to manage your data.
        - It's responsible for keeping track of specific tablets on disk.
    - Compaction:
        - The process of re-organizing the data which was already deleted to make more efficient know as compaction. 
    - Access data using `cbt` command or Hbase shell
    - Tablet: Sharded version of the table is called a tablet.
    - No transaction support.
    - Access Control
        - Can control the IAM permission project level, instance level, and table level.
    - Best Practice
        - For time serious table, use narrow/tall table
        - Keep related information in a single table and move unrelated data to another table
        - Keep column family/column name short (disk space save)
    - Good if your data is more than 1 TB
    - Replication, backup, restore all those things take care of by BigTable.
    - We can add up to 4 clusters in single instances.
    - Can't change from HDD to SSD: (todo you have to export data to the bucket and recreate again)
    - App profile
        - Configurations that we can configure how to handle the incoming request, 
        - **Single routing policy:** Routes all request to a single cluster, If cluster unavailable you have to manually failover to a different cluster.
        - **Multi-cluster routing:** Automatically routes the request to the nearest cluster, if the cluster is unavailable it automatically failover to another cluster.
    - Bigtable/Storage Structure
        - One instance can have multiple clusters
        - One cluster has multiple nodes (compute instances)(tablet server)
        - Tables are sharded into a block of contiguous rows called a tablet.
        - Tablet is stored in Colossus (Google File System) in SStable format.
        - Each tablet is associate with a particular node.
        - Data never stored in node rather stored in Colossus.
        - Rebalancing, recovery, is very fast you don't need to recover the entire data, just set the pointer.
        - No data will be lost if the node failed.

    [Top](#data-engineer-guide)

#### Cloud Datastore
- NoSQL fully managed database build on top of Bigtable by Google
    ### Key points:
    - Highly scalable based on utilization
    - Automatic sharding, Support ACID transactions, indexes, SQL like query (GQL)
    - Next version of datastore is called firestore (support realtime update & many more)
    - Exporting options/limitations:
        - You can't export index values
    - Index is the heart of Datastore
        - Query gets a result from the index only.
        - Composite Index:
            - This is useful when you have complex query
            - All index defined in index.yaml file and upload using gcloud
        - Build-in:
            - Allow single property queries.
    - RDBMS/Datastore (key terms)
        - Table == Kind
        - Row == Entity
        - Column == Property
        - Primary Key == Key
    - Consistency Level
        - Strong Consistent:
            - Query give upto results but might take longer time.
            - The query which is execute against entity group is strongly consistent.
        - Eventually Consistent:
            - Query run faster but sometime give stale result
            - Global query (not part of entity group) are always eventual consistent.

    [Top](#data-engineer-guide)

#### Cloud Spanner
- Fully managed, highly scalable RDBMS by google.
    ##### Key points:
    - Support horizontal scaling with strong consistancy across different regions.
    - Support SQL query.
    - Table structure is different than MYSQL(child table resides in parents table: interleaved table and parents child table relationship with primary and FK key).
    - Strong transaction is available.
    - Automatic sharding
    - Avoid Hotspoting:
        - Hash the key
        - Swap the order
        - Use the UUID key
        - Bit reverse.

    ##### Access Control:#####
        - You can set IAM permission at project, instance level, and database level.

    [Top](#data-engineer-guide)

<hr/>

### INGESTION & PROCESS
#### Compute Engine:
- Refer this documentation: https://cloud.google.com/compute/docs

#### Kubernetes Engine:
- Refer this documentation: https://cloud.google.com/kubernetes-engine/docs
#### App Engine:
- Refer this documentation: https://cloud.google.com/appengine/docs
#### Cloud Functions:
- Refer this documentation: https://cloud.google.com/functions/docs

[Top](#data-engineer-guide)

#### Pubsub:
- Pub/Sub is an asynchronous messaging service and Alternate of Apache Kafka (Publisher and Subscriber model)
    #### Features:
    - Use for streaming data ingestion at any scale
    - Fully managed service (no-ops. required)
    - Pull(pull message in the regular interval) and Push(Pubsub will post request to specific URL when message published to topic) subscription method
    - Support customer-managed key(Cloud KMS)
    - Multiple users can publish the message into a single topic, one topic can have multiple subscriptions, message deliver to subscription, not a subscriber(if multiple users subscribed to single subscription only one message will be delivered)
    - Maximum retention period is 7 days.
    - Global availability
    - Guaranteed delivery of the message at least one
    - Once acknowledge of the message receiving it get removed from the pubsub queue.
    - Retry Policy (immediately, exponential backoff delay) 
    - We can connect existing Kafka integration with pubsub with kafka connector(With on-prem Kafka)
    - Monitor the health of pubsub topics and messages using stack driver monitoring.
    - Challenges Associated with PubSub.
        - Latency
        - No Order of messages
        - Duplication may happen
    #### Access Control: Permission can apply to Project, topic level, and subscription level as well.
    - Publisher: Can only publish a message to the topic
    - Subscriber, Editor, Admin
    #### Examples:  
    - [Publish Message (python SDK)](examples/pubsub/publishMessage.py)
    - [Pull Message (python SDK)](examples/pubsub/pullMessage.py)

    [Top](#data-engineer-guide)

#### DataFlow
- Fully managed streaming analytics service that minimizes latency, processing time, and cost through autoscaling and batch processing.

    ##### **Basics of Apache Flink:**
    - Distributed processing engine for stateful computations over unbounded and bounded data streams.

    ##### **Understand Apache Beam:**
    - **UNIFIED:** single api for streaming and batch processing.
    - **PORTABLE:** write once and run on multiple execution engine eg. google cloud dataflow, flink, spark etc
    - **Extensible:** Various connector, Supported by various SDK (eg. Python, Java, Go)
    ##### **Workflow:**
    - **Input[Storage, Pubsub, BigQuery etc]  => Read => Various Transformation[Grouping, Filter, Side-Input etc] => Write[Bucket, Pubsub, BigQuery etc] -> Output**

    ##### **Key points:**
    - Unbounded streams:
        - kind of streaming data
        - no start and no end (continuously processed)
    - Bounded Stream:
        - Batch processing
    - Pipelines:  Set of data processing elements connected in series. where the output of one element will be input for the next one.
    - PCollection:
        - Represent the distributed dataset for parallel processing.
        - It's immutable
    - Transform: 
        - Data processing operations.
        - Uses programming logic eg. loop, if-else etc.
    - Runner: 
        - Execution environments to execute beam pipelines eg. dataflow, spark, flink, etc
    - Side Input: 
        - It's additional input that your DoFn can access that data every time while processing. eg. get configurations from BigQuery while transforming your data.
    - Various transformations functions:
        - Element: Single entry in data
        - ParDo: Perform parallel processing, take a single input, and produce zero or multiple outputs for the next collection.
        - Map: 1 to 1 mapping function over each element in the collection.
        - Flatmap: 1 to many mapping functions over each element in the collection.
        - GroupByKey: Grouping the values based on a common key for single input PCollection.
        - CoGroupByKey: Same as GroupByKey but it takes multiple input PCollection and grouping them.
        - Combine: use this for faster performance over groupBy
    - We can create our template(flexible, standard)
    - Support Dataflow SQL
    - Lag Time: The interval between event time and the processing time is called lag time.
    - Composite Transform: Group of multiple transformations is called composite transformation.
    - Watermark: Which is the system’s notion of when all data(including late date) in a certain window can be expected to have arrived in the pipeline
    - Trigger: Machnisim to when to fire a final event. Once triggered run late date is not allowed.
    - Event Time: the time of event occurs, determined by timestamp on the data itself.
    - Processing Time:  The time the data appears in the pipeline
    - Composite trigger
    - Handle late arrival data(watermark)
    - Windowing (for stream processing):
        - Divide the unbounded collection into logical components called windowing.
            - **Fixed windows (Tumbling windows)**
                - Consistent, disjoint time interval
            - **Sliding windows (Hopping windows)**
                - Consistent but can be overlap between the window
                - eg. to take the running average of data.
            - **Session windows**
                - Contains element within gap duration of another element. The gap duration is an interval between old and new data in the data stream.
                - If an event doesn't occur within a specified time it will close the window and start a new one.
                - eg. User session data, click records, gaming state, etc.
            - Single global window: (default for both)
                - Default window
                - Late arrival data will be discarded
                - This is best for batch processing

    ##### **Features of DataFlow:**
    - Horizontal autoscaling(adding vm automatically based on demand)
    - Pay as you use
    - Pre-defined data processing pipeline template managed by google.
    - Can create own data processing pipeline in any of the supported SDK.
    - Work scheduler
    - Dynamic work re-balancer
    - Intelligent watermarking
    - Types of trigger
        - Event Time
        - Processing Time
        - The number of data elements in a collection.

    ##### Access Control:
    - Dataflow Developer: Provide necessary permission to execute & manipulate dataflow jobs.
    - Dataflow Worker: Provide necessary permission to (VM) execute dataflow pipeline 

[Top](#data-engineer-guide)

#### Storage Transfer Services:
- There is various way to transfer data from different source to GCP.
    #### Online Transfer Services
    - gsutil/agent (if data is less than 1 TB, used to transfer on-prem data center to the cloud): Best practice while using gsutil: https://cloud.google.com/storage/docs/best-practices
    - Drag & Drop & via API
    #### Transfer Service
    - One cloud services to another cloud services (eg. S3 bucket to GCS bucket)
    - One bucket to another bucket (eg. GCS bucket to GCS)
    - From public URL.
    - Can schedule uploading time based on requirements (eg. Every morning at 5 AM)
    - Can filter out the file (based on prefix) while uploading (eg. the only file started with config_ etc)
    #### Transfer Appliance
    - Physical google provided secured device
    - when you have a very large set of data to upload into the cloud eg. more than 1 TB 

#### Dataprep:
    - Intelligent data service for visually exploring, cleaning & preparing structured and unstructured data for machine learning and reporting by Trifacta.
    - No, Ops, no server management, autoscaling as demand.
    - No need to write any code.
    - You can apply various predictive transformations as well as custom.
    - Also we can schedule the transformation of recipes as per our need. 

[Top](#data-engineer-guide)

#### BigQuery:
- Fully managed petabytes scale serverless data warehouse service for both Fast Query processing and storage.
- Connected with a high-speed network (PetaBytes) between storage and Query service.
    #### Structure of BigQuery:
    - One project contains one or more dataset
    - One dataset contains one or more tables
    - [STORAGE]: BigQuery leverages Capacitor to store data in Colossus
        - Colossus is Google’s latest generation distributed file system and successor to GFS (Google File Systems)
        - Colossus handles cluster-wide replication, recovery and distributed management
    - [COMPUTE]: BigQuery takes advantage of Borg for data processing.
        - Borg simultaneously runs thousands of Dremel jobs across one or more clusters made up of tens of thousands of machines
        - In addition to assigning compute capacity for Dremel jobs, Borg handles fault-tolerance
    - [NETWORK]: Google’s Jupiter network enables BigQuery service to utilize 1 Petabit/sec of total bisection bandwidth.
    #### Key points/features of BigQuery:
    - Support Federated Query/Datasource:(with few limitations)
        - Data resides outside the BigQuery and still be able to query on data (eg. Cloud SQL, Cloud storage, cloud BigTable, drive, etc)
        - Small sets of the dataset which is constantly changing(do not need to load data every time).
        - Federated query results never are cached.
        - Never stored data inside BigQuery.
        - You will be able to join tables between big query tables and external data sources (eg. cloud SQL)
        - The location of BigQuery (processing) and external data source should remain in the same region.
    - Support stream insertion and batch insertion.
        ##### Stream Insertion:
        - If you need millions of insertion per seconds consider BigTable
        - Column size shouldn't be greater than 5 MB
        - Maximum bytes per seconds shouldn't be more than 1 GB
        - 500 Thousand rows per second per project/per table.
        - Can't insert more than 10,000 rows at a time.
        - When you pass inserted BigQuery uses this id to support best-effort de-duplication for up to 1 minute.
        - If you need strong de-duplication requirements consider storing information in a datastore which is support transactions.
        - For better de-duplication requirements you can use dataflow as data processing tool before insert into BigQuery.
        - you can stream insert into BigQuery partitioned tables (last 5 years and future 1 years)
        ##### Batch Insertion:
        - Allow you to put several API calls into a single HTTP request.
        - Only 1000 batch operations you can perform per day.
    - Support Decorator:(Supported in legacy SQL)
        - This is the way of getting a subset of information in cost-effective way (eg. if you want to take a snapshot of the table at one hour ago.)
    - Support user-defined functions:
        - You can write your own persistent or temporary functions
        - Function can be written in JavaScript of SQL.
        - Take columns as arguments, perform operations, and return the result.
    - Support Analytical Function
        - OVER, RANK, LEAD, LAG, etc.
    - Support Geographical functions:
        - functions start with **ST_**
    - Support standard SQL.
    - Configuration file for BigQuery
        - --use_legacy_sql=false in .bigqueryrc
    - Export Capabilities/Limitations
        - Supported format (JSON, CSV, AVRO)
        - Can't export more than 1 GB in a single file
        - Only you can export to Cloud Storage.
        - You can't export repeated & nested fields in CSV
        - The bucket of the location should be in the same region as BigQuery dataset location.
        - Supported compression type is gzip (for all types) and snappy(Avro)
        - eg. `bq extract --destination_format NEWLINE_DELIMITED_JSON 'mydataset.mytable' gs://example-bucket/myfile.json`
    - Loading data to BQ Capabilities/Limitations
        - Supported format (AVRO, JSON, CSV, ORC, Parquet)
        - Wildcard, comma separated file upload doesn't support from the local system.
        - The location of the bucket and dataset should be in the same region.
        - Doesn't support nested and repeated fields.
        - Doesn't support SQL format
        - Source table and destination table should be in the same location while copying.
    - Support BigQuery magic function (%%) to store BigQuery to pandas dataframe.
    - Two types of query processing
        - Interactive: Query will execute as soon as possible.
        - Batch: Query will execute as soon as possible when idle resources available, if the query doesn't execute with int 24 hours it will convert to interactive query.
        - NOTE: The same price for both jobs, the batch query doesn't count towards your quota but Interactive does.
    - Authorized View:
        - Permitting (group, person) by creating a view which includes a subset of your data (without permitting underlying source dataset)
    - Partition:
        - Special table divided into different segments. It helps to increase performance and lower costs.
            ##### Ingestion Time:
            - Table is partitioned based on load time (load data into BigQuery)
            - Default is Daily based partitioned, we can specify HOUR, MONTH, DAY, and YEAR.
            ##### Date/timestamp/datetime:
            - Table are partitioned based on Date/timestamp/datetime column
            - If partitioned on Date column we can partition Daily, Monthly, Yearly.
            - If partitioned on timestamp/datetime column we can partition with any time unit eg. hour,
            ##### Integer Range:
            - Table is partitioned based on integer columns.
            - You can specify the start, end, and interval of partitioned during the creation of partitions.
        - 
    - Clustering:
        - Another way to increase performance.
        - When you create clustering from different columns, BigQuery automatically arranged the content of columns in sorted order. 
        - Similar to RDBMS indexing.
        - If data doesn't present in clustering, BigQuery prevents the whole scanning.
        - You can clustering on partitioning columns.
        - Cluster only those column which is commonly used in where and aggregation.
    - Table Expiration: You can specify the number of days to keep your data on BigQuery and it will automatically remove from BigQuery storage.
        - This is helpful if you only want to analyze the insights without storing it(permanently). 
        - Save storage cost.
        - You can apply table expiration at the dataset level and partitioned table.
    - Metadata:
        - This is useful to get information about the dataset, tables, table schema, reservation, job, view, etc.
    - Build ML models using structured Data.
    #### Best practice while working in BigQuery
    ##### Best practice of schema design
    - Support Record/Struct:
        - Struct is a container of fields (consider as relation table in RDBMS)
        - The best way to organize data without a normalized table.
        - Struct can have another struct inside the struct.
        - Struct can have repeated fields inside it.
        - It will prevent the join (which is costly)
    - Repeated Fields:(array)
        - Array is called REPEATED fields in BigQuery.
        - Extract the array information into rows you can use ***UNNEST**
        - It will save storage space.
    ##### Best practice for saving the cost/other
    - Avoid **Select *** 
    - Data skew:
        - Data skew can occur when the data in the table is partitioned into unequally sized partitions. When joining large tables that require shuffling data: (pre-filter results before join)
    - De-normalize when-ever possible
        - Use Struct & Array for faster performance and low cost.
    - Limit doesn't impact the cost
    - Partition
    - Clustering
    - Use APPROX_COUNT_DISTINCT over count(distinct)
    - Put largest table on left while joining
    - Put where on early as possible(early filtering)
    - Put order on outmost query
    - Storage Cost:
        - Table Expiration
        - Active vs Passive(older than 90 days)

    #### Pricing model
    - On Demand: 
        - Calculate amount based on bytes scanned.
        - Query will get up to 2000 slots per project(depending upon query complexity)
    - Slots based: (Kind of commitment)
        - Slots are BigQuery's unit of computational capacity
        - Dedicated resources(CPU, RAM, etc) for your workload.
        - Best fit if you know the predictive cost for BigQuery.
        - You can query as much as you can.
        - You can reserved slots for Flexible(minute, hour, etc), monthly, yearly basis.
        - Doesn't include a storage charge.
    #### Data encryption and security.
    - Encrypted at rest.
    - Support google manage encryption and customer-managed keys.
    - Not supported customer supplied keys.
    #### Bigquery Migrations & Data transfer
    - Backfill: The process of fill the data which, is missing while loading.
    - Support various connector (more than 100) and you can load data from different SaaS products
    - EL (Extract & Load): (consider this if you don't need any transformation)
    - ETL (Extract Transform & load): (consider this if your source data is not clean and you need to transform before loading into BigQuery)(use dataflow for transformation)
    - ELT: (Extract Load & Transform): Consider this if you have limited transformation and use a simple query to transform those records as required.
    - Batch transfer supported format
        - CSV, JSON, Avro, datastore backup, parquet, orc.
    - BQ to BQ transfer services only available within the same region (you can't transfer from one region to another)
    - Way to change location
        - Export to the same location bucket -> copy bucket data to the new bucket -> create a new dataset from a new location bucket.
    #### Access Control
    - Inherited Access control from IAM
    - Project level, dataset level permission managed by cloud IAM.
    - Table, View level permission manage by ACL.
    - Individual authorized view doesn't support ACL.
    - Viewer:
        - Can start the job
        - List out all the jobs.
    - Editor: 
        - Same as viewer +
        - Can create a new dataset in the project
        - If you create a new dataset in BigQuery you will be the owner of that dataset.
    - Owner:
        - Same as Editor +
        - Can list all the datasets 
        - Can delete any datasets in the project.

   [Top](#data-engineer-guide)

<hr/>

### MACHINE LEARNING
#### ML/AI [Basics terms and terminologies]
- **AI vs ML:**
    - AI is a science discipline and its works with theory and method. 
    - AI is broad topics
    - ML is one branch of AI.
    - ML is a toolset & it is the study of computer algorithms that allow a computer program to learn and improve through experience. 
- **Supervised Learning:**
    - Designed to be learned from example(training dataset).
    - Consists of input(data) along with label(output).
    - Use while training the model.
    - Classification & Regression model are an example of Supervised learning.
- **Unsupervised Learning:**
    - Data doesn't have a label(output).
    - Only provide input data.
    - Clustering & association are examples of unsupervised learning.
- **Clustering:**
    - Clustering is a form of unsupervised learning(learning with unlabeled data)
    - Used to organize customer demographics and purchasing behavior into specific segments for targeting.
- **Association**
    - Association is part of unsupervised learning
    - It attempts to identify associations between the various items in big data set.
    - eg. If you purchase a mobile on an eCommerce website it tends to be by the mobile cover.
- **Regression:**
    - Regression is a type of structured machine learning algorithm where we can label the inputs and outputs
    - **Linear regression:**
        - Provides outputs with continuous variables (any value within a range), such as pricing data
    - **Logistical regression:**
        - Logistical regression is when variables are categorically dependent and the labeled variables are precisely defined. For example, you can classify whether a store is open as (1) or (0), but there are only two possibilities.
        - It is used to solve the classification problem.
- **Classification:**
    - Classification is a part of supervised learning (learning with labeled data) through which data inputs can be easily separated into categories
    - Cross-Entropy is used to solve the classification problem.
    - **Binary Classification:**
        - try to predict yes/no response (only two possible answers)
    - **Multi-class Classification:** 
        - try to predict more than 2 possible values (eg. low, medium, high priority, etc)
- **Generalization:**
    - Refers to the model’s ability to react to new data, Once it is trained on a training set, the model will be able to digest new data and make predictions. 
- **Sampling:**
    - Picking the subset of the entire dataset while analyze without having to investigate(analyze) all datasets.
    - It's easy to process, cost-effective, etc
- **Hyperparameters:**
    - The parameter whose values are used to control the learning process(external configurations configured by the practitioner).
    - We can't estimate the value from the dataset.
    - Hyperparameters adjust the training process itself.
    - https://cloud.google.com/ai-platform/training/docs/hyperparameter-tuning-overview 
- **Deep & Wide neural network:** (https://ai.googleblog.com/2016/06/wide-deep-learning-better-together-with.html)
    - Deep learning used for generalization
    - Wide learning used for memorization.
    - Good for recommender system 
- **Inference:**
    -  The process of using a trained machine-learning algorithm to make a prediction
- **Training:**
    - The process of creating an ML algorithm.
    - Traning involves the use of deep learning framework like (TensorFlow)
    - Data is the fuel of any ml model
- **Models:**
    - It's just mathematical functions will predict output for the given input
- **Label:**
    - The output you get from your model after training it is called a label.
- **Features:**
    - Features are the measurable property of the object you are trying to analyze.
- **Feature Engineering:**
    - The process of extract features from raw data using domain knowledge(eg. cleaning data, aggregation, etc).
    - This is helpful to improve the performance of ML.
- **Training set:**
    - is a subset of the dataset used to build predictive models
- **Validation set:**
    - Subset of the dataset **used** to assess the performance of the model built in the training phase
- **Test set:**
    - Unseen data, is a subset of the dataset used to assess the likely future performance of a model
- **Confusion matrix:**
    - A much better way to evaluate the performance of a classifier is to look at the confusion matrix
- **Feature Selection:** 
    - Feature Selection is the process where you automatically or manually select those features which contribute most to your prediction variable or output in which you are interested.
- **Overfitting:**
    - Overfitting occurs when your model learns the training data too well and incorporates details and noise specific to your dataset. You can tell a model is overfitting when it performs great on your training/validation set, but poorly on your test set (or new real-world data).
- **Underfitting:**
    - When it cannot capture the underlying trend of the data.
    - It will destroy the accuracy of ML prediction.
    - This usually happened when we have less data while creating an ML model.
- **Prevent Overfitting:**
    - Split data into training and validation(test)
    - Once the RMSE value getting increase you have to stop fitting data into the model.
    - Training model with high-quality data.
    - Remove unnecessary features.
    - Stopped earlier to feed data(noise data) into the model
    - Regularization
- **Bias:**
    - Data bias in machine learning is a type of error in which certain elements of a dataset are more heavily weighted and/or represented than others.
- **L1 & L2 Regularization:** (https://developers.google.com/machine-learning/crash-course/regularization-for-sparsity/l1-regularization)
    - L1 is used to feature selection, tries to estimate the median of the data
    - L1 regularization is able to reduce the weights of less important features to zero or near zero
    - L1 regularization helps in feature selection by eliminating the features that are not important
    - L1 regularization is used in a sparse data set.
    - L2 used to prevent overfitting.
    - L2 regularization is more relevant when all features have relatively equal weights/influence
    - L2 regularization always improves generalization in linear models.
    - L2 regularization is best used in non-sparse outputs.
- **Loss Metrics:**
    - MSE: Mean Squared Error (a measure of loss)
        - Represents the difference between the original and predicted values which are extracted by squaring the average difference over the data set.
        - Use in the regression model.
    - RMSE: Root Mean Squared Error (use in higher weight and many errors)
        - RMSE (Root Mean Squared Error) is the error rate by the square root of MSE
        - Use in the regression model.
- **Neural Network:**
    - NN is a computational learning system that uses a network of functions to understand and translate a data input of one form into the desired output, usually in another form. The concept of the artificial neural network was inspired by human biology and the way neurons of the human brain function together to understand inputs from human senses. 
- **Epoch:**
    - An epoch describes the number of times the algorithm sees the entire data set.
- **TensorFlow:**
    - Open-source platform machine learning/Deep learning.
- **Matrix factorization:**
    - Algorithm Used to build a recommendation system.
- **Validate the ML Model:**
    - If you have lots of data use a separate test dataset
    - If you have little data use cross-validation (training, validation with multiple scenarios)
- **Deep Learning:**
    - Usable when you can't explain the labeling rules
- **Kubeflow:**
    - Used to making deployments of machine learning workflow on Kubernetes.
- **TPU:**
    - Tensor Processing Unit(designed to solve the computational problem)
    - Optimised for large batches and CNNs and has the highest training throughput.
    - Used in machine learning
- **Re-enforcement model:**
    - It enables an **agent** to learn in an interactive environment by trial and error using feedback from its own actions and experiences

[Top](#data-engineer-guide)

#### Dataproc
- Managed Apache Spark, Hadoop on Google Cloud Platform having pre-installed software for batch, stream, querying, and machine learning processing.
    ##### Key points
    - Resizable clusters
        - Support Graceful Decommissioning(don't stop without completing its work)
    - Autoscaling not good
        - If you are storing data inside HDFS
        - When you need Spark Structured Streaming
    - Left & Shift existing Hadoop workloads.
    - Can utilize preemptable VM for cost-saving.
    - Autoscaling clusters (based on Hadoop YARN metrics)
    - Pay what you use
    - Dataproc spark operations use lazy execution.
    - Easy to spin up clusters in 1 or 2 minutes.
    - Cost-saving (by utilizing preemptible VM, and turn VM down whenever you don't' need)
        - Best, do not use more than 50% preemptible VM (out of total VM)
    - Choose HDFC over Cloud storage
        - When your job has lots of metadata operations eg. thousands of partitions and directories and file size is small.
        - If you are modifying the directory structure.
        - when you append data on the HDFS file.
    - Support DAG for workflow management(inside data proc via rest API & command line)
    ##### Understand the Hadoop Components
    - HDFS: The Hadoop Distributed File System (HDFS) is the primary data storage system used by Hadoop applications. It employs a NameNode and DataNode architecture to implement a distributed file system that provides high-performance access to data across highly scalable Hadoop clusters. It's designed with high fault tolerance.  
    URL: https://www.edureka.co/blog/apache-hadoop-hdfs-architecture/
        - NameNode:
            - Act as the master server
            - Manages the file system namespace
            - stored data metadata not data
            - It also executes file system operations such as renaming, closing, and opening files and directories.
        - DataNode: 
            - Act as a slave node
            - Store data that need to be processed.
            - Send heartbeat request to namenode (health check)
    - MapReduce: MapReduce is a software framework and programming model used for processing huge amounts of data. MapReduce program work in two phases, namely, Map and Reduce.
        - Map: Deal with splitting and map of the data
        - Reduce: Deal with shuffle & reduce the data.
    - Yarn: Yet Another Resource Negotiator
        -Introduce in Hadoop 2.0
        - It's redesigned of a resource manager
        - Separate the resource management layers from the processing layer.
        - Allow different data processing engines like batch processing and stream processing.
    - Pig: 
        - High-level programming language which is useful for analyzing a very large data set.
        - Build on top of Hadoop for the map and reduce functionality. (abstraction layers)
        - It allows the programmer to focus on data rather than focus on programming (how map and reduce is working internally in the Hadoop eco system)
    - Hive: 
        - data warehouse infrastructure tool
        - working with a structured dataset
        - Support SQL like language called HQL (Hive Query Language)
    - Spark: 
        - Big data distributed processing in-memory framework.
        - Very fast (100 times) as compared to map-reduce.
        - Very useful for stream processing, machine learning, graph processing, etc
        - Can run separately or also run top of the Hadoop eco system.
    - Sqoop: 
        - Tool to export HDFS data to Relational database or import data from a relational database to HDFS.
    - Oozie: 
        - Workflow scheduler for Hadoop.
        - Organize workflow using DAG (Directed Acyclical Graphs) in action.

[Top](#data-engineer-guide)

#### Data Fusion:
- Fully managed, cloud-native enterprise data integration service for quickly building pipelines and managing pipelines.
- No code
- Create GKE instances behind the scene.
- Abstract everything from you(cloud storage, cloud SQL, persistent disk, etc).
#### Cloud Composer:
- Managed workflow orchestration tools based on the apache airflow open-source tool.
- Supported the python language.
- Support varieties of operators
- Support event-based trigger and scheduling based trigger.
- Support hybrid(multiple clouds, cloud to on-prem).
- Support API.
- Different services used behind the scene.
    - App engine
    - Cloud Storage
    - GKE
    - Cloud IAP
    - Cloud SQL
    
[Top](#data-engineer-guide)

#### BigQuery ML
- Allow you to create and execute machine learning models in BigQuery using SQL.
- Supported models by BigQuery ML
    - **Linear Regression:** (For Forecasting) 
        - eg. The sales of the item on a given day or time.
    - **Binary Logistic Regression:** (For Classification)
        - Labels must only have two possible values. (eg. customer will purcahse or not)
    - **Multiclass Logistic Regression:** (For Classification)
        - Labels can have upto 50 unique values 
        - Prediction can fall into multiple categories. eg. low, medium, high
    - **K-means Clustering:**: (For data segmentation)
        - Used for unsupervised learning
        - Model training does not require labels nor split data for training or evaluation.
    - **Matrix Factorization:** (For production recommendation)
    - **Time Series:** (For time serious forcasting eg. handle holidays)
    - **Deep Neural Network:** (For creating TensorFlow based deep neural network for classification and regression models)
- Model evaluation functions
- ``CREATE OR REPLACE  model `dataset.modelname` options (model_type=[modeltype], input_label_column=[column], ...)``

[Top](#data-engineer-guide)

#### **Bigquery ML Process:**
- ETL into BigQuery
- Pre-process the records (eg. join, create train model, etc) 
- Create a model (SQL query with training data)
- Evaluate the model data(SQL query with evaluate data)(verify)
- Predict the result set (SQL Query with test data)(provide data to model to get prediction)
##### **Bigquery ML Cheatsheet:**
- Label: Label is considered as a column of the table
- Feature: passed through to the model as part of the SQL query to get statistics about that column.
    - `SELECT * FROM ML.FEATURE_INFO (MODEL, 'mydataset.model)`
- Model: An object created inside bigquery dataset as model.
- Model Types: Linear Regression, Logistic Regression
    - ``CREATE OR REPLACE  model `dataset.modelname` options (model_type=[model-type])``
- Training Progress: To get model traning progress 
    - `select * from ML.TRAINING_INFO (MODEL 'mydataset.model')`
- Inspect weights
    - `select * from ML.WEIGHTS (MODEL 'mydataset.model', (<query>))`
- Prediction: 
    - `select * from ML.PREDICT (MODEL 'mydataset.model', (<query>))`

[Top](#data-engineer-guide)

#### Prebuild ML products
- **Cloud Vision API:** 
    - Identify the object detection, categorize content emotion detection, recognize the landmark, popular logo, text read also able to find inappropriate content from the image.
- **Cloud Translate API:**
    - Dynamically translate between languages using Google machine learning.
    - Support more than 100 languages.
    - Automatic language detection.
- **Cloud Dialogflow API:**
    - Dialogflow is a natural language understanding platform used to design and integrate a conversational user interface into mobile apps, web applications, devices, bots, interactive voice response systems, and so on.
- **Cloud text-to-speech API:**
    - Accurately convert text into various languages using an API powered by Google’s AI technologies
    - Support more than 40 languages.
    - Can convert to different voice format
    - Integrated REST and gRPC APIs
- **Cloud speech-to-text API:**
    - Accurately convert speech into text using an API powered by Google’s AI technologies
    - Support Synchronous Recognition, Asynchronous Recognition & Streaming Recognition.
- **Cloud Natural Language API:**
    - Natural Language uses machine learning to reveal the structure and meaning of the text
    - You can extract information about people, places, and events, and better understand social media sentiment and customer conversations.
    - You can build your cloud natural language model as per your organization requirements.
    - Score: sentiment ranges between -1.0 (negative) and 1.0 (positive) and corresponds to the overall emotional leaning of the text.
    - Magnitude: magnitude indicates the overall strength of emotion (both positive and negative) within the given text, between 0.0 and +inf.
- **Cloud Video Intelligence API:**
    - The powerful content discovery from the video.
    - You can also build your model as per your requirements.
        
[Top](#data-engineer-guide)

#### Cloud ML
- Learn from existing data
- ML is not rules, its an example
- useCases: recommendation systems, predictions, classifications
- Scaling tier AI Platform
    - BASIC
    - STANDARD_1
    - PREMIUM_1
    - BASIC_GPU
    - BASIC_TPU
    - CUSTOM
- Way to deploy ML model to Cloud ML
    - Create Bucket
    - Upload SavedModel to bucket
    - Create an AI Platform prediction model resources.
    - Create an AI Platform prediction version resources.
- Online vs batch prediction
    - Online: 
        - Optimized to minimize the latency of serving predictions.
        - Predictions returned in the response message.
        - We can predict using REST API
    - Batch:
        - Optimized to handle a high volume of instances in a job and to run more complex models.
        - Predictions written to output files in a Cloud Storage location that you specify.

[Top](#data-engineer-guide)

#### Cloud Auto ML
- Suite of machine learning products.
- Bring your data and build the model.
- It enables developers (who have limited knowledge of ML) to train high-quality models specific to their needs.
- Process:
    - Data Pre-Processing
    - ML Model Design
    - Tune ML model parameters
    - Evaluate
    - Deploy
    - Update

[Top](#data-engineer-guide)

### EXPLORE & VISUALIZE
#### Google Data Studio
- https://support.google.com/datastudio/answer/7020039?hl=en

[Top](#data-engineer-guide)

## **Miscellaneous Terms**
#### Roles of Data Engineer
- Access to data
- Data accuracy 
- Availability of computing resources
- Query performance
#### Data Lake
- Data Lake: Scaleable and secure platform that allows enterprises to ingest, store, process, and analyze any type and volumes of data. It can be structure or unstructured
#### Data warehouse
- Stored only when its use is defined.
- Provide faster insights
- Current/Historical reports
- Structure dataset
- Only create the records (not update)
- Slow insertion, fast read (based on type and amounts of data)
#### EL/ELT/ETL Transformation
##### EL (Extract & Load)
- Can be imported as it is without modifying eg. import from an existing database with the same table schema.
- If data is already cleaned. eg. copy cloud storage logs to BigQuery
##### ELT (Extract, Load & Transform)
- First import to destination and import at the destination. eg. import data to BigQuery and transform using SQL query.
- Usecase: if you don't know what kind of transformation you need on your data.
##### ETL (Extract, Transform & Load)
- If you want to store the data to destination after transformation. eg, transform raw data using dataflow and store it into BigQuery.
- When the query can't transform the raw data to the final output.
- when your data is flowing endlessly(streaming)

[Top](#data-engineer-guide)
<hr/>

