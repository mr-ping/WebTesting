from settings import custom_log_line_length as len_line
import numpy as np


class Log(object):
    def __init__(self, file):
        self.log_file = file

    def get_steps_arrive_rate(self):
        """
        Compute the arrive rate of each step of testing.

        :return: Dict.
                 The arrive rates of testings like {'100': 0, '200': 0.14}
        """
        groups = self._get_groups()
        groups_rate = {}
        for group_id, group in groups.items():
            group_rate = self._get_final_result(group, 'arrive_rate')
            groups_rate[group_id] = group_rate
        return groups_rate

    def get_last_arrive_rate(self, num_logs):
        """
        Compute the arrive rate by log/logs at the end of log file.

        :param num_logs: The number of logs need to computed.
        :return: Int. Arrive rate.
        """
        logs_list = Log.get_last_logs(self.log_file, len_line, num_logs).split('\n')
        logs_list.remove('')
        arrive_rate = self._get_final_result(logs_list, 'arrive_rate')
        return arrive_rate

    def get_steps_trans_rate(self):
        groups = self._get_groups()
        groups_rate = {}
        for group_id, group in groups.items():
            group_trans_rate = self._get_final_result(group, 'trans_rate', -5)
            groups_rate[group_id] = group_trans_rate
        return groups_rate

    def get_steps_resp_time(self):
        groups = self._get_groups()
        groups_rate = {}
        for group_id, group in groups.items():
            group_resp_time = self._get_final_result(group, 'resp_time', -6)
            groups_rate[group_id] = group_resp_time
        return groups_rate

    def _get_final_result(self, logs_list, result_type, position=None):
        """
        Get the final result of one group.

        :param logs_list: A list of logs to computed.
        :return: float format. the rate.
        """
        result_list = self._get_result_list(logs_list, result_type, position)
        final_result = self._get_average_result(result_list)
        return final_result

    def _get_each_result(self, log, result_type, position):
        """
        Computing or direct getting the result of one-line from a log file.

        :param log: A one-line log waiting for computing
        :return: Float. The arrive rate.
        """
        log_components = log.split(',')
        if result_type == 'arrive_rate':
            try:
                result = float(log_components[-2]) / (int(log_components[-1]) + \
                     int(log_components[-2]))
            except ZeroDivisionError:
                result = 1
        else:
            result = float(log_components[position])
        return result


    def _get_result_list(self, log_list, result_type, position):
        """
        Extracting every particular testing elements from a log list to compose
        to a result list.

        :param log_list: The source list of results.
        :param result_type: The project type of analyzing.
        :param position: Where the element is in a single log.
        :return: The list of results. List.
        """
        result_list = []
        for log in log_list:
            result = self._get_each_result(log, result_type, position)
            result_list.append(result)
        result_list = self._remove_outlier(result_list)
        return result_list


    def _get_average_result(self, result_list):
        sum_result = 0
        for result in result_list:
            sum_result += result
        return sum_result / len(result_list)

    def _get_groups(self):
        """
        Organize logs into groups by the number of concurrent

        :return: Dict. The groups like {'100': [log1, log2], '200': [log3]}
        """
        with open(self.log_file) as f:
            groups = {}
            for log in f:
                log = log.strip()
                group_id = log.split(',')[0]
                if group_id not in groups.keys():
                    groups[group_id] = [log]
                else:
                    groups[group_id].append(log)
            return groups

    def _remove_outlier(self, result_list):
        #std = np.std(result_list)
        #mean = np.mean(result_list)
        #up_outlier = mean + (std * 3)

        #for res in result_list:
        #    if res > up_outlier:
        #        result_list.remove(res)
        #return result_list
        return result_list


    @staticmethod
    def get_last_logs(file, length_line, lines=1, step_num=None):
        """ Extract the last log/logs from a the siege log file.

        :param file: The position of siege log file.
        :param length_line: The average line's length of the file which
                            you locked in
        :param lines: The number of logs to extract from the end of the file.
        :param step_num: Concurrent number you want to add
        :return: String. The logs/log content.
        """
        position = -length_line * lines - 1
        with open(file, 'r') as f:
            content = ''
            f.seek(position, 2)
            lines_list = f.readlines()
            for i in reversed(range(lines)):
                if step_num:
                    line = '%9s,%s' % (str(step_num), lines_list[-(i+1)])
                else:
                    line = lines_list[-(i+1)]
                content += line
        return content

    @staticmethod
    def add_new_log(file, log):
        """ Add log/logs to the end of a file.

        :param file: The file position.
        :param log: the content of log/logs to appended.
        :return: None
        """
        with open(file, 'a') as f:
            f.write(log)
