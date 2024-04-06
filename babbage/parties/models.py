from django.db import models

class Person(models.Model):
    qid = models.PositiveBigIntegerField("Wikidata QID", primary_key=True)
    name = models.CharField(max_length=200, null=False)
    presumed = models.BooleanField(default=False)
    birth = models.DateField(null=True)
    death = models.DateField(null=True)

    def __str__(self):
        return f'{self.name} (Q{self.qid})'
    
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


class Guest(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    name = models.ForeignKey(Person, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.party}: {self.name}"
    
    class Meta:
        unique_together = ["party", "name", "source"]

    
