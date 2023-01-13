from django.shortcuts import render
from django.views import View
from pathlib import Path
import json
from . import models
BASE_DIR = Path(__file__).resolve().parent


class LocationCodeView(View):
	def get(self, request):
		country_code =request.GET.get('country_code')
		with open(BASE_DIR/'functions/location_code.json', 'r') as f:
			data = json.load(f)['data']
			data = sorted(data, key=lambda d: d['location_name'])
			for line in data:
				if line['location_code_parent'] == country_code:
					LOCATION_CODE.append((line['location_code'], line['location_name']))

		return render(request, '', context = LOCATION_CODE)


class ProjectListView(View):
	def get(self, request):
		projects = models.ProjectModel.objects.filter(creator = request.user)
		print(projects)
		return render(request, 'app_serp/snipets/project_list.html', {'projects': projects})

class ProjectView(View):
	def get(self, request):
		return render(request, 'app_serp/project.html')

class ProjectAddView(View):
	def get(self, request):
		return render(request, 'app_serp/project_add.html')

class DashboardView(View):
	def get(self, request):
		return render(request, 'app_serp/dashboard.html')

class TopicView(View):
	def get(self, request):
		return render(request, 'app_serp/topic.html')






