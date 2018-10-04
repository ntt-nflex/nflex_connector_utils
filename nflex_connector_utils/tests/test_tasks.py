import unittest

from flexer.context import FlexerContext
from flexer import CmpClient
import pytest
import requests_mock

from nflex_connector_utils import set_task_percentage


@pytest.fixture(scope="class")
def mock(request):
    m = requests_mock.Mocker()
    m.start()
    request.addfinalizer(m.stop)
    request.cls.mock = m
    return m


@pytest.mark.usefixtures("mock")
class TestTasks(unittest.TestCase):
    def test_tasks(self):
        auth = ('username', 'password')
        cmp_client = CmpClient(url='http://localhost',
                               auth=auth,
                               access_token='foo')

        task_id = 'task-1'
        context = FlexerContext(cmp_client=cmp_client)

        # Should do nothing
        set_task_percentage(context, None, 100)

        self.mock.post('http://localhost/tasks/task-1/update', text='null')
        set_task_percentage(context, task_id, 100)

        self.mock.post('http://localhost/tasks/task-1/update', text='"Oops"',
                       status_code=500)
        with pytest.raises(Exception) as e:
            set_task_percentage(context, task_id, 100)
        assert 'Got bad response from tasks API' in str(e)
