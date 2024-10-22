from django.db.models import Model, CharField, ForeignKey, CASCADE


class Folder(Model):
    prefix = CharField(blank=False, max_length=255)


class Name(Model):
    name = CharField(blank=False, max_length=255)
    folder = ForeignKey(Folder, related_name="names", on_delete=CASCADE)

    def __str__(self):
        return self.name
