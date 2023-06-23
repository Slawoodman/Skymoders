import re
from django.db import models
import uuid
from users.models import Profile
from django.core.exceptions import ValidationError


def validation_file(value):
    if not value.name.endswith(('.zip', '.rar', '.7z')):
        raise ValidationError('Only Zip and rar are allowed')


class Mod(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to='modtitle/', default = 'default.png')
    modfile = models.FileField(upload_to="files/", validators=[validation_file])
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(null=True, default=0, blank=True)
    vote_ration = models.IntegerField(null=True, default=0, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    
    def __str__(self) -> str:
        return self.title
    

    class Meta:
        ordering = ['-vote_total', '-vote_ration', '-title']
    

    @property
    def getVoters(self):
        voters = self.review_set.all().values_list('owner__id', flat=True)
        return voters

    @property
    def getImage(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url


    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        if totalVotes == 0:
            return 
        ration = (upVotes / totalVotes )*100
        self.vote_total = totalVotes
        self.vote_ration = round(ration, 2)
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    mod = models.ForeignKey(Mod, on_delete=models.CASCADE)
    created = models.TimeField(auto_now_add=True)
    body = models.TextField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)


    class Meta:
        unique_together = [['owner', 'mod']]

    def __str__(self) -> str:
        return self.value


class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Mod, null=True, blank=True, on_delete=models.CASCADE)
    user_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(null=True, blank=True, upload_to='modgallery/')

    def __str__(self):
        return f'{self.parent} {self.id}'

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.TimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self) -> str:
        return self.name