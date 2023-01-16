#Задание 0
import csv
import pandas as pd
from typing import List

def time_minutes(row: str) -> int:
  ''' Функция для перевода времени 
      из типа данных str в виде ___hrs___mins 
      к типу данных int в минутах 
      ('5 hrs 35 mins' -> 335)
      При передаче NaN возвращает 0'''
      
  if row == 'nan':
      return 0
  time_list: List[str] = row.split()
  total_time: int = 0
  if 'hrs' in time_list:
      hours = int(time_list[0])
      total_time = hours * 60
  if 'mins' in time_list:
      mins_ind = time_list.index('mins')
      minutes = int(time_list[mins_ind - 1])
      total_time += minutes
  return total_time


with open('recipes_100.csv') as f:
      reader = csv.reader(f)

      row = next(reader)
      time_ind = row.index('total_time')

      for row in reader:
          time = time_minutes(row[time_ind])

#Asserts
assert time_minutes('NaN') == 0
assert time_minutes('nan') == 0
assert time_minutes('') == 0
assert time_minutes('   ') == 0
assert time_minutes('0 mins') == 0
assert time_minutes('0 hrs') == 0
assert time_minutes('35 mins') == 35
assert time_minutes('0 hrs 35 mins') == 35
assert time_minutes('5 hrs 35 mins') == 335
assert time_minutes('5 hrs') == 300

#Задание 1
# Все рецепты, в которых используется курица

def find_recipe(ingredient: str) -> set:
    '''Функция для поиска рецептов, в которые входит переданный 
ингридиент'''
    global row, ingredients_ind, recipe_name_ind
    all_ingredient_recipes = set()
    for row in reader:
        if ingredient in row[ingredients_ind]:
           all_ingredient_recipes.add(row[recipe_name_ind])
    return all_ingredient_recipes


with open('recipes_100.csv') as f:
     reader = csv.reader(f)

     row = next(reader)
     ingredients_ind = row.index('ingredients')
     recipe_name_ind = row.index('recipe_name')

     recipes = find_recipe('chicken')

     print('Все рецепты, в которых используется курица:', *recipes, 
sep='\n', end='\n\n')


# Три самых долгих для приготовления рецепта
df = pd.read_csv('recipes_100.csv')
new_df = df[['recipe_name', 'total_time']].copy()

for i in range (len(new_df)):
    new_df.loc[i, 'total_time'] = time_minutes(str(new_df.loc[i, 
'total_time']))
                                # функция time_minutes в задании 0

sorted_df = new_df.sort_values('total_time', ascending=False)
maxtime_dishes = new_df.loc[sorted_df[:3].index, 'recipe_name']
print('Три самых долгих для приготовления рецепта:',
      '1)на основе исходного датасета:', 
      *maxtime_dishes, sep='\n', end='\n\n')

# Вариант без повторений
without_repeat_df = 
sorted_df.copy().drop_duplicates(subset=['recipe_name'])
maxtime_dishes_2 = new_df.loc[without_repeat_df[:3].index, 'recipe_name']
print('2)если без повторений:', *maxtime_dishes_2, sep = '\n', end='\n\n')


# На каждое количество человек названия блюд, которые можно приготовить

def serv_dishes(serv: int) -> set:
    '''Функция выводит названия блюд, 
       которые можно приготовить для переданного количества человек '''
    global df
    dishes = df[(df.servings == serv)]['recipe_name']
    return set(dishes)


df = pd.read_csv('recipes_100.csv')
max_serv = df['servings'].max()
min_serv = df['servings'].min()
serv_dict = {}

for i in range(min_serv, max_serv + 1):
    dishes = serv_dishes(i)
    if dishes:
       serv_dict[i] = [*dishes]
       print('На', i, 'человек можно приготовить следующие блюда:')
       print(*dishes, sep='\n', end='\n\n')


# Сохранение всех ответов в JSON файл

import json


answers_dict = {
    'All recipes that use chicken:': list(recipes),
    'The three longest dishes to cook:': 
              {
               '1)based on the original dataset:': list(maxtime_dishes),
               '2)if there are no repetitions:': list(maxtime_dishes_2)
              },
    'For each number of people, the names of dishes that can be 
prepared:': serv_dict
               }

with open("task1.json", "w") as json_file:
     json.dump(answers_dict, json_file, indent=3)

# Задание 2
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv('recipes_100.csv')

df['rating'].plot(kind='hist',
                  alpha=0.7, 
                  bins=15,
                  title='Гистограмма оценок блюд ',
                  grid=True,
                  facecolor='green',
                  edgecolor='black')
plt.xlabel('Рейтинг')
plt.ylabel('Частота встречаемости')
plt.savefig('task2.png')
plt.show()
