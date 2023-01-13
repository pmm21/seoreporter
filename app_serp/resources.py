from import_export import resources
from import_export.fields import Field
from . import models

class KeywordResource(resources.ModelResource):
	class Meta:
		model = models.KeywordModel

	def before_import(self, dataset, using_transactions, dry_run, **kwargs):
		try:
			topic_id = kwargs['topic'][0]
			data = []
			for line in dataset:
				data.append(topic_id)
			dataset.append_col(data, header='topic')
		except:
			pass