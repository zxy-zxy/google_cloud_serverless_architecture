####Streaming pipeline with Apache Beam, Google PubSub and Google DataFlow
####Execute the pipeline
* Assign Google service account key path to environment variable
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/usr/.gcloud/service_account.json
```
#####Run with local runner
```bash
python process_streaming.py \
--streaming \
--input-topic <your_pubsub_topic_id_here> \
--output-table <your_bigquery_table_id_here> 
```
#####Run with Dataflow runner
```bash
python process_streaming.py \
--project <your_project_id_here> \
--streaming \
--input-topic <your_pubsub_topic_id_here> \
--output-table  <your_bigquery_table_id_here> \
--runner DataflowRunner \
--temp_location gs://<your_project_id_here>/temp \
--staging_location gs://<your_project_id_here>/staging
```

* *PubSub input topic* should be described as  projects/project_id/topics/topic_id
* *BigQuery output table* should be defined as project_id:dataset.table
