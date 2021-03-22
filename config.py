# This dictionary is to define metrics that we should extract data from and then
#    their exposed name as predicted metric
metrics = {
    'actual_metric_name1': 'actual_metric_name1_predict',
    'actual_metric_name2': 'actual_metric_name2_predict'
}
#
prom_url = 'http://localhost/'
expose_port = 8000
# interval in days
interval = 30
# chunk size in hour
chunk_size = 24