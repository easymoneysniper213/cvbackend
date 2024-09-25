import json
from django.core.management.base import BaseCommand
from api.models import Patent, Claim, Image, IndependentClaim, SystemIndependentClaim, SystemComponent

class Command(BaseCommand):
    help = 'Loads data from JSON file into the Patent database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file with patent data')

    def handle(self, *args, **options):
        json_file = options['json_file']
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
                for entry in data:
                    patent = Patent.objects.create(
                        key=entry['key'],
                        abstract=entry['abstract'],
                        description_link=entry['description_link']
                    )

                    for claim in entry['claims']:
                        Claim.objects.create(patent=patent, text=claim)

                    for image in entry['images']:
                        Image.objects.create(patent=patent, image_link=image)

                    for ind_claim in entry['indp_claims']:
                        IndependentClaim.objects.create(patent=patent, text=ind_claim)

                    for sys_ind_claim in entry['system_indp_claims']:
                        SystemIndependentClaim.objects.create(patent=patent, text=sys_ind_claim)

                    for component in entry['all_system_components']:
                        SystemComponent.objects.create(patent=patent, component=component)

            self.stdout.write(self.style.SUCCESS('Successfully loaded patent data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))
