from django.db import models

class Person(models.Model):
    qid = models.CharField("Wikidata QID", max_length=32, primary_key=True)
    name = models.CharField(max_length=200, null=False)
    presumed = models.BooleanField(default=False)
    birth = models.DateField(null=True)
    death = models.DateField(null=True)
    gender = "female"
    occupation = "DJ"
    nationality = "Angola"
    aliases = "Oliver Tater Tizzle"
    birthname = "Bear"
    birthplace = "Portland"
    spouse = "Baxter the sad stuffed teddy"
    deathcause = "perfuming with rancid seagull poo"

    def __str__(self):
        return f'{self.name} ({self.qid})'
    
    class Meta:
        ordering = ["name", "qid"]


class Source(models.Model):
    sid = models.CharField("Source ID", max_length=80, primary_key=True)
    source = models.CharField(max_length=80, null=True)
    quote = models.TextField(null=False)
    pages = models.CharField(max_length=80, null=True)

    def __str__(self):
        return self.sid
    
    class Meta:
        ordering = ["sid"]


class Party(models.Model):
    pid = models.CharField("Party ID", max_length=80, primary_key=True)
    year = models.SmallIntegerField(null=False)
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

    def __str__(self):
        return f"{self.party}: {self.guest} [{self.source}]"
    
    class Meta:
        unique_together = ["party", "guest", "source"]
        ordering = ["party", "guest"]

    
