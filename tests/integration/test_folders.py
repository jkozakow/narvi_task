import pytest
from rest_framework.test import APITestCase

from narvi_task.users.models import User


@pytest.mark.django_db(True)
class TestFolderResetView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.force_authenticate(user=self.user)

    def test_populate_data_move_reset_folders_success(self):
        # make sure that at start of application folders table is empty
        folders_response = self.client.get("/api/folders/", format="json")
        assert folders_response.status_code == 200
        assert folders_response.json() == []

        # do reset folders API call which also populates data
        reset_folders_response = self.client.get("/api/reset_folders/", format="json")
        assert reset_folders_response.status_code == 200

        # check folders data is correct
        folders_response = self.client.get("/api/folders/", format="json")
        assert folders_response.status_code == 200
        assert len(folders_response.json()) == 105
        assert folders_response.json()[0] == {
            "names": ["adhoc_charge_amt", "adhoc_charge_amt_usd"],
            "prefix": "adhoc_charge_amt",
        }
        assert folders_response.json()[1] == {
            "names": ["admin_refund_amt", "admin_refund_amt_usd"],
            "prefix": "admin_refund_amt",
        }

        # call API to move names into another folder
        name_to_move = "bags_in_shelves"
        move_name_response = self.client.patch(
            f"/api/names/{name_to_move}/move_name_into_folder/",
            data={"folder_name": "adhoc_charge_amt"},
        )
        assert move_name_response.status_code == 200
        assert move_name_response.json() == {
            "name": "bags_in_shelves",
            "folder_name": "adhoc_charge_amt",
        }

        # check that the name was moved into given folder
        folders_response = self.client.get("/api/folders/", format="json")
        assert folders_response.json()[0] == {
            "names": ["adhoc_charge_amt", "adhoc_charge_amt_usd", "bags_in_shelves"],
            "prefix": "adhoc_charge_amt",
        }

        # check that reset_folders works and data is like when pulled from csv file
        reset_folders_response = self.client.get("/api/reset_folders/", format="json")
        assert reset_folders_response.status_code == 200
        folders_response = self.client.get("/api/folders/", format="json")
        assert folders_response.json()[0] == {
            "names": ["adhoc_charge_amt", "adhoc_charge_amt_usd"],
            "prefix": "adhoc_charge_amt",
        }

    def test_move_name_into_folder_does_not_exist(self):
        # make sure that at start of application folders table is empty
        folders_response = self.client.get("/api/folders/", format="json")
        assert folders_response.status_code == 200
        assert folders_response.json() == []

        # expect failed move
        name_to_move = "arrived_customer_location_date_time_pt"
        move_name_response = self.client.patch(
            f"/api/names/{name_to_move}/move_name_into_folder/",
            data={"folder_name": "num_items"},
        )
        assert move_name_response.status_code == 404
        assert move_name_response.json() == {
            "detail": "Folder with name=num_items not found"
        }
