from django.db import models
from django.contrib.auth.models import User
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

SE_DOMAINS, LANGUAGE_CODE, COUNTRY_CODE, LOCATION_CODE = [], [], [], []
with open(BASE_DIR/'functions/search_engine_domain.json', 'r') as f:
	for line in json.load(f)['data']:
		SE_DOMAINS.append((line['search_domain'], line['country']+" ("+line['search_domain']+" )"))

with open(BASE_DIR/'functions/location_code.json', 'r') as f:
	data = json.load(f)['data']
	data = sorted(data, key=lambda d: d['location_name'])
	country_code_list = []
	for line in data:
		if not line['location_code_parent']:
			COUNTRY_CODE.append((line['location_code'], line['location_name']))
			country_code_list.append(line['location_code'])

	for line in data:
		if line['location_code_parent'] in country_code_list:
			LOCATION_CODE.append((line['location_code'], line['location_name']))

with open(BASE_DIR/'functions/language_code.json', 'r') as f:
	for line in json.load(f)['data']:
		LANGUAGE_CODE.append((line['language_code'], line['language_name']+" ("+line['language_code']+" )"))

DEVICE = [
	('mobile', 'MOBILE'),
	('desktop', 'DESKTOP')
]

class ProjectModel(models.Model):
	project_name = models.CharField(max_length = 125)
	domain = models.CharField(max_length = 75)

	search_domain = models.CharField(default='google.com.vn',max_length=125, choices=SE_DOMAINS)
	language = models.CharField(default='vi', max_length=13, choices=LANGUAGE_CODE)
	country = models.IntegerField(default='2704', choices=COUNTRY_CODE)
	location = models.IntegerField(null=True, blank=True, choices=LOCATION_CODE)
	device = models.CharField(default='mobile', max_length=25, choices=DEVICE)

	creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	create_time = models.DateTimeField(auto_now_add = True)	

	class Meta:
		verbose_name = 'Project'

	def __str__(self):
		return self.project_name

class TopicModel(models.Model):
	topic_name = models.CharField(max_length = 125)
	keywords = models.TextField()
	project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Topic'

	def __str__(self):
		return self.topic_name

class PosToTrackModel(models.Model):
	pos1 = models.IntegerField(default=3)
	pos2 = models.IntegerField(default=10)
	pos3 = models.IntegerField(default=30)
	pos4 = models.IntegerField(default=50)
	pos5 = models.IntegerField(default=100)

	topic = models.OneToOneField(TopicModel, on_delete=models.CASCADE)

class AddvanceColumnShowModel(models.Model):
	parent = models.BooleanField(default=False)
	canibal = models.BooleanField(default=False)
	tag = models.BooleanField(default=False)
	target_url = models.BooleanField(default=False)

	topic = models.OneToOneField(TopicModel, on_delete=models.CASCADE)

class KeywordModel(models.Model):
	keyword = models.CharField(max_length=80)
	volumn = models.IntegerField(null=True, blank=True)
	volumn_history = models.JSONField(null=True, blank=True)

	parent = models.CharField( max_length=80, null=True, blank=True)
	tag = models.CharField( max_length=80, null=True, blank=True)
	target_url = models.CharField( max_length=80, null=True, blank=True)

	on_check = models.BooleanField(default=False)
	topic = models.ForeignKey(TopicModel, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Keyword'

	def __str__(self):
		return self.keyword

class SerpDataModel(models.Model):
	create_time = models.DateTimeField(auto_now_add=True)
	pos = models.IntegerField()
	url_found = models.URLField(max_length=200)
	top_10_data = models.JSONField()

	keyword = models.ForeignKey(KeywordModel, on_delete=models.CASCADE)











