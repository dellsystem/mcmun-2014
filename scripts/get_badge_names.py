import csv

from committees.models import DelegateAssignment as D


csv_writer = csv.writer(open('badges.csv', 'wb'))
csv_writer.writerow(['name', 'school', 'committee', 'character'])


for i, d in enumerate(D.objects.filter(delegate_name__isnull=False)):
    data = [
        d.delegate_name,
        d.committee_assignment.school.school_name,
        d.committee_assignment.committee.name,
        d.committee_assignment.assignment,
    ]
    csv_writer.writerow(map(lambda s: s.encode('utf-8'), data))

print i
