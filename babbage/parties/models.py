from django.db import models

class Person(models.Model):
    qid = models.CharField("Wikidata QID", max_length=32, primary_key=True)
    name = models.CharField(max_length=256, null=False)
    birth = models.CharField(max_length=32, null=True)
    death = models.CharField(max_length=32, null=True)
    gender = models.CharField(max_length=32, null=True)
    occupation = models.CharField(max_length=256, null=True)
    nationality = models.CharField(max_length=256, null=True)
    aliases = models.CharField(max_length=256, null=True)
    birthname = models.CharField(max_length=256, null=True)
    birthplace = models.CharField(max_length=256, null=True)
    spouse = models.ForeignKey("Person", on_delete=models.SET_NULL, null=True)
    deathcause = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'{self.name} ({self.qid})'
    
    class Meta:
        ordering = ["name", "qid"]


class Book(models.Model):
    bid = models.CharField("Book ID", max_length=80, primary_key=True)
    citation = models.CharField(max_length=80, null=True)

    def __str__(self):
        return self.bid
    
    class Meta:
        ordering = ["bid"]

class Source(models.Model):
    sid = models.CharField("Source ID", max_length=80, primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quote = models.TextField(null=False)
    pages = models.CharField(max_length=80, null=True)

    def __str__(self):
        return self.sid
    
    class Meta:
        ordering = ["sid"]



class Party(models.Model):
    pid = models.CharField("Party ID", max_length=80, primary_key=True)
    year = models.SmallIntegerField(null=True)
    month = models.SmallIntegerField(null=True)
    day = models.SmallIntegerField(null=True)

    def __str__(self):
        return self.pid
    
    class Meta:
        ordering = ["year", "month", "day"]
        verbose_name_plural = "parties"


class Mention(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    guest = models.ForeignKey(Person, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    presumed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.party}: {self.guest} [{self.source}]"
    
    class Meta:
        unique_together = ["party", "guest", "source"]
        ordering = ["party", "guest"]

    
