# TwitterPullCounts
Simple fun project to pull counts of news website url shares from twitter during the FB outage

You will need a few things in place before you can run the code directly.

1) The websites for which we need the data are in the excel file SniffTest_Sources_adfontesmedia. Modify this for your own purposes. The code only gets the counts for websties.
2) Create a python file called twitter_auth.py with the following lines

```
import os
def auth():
    os.environ['TOKEN']= '' # insert your token from the the twitter API here
    return os.getenv('TOKEN')
```

This is how your code can login to twitter and get the tweets. You need to apply for a developer account first. Usually comes through in a day if you are an academic.

3) ??
4) Enjoy!
