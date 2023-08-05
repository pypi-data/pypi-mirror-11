from taiga.requestmaker import RequestMaker
from taiga.models import Membership, Memberships
import unittest
from mock import patch


class TestMemberships(unittest.TestCase):

    @patch('taiga.models.base.ListResource._new_resource')
    def test_create_severity(self, mock_new_resource):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        mock_new_resource.return_value = Membership(rm)
        mb = Memberships(rm).create(1, 'stagi.andrea@gmail.com', 2)
        mock_new_resource.assert_called_with(
            payload={
                'project': 1,
                'email': 'stagi.andrea@gmail.com',
                'role': 2,
            }
        )
