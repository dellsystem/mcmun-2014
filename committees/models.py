import os

from django.db import models


position_paper_upload_path = 'position-papers/'

def get_position_paper_path(instance, filename):
	return os.path.join(position_paper_upload_path, str(instance.id) + os.path.splitext(filename)[1])


class Category(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural = 'categories'

	def __unicode__(self):
		return self.name


class Committee(models.Model):
	name = models.CharField(max_length=100)
	slug = models.CharField(max_length=20, unique=True)
	description = models.TextField()
	category = models.ForeignKey(Category)
	# Committees should be hidden until they are released
	is_visible = models.BooleanField(default=False)

	class Meta:
		ordering = ('category', 'id')

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('committee_view', [self.slug])

	def is_searchable(self):
		return self.is_visible


class CommitteeApplication(models.Model):
	"""
	An abstract base class used by all committee applications
	"""
	class Meta:
		abstract = True

	name = models.CharField(max_length=100)
	school = models.CharField(max_length=100)
	email = models.EmailField(max_length=255)
	head_delegate_name = models.CharField(max_length=100, verbose_name="Name of head delegate")
	field_of_study = models.CharField(max_length=100)
	previous_mun_experience = models.TextField(verbose_name="Describe your previous Model UN experience.")

	def __unicode__(self):
		return '%s from %s' % (self.name, self.school)


class UFCApplication(CommitteeApplication):
	class Meta:
		verbose_name = 'Committee application: UFC'
		verbose_name_plural = 'Committee applications: UFC'

	why_you = models.TextField(verbose_name='Why should you be a part of the UFC committee? What skills do you bring that are applicable to the specific mode of conduct?')
	guillotine = models.TextField(verbose_name='What is a Guillotine?')
	favourite_figure = models.TextField(verbose_name='Who is your favourite figure (athlete or otherwise) in the UFC?')
	defend_ufc = models.TextField(verbose_name='In 250 words or less, defend the UFC against a critique that it is a grotesque and violent sideshow. Why do you see it as a legitimate sport organization?')


class CEAApplication(CommitteeApplication):
	class Meta:
		verbose_name = 'Committee application: CEA (Detroit)'
		verbose_name_plural = 'Committee applications: CEA (Detroit)'

	why_you = models.TextField(verbose_name='Why should you be part of the United States Council of Economic Advisers? What qualifications do you have for this role?')
	which_corp = models.TextField(verbose_name='Which multinational corporation would you want to work for and why?')
	economic_policy = models.TextField(verbose_name='What is the role of the CEA for American economic policy?')
	auto_industry = models.TextField(verbose_name='Describe in 250 words or less the economic consequences of letting the American auto industry collapse in 2008.')


class ICCApplication(CommitteeApplication):
	class Meta:
		verbose_name = 'Committee application: ICC'
		verbose_name_plural = 'Committee applications: ICC'

	why_you = models.TextField(verbose_name='Why should you be part of the International Criminal Court committee? What skills do you have that would be applicable to trial simulation?')
	world_leader = models.TextField(verbose_name='Name a world leader that you would like to have a meal with and why.')
	chief_prosecutor = models.TextField(verbose_name='What role does the Chief Prosecutor play within the institutional framework of the ICC?')
	icc_role = models.TextField(verbose_name='Describe, in 250 words or less, the role the ICC and international law should have in international relations.')


class DEFCONApplication(CommitteeApplication):
	class Meta:
		verbose_name = 'Committee application: DEFCON'
		verbose_name_plural = 'Committee applications: DEFCON'

	why_you = models.TextField(verbose_name='Why should you be a part of the DEFCON committee? What can you bring to a war game committee?')
	juiche = models.TextField(verbose_name='What is Juiche and how does it relate to the international relations of the DPRK?')
	any_country = models.TextField(verbose_name='If you could lead any country in a war game situation (that is not the United States) which would it be and why?')
	six_party = models.TextField(verbose_name='Describe, in 250 words or less, what has been achieved through previous Six Party Talks.')


class AdHocApplication(CommitteeApplication):
	class Meta:
		verbose_name = 'Committee application: Ad-hoc'
		verbose_name_plural = 'Committee applications: Ad-hoc'

	greatest_skill = models.TextField(verbose_name='What is the greatest skill you have and how can that be applied to Model United Nations?')
	favourite_leader = models.TextField(verbose_name='Who is your favourite military leader and why?')
	proportional_response = models.TextField(verbose_name='What is the virtue of a proportional response?')
	why_law = models.TextField(verbose_name='Briefly argue, in 250 words or less, why a law must be obeyed even when it conflicts with morality.')


class CommitteeAssignment(models.Model):
	class Meta:
		ordering = ('school', 'committee')
		permissions = (("can_view_papers", "Can view position papers"),)

	# Number of delegates is usually 1, except in double-delegation committees
	school = models.ForeignKey('mcmun.RegisteredSchool')
	num_delegates = models.IntegerField(default=1)
	committee = models.ForeignKey(Committee)
	# The country or character name, in plain text
	assignment = models.CharField(max_length=255)
	notes = models.TextField(blank=True, null=True)
	position_paper = models.FileField(upload_to=get_position_paper_path, blank=True, null=True)

	def __unicode__(self):
		return "%s" % self.assignment

	def is_filled(self):
		return self.delegateassignment_set.filter(delegate_name__isnull=False).count() == self.num_delegates


class DelegateAssignment(models.Model):
	class Meta:
		unique_together = ('committee_assignment', 'delegate_name')

	committee_assignment = models.ForeignKey(CommitteeAssignment)
	# Blank until a delegate is there
	delegate_name = models.CharField(max_length=255, null=True, blank=True)

	def __unicode__(self):
		if self.delegate_name:
			return self.delegate_name
		else:
			return "N/A"


def create_delegate_assignments(sender, instance, created, **kwargs):
	"""
	Defines a post_save hook to create the right number of DelegateAssignments
	(with no delegate name specified) for each CommitteeAssignment
	"""
	if created:
		for i in xrange(instance.num_delegates):
			instance.delegateassignment_set.create()

models.signals.post_save.connect(create_delegate_assignments, sender=CommitteeAssignment)
