### Data processing pipeline on Google Cloud 

This repo contains POC of small serverless data processing pipeline.

#### Serverless function
[First part](gcloud_function/README.md) contains example of serverless function which is aimed to 
pass incoming data to pubsub with 
* Google Cloud Functions
* Google Cloud PubSub  

Development environment could be setup with a Docker, 
however deployment cycle is based on [Serverless framework](https://serverless.com/).

#### Streaming pipeline
[Second part](gcloud_streaming_pipeline/README.md) contains implementation of streaming pipeline which is 
implemented with following technologies:
* Google Cloud PubSub  
* Google Cloud DataFlow
* Google BigQuery