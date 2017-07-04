# Python
import importlib
import time

# Packages
from django.core.management import BaseCommand


class Command(BaseCommand):
    import_datasets = ['jekuntmeer', 'socialekaart']

    def add_arguments(self, parser):
        parser.add_argument(
            'dataset',
            nargs='*',
            default=self.import_datasets,
            help="Dataset to use, choose from {}. Defaults to all the datasets.".format(
                ', '.join(self.import_datasets))
        )

    def handle(self, *args, **options):
        start = time.time()

        datasets = options['dataset']

        for ds in datasets:
            if ds not in self.import_datasets:
                self.stderr.write(f'Unkown dataset: {ds}')
                return

        # Importing and running batch
        for dataset in datasets:
            module_path = f'datasets.{dataset}.batch'
            batch = importlib.import_module(module_path)
            batch.run()

        self.stdout.write(
            "Total Duration: %.2f seconds" % (time.time() - start)
        )
