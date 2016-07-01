from addressesapp.models import Person
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import csv

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
                make_option('--output',
                             dest='output', type='string',
                             action='store',
                             help='output file'),
       )

    def person_data(self, person):
            return [person.name,person.mail]

    def handle(self, *args, **options):
         outputfile = options['output']
         contacts = Person.objects.all()
         
         header = ['Name','email']
         f = open(outputfile,'wb')
         writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
         writer.writerow(header)
         for person in contacts:
             writer.writerow(self.person_data(person))