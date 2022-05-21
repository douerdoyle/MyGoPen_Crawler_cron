# MyGoPen_Crawler_cron
## Introduction
This crawler can get article data from the MyGoPen website(https://www.mygopen.com/)<br>
Each article data will split to title, content and tags and store into Elasticsearch server<br>

## How to establish the service

```
# Create the docker container
docker-compose up -d
```

You may use this command to trigger crawler immediately<br>
```
docker exec -it mygopen_crawler python ./schedule/mygopen_crawler.py
```
