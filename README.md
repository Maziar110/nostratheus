# Welcome to Nostratheus Project
**Nostratheus is a project to use Machine Learning to predict Prometheus metrics**

It fetches one or more metric/s for a defined period of time and then traines a model based on time(as X) and it's value in that time (as Y) then saves that in file and an exporter will use that/those file/s to expose new predicted metrics for prometheus. 

## How to config the project

- You should config you prometheus host in config file, if there is authentication, you should handle it in code by yourself since for now it just works with unauthenticated hosts.

- You can define the metric that you are going to fetch in config file and also assign it with a new name which will be exposed to prometheus.

- Also you can define data period which we use to train the model(by defult it is 1 month)

***
**Tip:** If you want to have a lighter trained model to consume less memory, you should choose your period wisely also there is a `max_depth=6` which you can change(By increasing this value, accuracy will be more but memory consumption also gets increased)
***
## How to run the project

The `book_of_future.py` is responsible for training the model and runs just once to train model. You can run it your self or just run `pigeon.py` which is prometheus exporter and if there is no trained file, runs it and then exposes predicted values to prometheus.


`If you had any question, feel free to be in touch with me`