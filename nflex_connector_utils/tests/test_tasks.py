import pytest
import requests_mock

from flexer.context import FlexerContext
from flexer import CmpClient
from nflex_connector_utils import set_task_percentage


class TestTasks(object):
    @requests_mock.Mocker()
    def test_tasks(self, mock):
        auth = ('username', 'password')
        cmp_client = CmpClient(url='http://localhost',
                               auth=auth,
                               access_token='foo')

        task_id = 'task-1'
        context = FlexerContext(cmp_client=cmp_client)

        # Should do nothing
        set_task_percentage(context, None, 100)

        mock.post('http://localhost/tasks/task-1/update', text='null')
        set_task_percentage(context, task_id, 100)

        mock.post('http://localhost/tasks/task-1/update', text='"Oops"',
                  status_code=500)
        with pytest.raises(Exception) as e:
            set_task_percentage(context, task_id, 100)
        assert 'Got bad response from tasks API' in str(e)
