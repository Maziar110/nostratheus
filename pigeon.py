from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily,REGISTRY, CounterMetricFamily
import book_of_future
import sys
import time
from datetime import datetime
import os
import config
import joblib
import resource


metrics = config.metrics
file_dir = './trained_models/'


def memory_limit():
    """
        I'm limiting the app not to use all the ram and disrupt the server while running it.
        it's smart of programmer to keep this in mind ( although it might end to disruption in app performance)
    """
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    mem_limit = (int((get_memory() * 1024) - 100000000), hard)
    resource.setrlimit(resource.RLIMIT_AS, mem_limit)


def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:', 'SwapFree:'):
                free_memory += int(sline[1])
    return free_memory


def trained(file_name):
    #This function opens trained model and returens the predicted result. 

    with open(file_name, 'rb') as file:
        model = joblib.load(file, mmap_mode=None)
        #print(model)
        t = datetime.utcnow()
        day = t.day
        weekday = t.weekday()
        sec_from_day = (t - t.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        try:
            predicted = model.predict([[sec_from_day, day, weekday]])
            return predicted
        except Exception as e:
            print(e)
            return 0


class Collector(object):

    def __init__(self):
        pass

    def collect(self):
        """
        This function get's the predicted metric from the model which is pickled in a joblib file
        """
        for item in metrics:
            file_name = file_dir + item + '.joblib'
            if os.path.exists(file_name):
                predicted = trained(file_name)
                print(f" Predicted value for {metrics[item]} is {predicted} ")
                exposed_metric = GaugeMetricFamily(metrics[item], 'Predicted Value')
                exposed_metric.add_metric(metrics[item], value=predicted )
                yield exposed_metric
            else:
                book_of_future.train_models()


if __name__ == '__main__':
    memory_limit()

    # Usage: json_exporter.py port endpoint
    try:
        start_http_server(config.expose_port)
        REGISTRY.register(Collector())
    except MemoryError:
        sys.stderr.write('\n\nERROR: Memory Exception\n')
        sys.exit(1)

    while True:
        time.sleep(1)

