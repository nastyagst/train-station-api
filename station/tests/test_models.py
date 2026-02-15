from django.test import TestCase
from station.models import Train, TrainType


class ModelTest(TestCase):
    def test_tarin_str(self):
        train_type = TrainType.objects.create(
            name="Intercity"
        )
        train = Train.objects.create(
            name="Express 1",
            cargo_num = 5,
            places_in_cargo = 20,
            train_type = train_type
        )

        self.assertEqual(str(train), "Express 1")

    def test_train_capacity(self):
        train_type = TrainType.objects.create(
            name="Suburban"
        )
        train = Train.objects.create(
            name="Elektrichka 1",
            cargo_num=10,
            places_in_cargo=50,
            train_type=train_type
        )

        self.assertEqual(train.capacity, 500)
