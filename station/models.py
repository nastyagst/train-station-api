from  django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source_routes")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="destination_routes")
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}"


class TrainType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="journeys")

    class Meta:
        ordering = ["-departure_time"]

    def __str__(self):
        return f"{self.route} ({self.departure_time})"


class Order(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("journey", "cargo", "seat")
        ordering = ["cargo", "seat"]

    @staticmethod
    def validate_ticket(cargo, seat, train, error_to_raise):
        if not (1 <= cargo <= train.cargo_num):
            raise error_to_raise({
                "cargo": f"cargo number must be in range [1, {train.cargo_num}]"
            })
        if not (1 <= seat <= train.places_in_cargo):
            raise error_to_raise({
                "cargo": f"seat number must be in range [1, {train.places_in_cargo}]"
            })

    def clean(self):
        Ticket.validate_ticket(
            self.cargo,
            self.seat,
            self.journey.train,
            ValidationError
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return f"str{(self.journey)} (cargo: {self.cargo}, seat: {self.seat}"

