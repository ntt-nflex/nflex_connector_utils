import httplib


def set_task_percentage(context, task_id, percentage):
    if task_id is None:
        return

    data = {'percentage': percentage}
    response = context.api.post(path='/tasks/%s/update' % task_id, data=data)
    if response.status_code != httplib.OK:
        raise Exception(
            'Got bad response from tasks API: %d, %s' % (
                response.status_code, response.content))
