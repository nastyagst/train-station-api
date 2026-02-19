from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from station.models import Train, TrainType
from station.serializers import TrainListSerializer

TRAIN_URL = reverse("station:train-list")


def sample_train(**params):
    defaults = {
        "name": "Average Train",
        "cargo_num": 5,
        "places_in_cargo": 60,
    }
    defaults.update(params)

    if "train_type" not in defaults:
        defaults["train_type"] = TrainType.objects.create(name="Default Type")

    return Train.objects.create(**defaults)


class UnauthenticatedTrainApiTests(APITestCase):
    def test_auth_required(self):
        res = self.client.get(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTrainApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "testuser",
            "test1"
        )
        self.client.force_authenticate(self.user)

    def test_list_trains(self):
        sample_train()
        sample_train(name="Yellow Train")

        res = self.client.get(TRAIN_URL)

        trains = Train.objects.all().order_by("id")
        serializer = TrainListSerializer(trains, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_train_forbidden(self):
        train_type = TrainType.objects.create(name="Express")
        payload = {
            "name": "Red Train",
            "cargo_num": 10,
            "places_in_cargo": 20,
            "train_type": train_type.id
        }
        res = self.client.post(TRAIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            "admin",
            "admin1"
        )
        self.client.force_authenticate(self.user)

    def test_create_train(self):
        train_type = TrainType.objects.create(name="Night Express")
        payload = {
            "name": "Fast Train",
            "cargo_num": 8,
            "places_in_cargo": 100,
            "train_type": train_type.id
        }
        res = self.client.post(TRAIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        train = Train.objects.get(id=res.data["id"])
        self.assertEqual(train.name, payload["name"])