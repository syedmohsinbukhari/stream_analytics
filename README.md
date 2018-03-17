# Stream Analytics
This is a repository for a course project 'CS 5312 - Big Data Analytics'

### Prerequisites
- Python 3 (Python 2 will not work as expected because it lacks "good" UTF-8 support)
- Tweepy (For streaming tweets)

### How to install
- Make sure you have the prerequisites
- Clone this repository (`git clone https://github.com/syedmohsinbukhari/stream_analytics.git` )

### How to use this code?
#### Prepare configuration files
- Make sure you have your credentials in this file (`/path/to/stream_analytics/scripts/conf/api_keys.txt`). This file should contain the following four lines with appropriate replacement of credentials acquired from `apps.twitter.com`.<br/>*Note: Replace '<' and '>' too.*
    1. \<consumer_token\>
    2. \<consumer_secret\>
    3. \<access_token\>
    4. \<access_token_secret\>
- Make sure you have a file that contains one tag per line to filter from Twitter Streaming API. This file must be located here (`/path/to/stream_analytics/scripts/conf/tags.txt`)
    1. tag1
    2. \#tag2
    3. tag3

#### How to run built in scripts
##### twitter_streamer.py

```shell
cd /path/to/stream_analytics
python3 scripts/twitter_streamer.py
```
