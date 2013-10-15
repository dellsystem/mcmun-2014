from django.db import models

from committees.models import Committee


year_choices = (
    ('U0', 'U0 (first year)'),
    ('U1', 'U1'),
    ('U2', 'U2'),
    ('U3', 'U3'),
    ('U4+', 'U4 and above'),
)

coordinator_choices = (
    ('staff-room', 'Staff Room Coordinator'),
    ('drc', 'Delegate Resource Center Coordinator'),
    ('page', 'Page Coordinator'),
    ('events-tl', 'Entertainment and Events Team Leader'),
    ('events-coord', 'Entertainment and Events Coordinator'),
    ('media', 'Media Team Logistics Coordinator'),
    ('photo', 'Photography Coordinator'),
    ('occc', 'Opening and Closing Ceremonies Coordinator'),
    ('food', 'Food Coordinator'),
    ('editor-in-chief', 'Editor-in-Chief for The Ambassador'),
    ('senior-editor', 'Senior Editor for The Ambassador'),
)

non_coordinator_choices = (
    ('log-or-com', 'Logistical or committees staff'),
    ('log', 'Logistical staff only'),
    ('com', 'Committees staff only'),
    ('com-then-log', 'Committees staff first, then logistical staff'),
    ('log-then-com', 'Logistical staff first, then committees staff'),
    ('none', 'None'),
)

cv_upload_path = 'staff-application/coordinator_cvs/'

logistical_choices = (
    ('staff-room', 'Staff room'),
    ('drc', 'Delegate Resource Center'),
    ('page', 'Page'),
    ('group-leader', 'Group leader (Pub Crawl)'),
    ('venue-staff', 'Venue staff (Pub Crawl)'),
    ('photographer', 'Photographer'),
    ('occc', 'Opening Ceremonies and Closing Ceremonies staff'),
    ('food', 'Food staff'),
)


class StaffApp(models.Model):
    """
    The questions for the other staff applications have not been sent to me yet, so I'm just guessing as to which questions will be reused. Hopefully this set is a valid subset. If not I will make it one.
    """
    class Meta:
        abstract = True

    full_name = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    year = models.CharField(choices=year_choices, max_length=3)
    email = models.EmailField(verbose_name="Please enter your McGill email address. (Note that you must be a McGill student to staff at McMUN; contact staff@mcmun.org if you have any questions.)")
    phone_number = models.CharField(max_length=20)

    attend_training = models.BooleanField(verbose_name="Are you available to attend all training sessions?", help_text="<a href=\"/staff-key-dates\">View training session dates &raquo;</a>")
    attend_mcmun = models.BooleanField(verbose_name="Are you available to attend McMUN 2014 (Thursday, January 23, 2014 to Sunday, January 26, 2014)?")


class CoordinatorApp(StaffApp):
    preferred_position_1 = models.CharField(choices=coordinator_choices, max_length=20)
    preferred_position_2 = models.CharField(choices=coordinator_choices, max_length=20)
    preferred_position_3 = models.CharField(choices=coordinator_choices, max_length=20)

    occc_experience = models.TextField(null=True, blank=True, verbose_name="Please describe any previous stage managing experience you have.")
    event_experience = models.TextField(null=True, blank=True, verbose_name="Please describe any previous event planning experience you have.")

    cv = models.FileField(upload_to=cv_upload_path, verbose_name="Upload your CV (PDF, DOC or DOCX)")

    can_drive = models.BooleanField(verbose_name="Can you legally drive in Canada?")
    leadership = models.TextField(verbose_name="Please describe any previous leadership positions you have held.")
    why_you = models.TextField(verbose_name="Please outline why you are a good candidate for each preferred position. (Provide a separate answer for each portfolio).")

    best_trait = models.CharField(max_length=100, verbose_name="What is your best trait? (1 word or phrase)")
    greatest_fault = models.CharField(max_length=100, verbose_name="What is your greatest fault? (1 word or phrase)")

    other_choices = models.CharField(choices=non_coordinator_choices, max_length=12, verbose_name="If you are not chosen for a Coordinator position, would you like to be considered for any of the following?")

    additional_comments = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.full_name


class CommitteesApp(StaffApp):
    preferred_committee_1 = models.ForeignKey(Committee, related_name='+')
    preferred_committee_2 = models.ForeignKey(Committee, related_name='+')
    preferred_committee_3 = models.ForeignKey(Committee, related_name='+')

    mun_experience = models.TextField(verbose_name="Please describe any previous Model United Nations experience you have. If you do not have any previous Model United Nations experience, please describe any relevant experience (e.g., debating, public speaking, etc.).")

    work_with = models.TextField(verbose_name="Is there anyone in particular you would like to work with?", null=True, blank=True)
    another_position = models.BooleanField(verbose_name="Are you amenable to another position (i.e. an alternative committee or a logistical staff position) if not selected for one of the above committees?")

    additional_comments = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.full_name


class LogisticalApp(StaffApp):
    preferred_position_1 = models.CharField(choices=logistical_choices, max_length=20)
    preferred_position_2 = models.CharField(choices=logistical_choices, max_length=20)
    preferred_position_3 = models.CharField(choices=logistical_choices, max_length=20)

    # Need a different verbose_name (mentions carnival, frosh, etc)
    mun_experience = models.TextField(verbose_name="Please describe any previous Model United Nations experience you have. If you do not have any previous Model United Nations experience, please describe any relevant experience (e.g., debating, public speaking, event planning, frosh or carnival leader, etc.).")

    # Not going to go to the trouble of making them show up automatically
    photography_experience = models.TextField(verbose_name="If you indicated that you're interested in the photographer position, please list any relevant photography experience.", null=True, blank=True)

    another_position = models.BooleanField(verbose_name="Are you amenable to another position (i.e. an alternative logistical staff position) if not selected for one of the above positions?")

    additional_comments = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.full_name
