VERSION = '0.11'

url = None
url_file = None

target_file = 'testlog.log'

log_file = '/var/log/siege.log'
#duration = '10S'  # seconds
repeat = 5  # for siege command
max_concurrent = 1000
num_samples = 3  #The samples number of every setp testing.
base_concurrent = 100
step_concurrent = 100

fails_allowed = 0.1  # 0.1 means 10%

siege_log_line_length = 121
custom_log_line_length = 131

plotting = True

test_type = 'load test'
