### Google Cloud Function with Serverless

#### Development with Docker

* Check example-env for details
* Run docker container with gcloud function for local observation
```bash
cd src &&\
docker-compose -f docker-compose-dev.yaml up --build
```

#### Create Google PubSub topic and subscription
* Create topic
```bash
gcloud pubsub topics create MyEventsTopic
```
* Create subscription
```bash
gcloud pubsub subscriptions create MyEventsTopicSubscription --topic MyEventsTopic --ack-deadline=20
```

#### Install serverless
```bash
sudo npm install -g serverless
sudo npm install --save serverless-google-cloudfunctions
```

```bash
serverless create --template google-python\
--path src --name my-gcloud-function
```

#### Package and deploy 

* Create template if it not exists
```bash
serverless create --template google-python --path event_processor
```
* Deploy with deployment manager
```bash
serverless package
serverless deploy
```