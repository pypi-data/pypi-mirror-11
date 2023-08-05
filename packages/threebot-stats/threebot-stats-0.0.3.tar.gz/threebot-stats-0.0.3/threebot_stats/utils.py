''' Utility functions that gather statistical information on a Workflow
'''

''' Number of logs for Workflow '''
def count_logs(workflow):
    return workflow.workflowlog_set.count()


''' Log execution time as a timedelta object '''
def response_time(workflow_log):
    diff = workflow_log.date_finished - workflow_log.date_started
    return diff.total_seconds()


''' Filter logs with start and end time '''
def _executed_logs(workflow):
    return workflow.workflowlog_set.exclude(date_finished__isnull=True, date_started__isnull=True)


def average_response_time(workflow):
    times = [response_time(log) for log in _executed_logs(workflow)]
    return sum(times) / float(len(times))


''' Response times of last n logs in seconds, as a list '''
def response_time_series(workflow, n):
    recent_logs = list(_executed_logs(workflow).order_by('-date_finished'))[-n:]
    return [response_time(log) for log in recent_logs]


''' Total of seconds the Workflow has run '''
def impact(workflow):
    logs = _executed_logs(workflow)
    seconds = sum([response_time(log) for log in logs])
    return seconds
