from django.contrib.auth import get_user_model
import random
import datetime
from django.core.management import BaseCommand
import warnings
from core.models import Tag, Ingredient, Recipe


def fxn():
    warnings.warn("NaiveTimeValue", RuntimeWarning)


class Command(BaseCommand):

    def handle(self, *args, **options):
        emails = []
        usernames = []
        passwords = []
        tags = ['fast', 'medium fast', 'medium slow', 'slow', 'easy', 'medium easy', 'medium hard', 'hard']
        ingredients = []
        urls = []

        with open('/app/core/management/commands/emails.txt', 'r') as emails_file:
            for line in emails_file:
                usernames.append(line.split('@')[0].replace('.', '_'))
                emails.append(line.strip())

        with open('/app/core/management/commands/passwords.txt', 'r') as passwords_file:
            for line in passwords_file:
                passwords.append(line.strip())

        with open('/app/core/management/commands/ingredients.txt', 'r') as ingredients_file:
            for line in ingredients_file:
                ingredients.append(line.strip())

        with open('/app/core/management/commands/urls.txt', 'r') as urls_file:
            for line in urls_file:
                urls.append(line.strip())

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fxn()

            print('[1/4] -- creating users')
            for each in range(len(usernames)):
                get_user_model().objects.create_user(
                    email=emails[each],
                    name=usernames[each],
                    password=passwords[each],
                    is_active=bool(random.getrandbits(1)),
                    is_staff=False,
                    last_login=datetime.datetime(year=random.randint(2010, 2023),
                                                 month=random.randint(1, 12),
                                                 day=random.randint(1, 28)),
                    is_superuser=False
                )
        print(get_user_model().objects.count(), 'users created.')

        print('[2/4] -- creating tags')
        for _ in range(len(usernames)):
            Tag.objects.create(name=random.choice(tags),
                               user=get_user_model().objects.filter(name=random.choice(usernames))[0])
        print(Tag.objects.count(), 'tags created.')

        print('[3/4] -- creating ingredients')
        for _ in range(len(usernames)):
            Ingredient.objects.create(name=random.choice(ingredients),
                                      user=get_user_model().objects.filter(name=random.choice(usernames))[0])
        print(Ingredient.objects.count(), 'ingredients created.')

        print('[4/4] -- creating recipes')
        count = 0
        for each in usernames:
            ingredient = random.choice(Ingredient.objects.all())
            tag = random.choice((Tag.objects.all()))
            many_ingredients = []
            random_range = random.randint(1, 5)
            random_numbers = random.sample(range(1, 1000), random_range)
            for _ in range(random_range):
                many_ingredients.append(Ingredient.objects.all()[random_numbers.pop()])

            if tag.name == 'fast':
                time = random.randint(5, 10)
            elif tag.name == 'medium fast':
                time = random.randint(11, 20)
            elif tag.name == 'medium slow':
                time = random.randint(21, 30)
            elif tag.name == 'slow':
                time = random.randint(31, 120)
            else:
                time = random.randint(10, 120)

            recipe = Recipe.objects.create(user=get_user_model().objects.all()[count],
                                           title=ingredient.name+' recipe',
                                           time_minutes=time,
                                           price=random.randint(20, 150),
                                           link=random.choice(urls))
            for ingredient in many_ingredients:
                recipe.ingredients.add(ingredient)
            recipe.tags.add(tag)
            recipe.save()
            count += 1
        print(Recipe.objects.count(), 'recipes created.')
        print('Done!')
