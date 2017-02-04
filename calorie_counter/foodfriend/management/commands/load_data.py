from django.core.management import BaseCommand
from django.utils import timezone
from foodfriend.models import Food


def populate():
    Food.objects.update_or_create(name="Ryż brązowy", kcal=353, proteins=7.1, carbs=76.8, fats=1.9, grams=100)
    Food.objects.update_or_create(name="Boczek parzony", kcal=259, proteins=14, carbs=1.3, fats=22, grams=100)
    Food.objects.update_or_create(name="Ser Gouda", kcal=356, proteins=24.9, carbs=2.2, fats=27.5, grams=100)
    Food.objects.update_or_create(name="Chleb razowy (1 kromka ok. 30g)", kcal=217, proteins=6.7, carbs=43.7, fats=1.5, grams=100)
    Food.objects.update_or_create(name="Pomidor", kcal=20, proteins=1, carbs=3, fats=0.2, grams=100)
    Food.objects.update_or_create(name="Jajko (1 porcja ok. 68g)", kcal=139, proteins=12.5, carbs=0.6, fats=9.7, grams=100)
    Food.objects.update_or_create(name="Ziemniaki", kcal=80, proteins=2, carbs=16.8, fats=0.1, grams=100)
    Food.objects.update_or_create(name="Filet z kurczaka", kcal=99, proteins=21.5, carbs=0, fats=1.3, grams=100)
    Food.objects.update_or_create(name="Mięso mielone wieprzowe", kcal=100, proteins=21.3, carbs=0, fats=9.6, grams=100)
    Food.objects.update_or_create(name="Wołowina, polędwica", kcal=116, proteins=20, carbs=0, fats=4, grams=100)
    Food.objects.update_or_create(name="Makaron razowy, spaghetti", kcal=343, proteins=13, carbs=65, fats=1.9, grams=100)
    Food.objects.update_or_create(name="Banan", kcal=90, proteins=1, carbs=20.2, fats=0.3, grams=100)
    Food.objects.update_or_create(name="Jogurt naturalny", kcal=61, proteins=4.6, carbs=6.1, fats=2, grams=100)
    Food.objects.update_or_create(name="Orzechy włoskie", kcal=607, proteins=14.1, carbs=14.5, fats=65.3, grams=100)
    Food.objects.update_or_create(name="Ser mozarella", kcal=221, proteins=20.1, carbs=0.1, fats=15.6, grams=100)
    Food.objects.update_or_create(name="Grejpfrut", kcal=30, proteins=0.7, carbs=7.3, fats=0.1, grams=100)
    Food.objects.update_or_create(name="Mleko kokosowe Aroy-d (100ml)", kcal=181, proteins=1.6, carbs=1.95, fats=18.5, grams=100)
    Food.objects.update_or_create(name="Kasza jaglana", kcal=348, proteins=10.5, carbs=68.4, fats=2.9, grams=100)
    Food.objects.update_or_create(name="Filet z indyka", kcal=84, proteins=19, carbs=0, fats=1, grams=100)
    Food.objects.update_or_create(name="Avokado", kcal=160, proteins=2, carbs=8.5, fats=14.66, grams=100)
    Food.objects.update_or_create(name="Twaróg półtłusty", kcal=116, proteins=17, carbs=3.4, fats=4, grams=100)
    Food.objects.update_or_create(name="Pierś z makaronem razowym (1 porcja)", kcal=652, proteins=55, carbs=70, fats=12, grams=1)
    Food.objects.update_or_create(name="Olej kokosowy", kcal=830, proteins=0, carbs=0, fats=100, grams=100)
    Food.objects.update_or_create(name="Ryba dorada", kcal=100, proteins=20.5, carbs=0, fats=1.3, grams=100)
    Food.objects.update_or_create(name="Brokuły", kcal=30, proteins=2.8, carbs=4, fats=0.4, grams=100)
    Food.objects.update_or_create(name="Fasola biała", kcal=328, proteins=29.5, carbs=50, fats=1.3, grams=100)
    Food.objects.update_or_create(name="McRoyal podwójny pikanty (1 porcja)", kcal=765, proteins=52, carbs=36, fats=45, grams=1)
    Food.objects.update_or_create(name="Pringles Sour Cream & Onion", kcal=509, proteins=3.9, carbs=52, fats=32, grams=100)
    Food.objects.update_or_create(name="Masło orzechowe (orzeszki ziemne)", kcal=630, proteins=26, carbs=4, fats=54, grams=100)
    Food.objects.update_or_create(name="Masło klarowane", kcal=898, proteins=0.1, carbs=0.1, fats=99.8, grams=100)
    Food.objects.update_or_create(name="PowerPack: Pikantny kurczak (1 porcja)", kcal=685, proteins=57, carbs=72, fats=14, grams=1)
    Food.objects.update_or_create(name="Oliwa z oliwek", kcal=824, proteins=0, carbs=0, fats=91.6, grams=100)
    Food.objects.update_or_create(name="Szynka Parmeńska Prosciutto di Parma", kcal=273, proteins=27, carbs=0.7, fats=18.6, grams=100)
    Food.objects.update_or_create(name="Papryka", kcal=32, proteins=1.7, carbs=4, fats=0.5, grams=100)
    Food.objects.update_or_create(name="Ser Cheddar", kcal=379, proteins=25, carbs=0, fats=31, grams=100)

class Command(BaseCommand):
    help = 'Initialize database'

    def add_arguments(self, parser):
        parser.add_argument('--add-foods',
                            action='store_true',
                            dest='add-foods',
                            default=False,
                            help='Insert food data')
    

    def handle(self, *args, **options):
        start = timezone.now()

        update_all = not any([options['add-foods']])

        if options['add-foods'] or update_all:
            print("Loading foods...")
            populate()

        end = timezone.now()
        print(end - start)