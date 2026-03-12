from django.db import models

class ReportedURL(models.Model):
    url = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

class VoteRecord(models.Model):
    report = models.ForeignKey(ReportedURL, on_delete=models.CASCADE, related_name='voters')
    ip_address = models.GenericIPAddressField()
    vote_type = models.CharField(max_length=10) # 'up' or 'down'

    class Meta:
        unique_together = ('report', 'ip_address')



