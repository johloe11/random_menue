# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:04:15 2020

@author: John
"""

from numpy import random
import pandas as pd

class DinnerPlan():
    def __init__(self):
        self.dinners = []
        self.meals = {}

    def add_meal(self, dinner, recipe, cuisine_type, difficulty, meat):
        if dinner in self.dinners:
            print('The dinner listed is already in the database')
        else:
            if difficulty in ['easy', 'moderately easy', 'moderately hard', 'hard']:
                self.dinners.append(dinner)
                self.meals[dinner] = {'dinner': dinner, 'recipe':recipe, 'cuisine_type': cuisine_type, 'difficulty':difficulty, 'meat':meat}
                print(f'{dinner} added to the database.')
            else:
                print('Difficulty should be listed as easy, moderately easy, '
                      'moderately hard, or hard')
  
    def what_to_eat(self, cuisine_type=False, difficulty=False, meat=False):
        try:
            dic = {dinner: [self.meals[dinner]['cuisine_type'], self.meals[dinner]['difficulty'], self.meals[dinner]['meat']] for dinner in self.meals}
            if cuisine_type:  
                dic = {key: value for key, value in dic.items() if self.meals[key]['cuisine_type'] == cuisine_type}
            if difficulty:
                dic = {key: value for key, value in dic.items() if self.meals[key]['difficulty'] == difficulty}
            if meat:
                dic = {dinner: self.meals[dinner]['meat'] for dinner in self.meals if self.meals[dinner]['meat']==meat}                
            cat = [key for key in dic.keys()]
            choice = (random.choice(cat)) 
            meal = self.meals[choice]
            print(f"Your meal today is {choice} ({meal['recipe']}), which "
                     f"is {meal['cuisine_type']} and is {meal['difficulty']} to make")
            df = pd.DataFrame(meal, index=[0])
            return df
        except ValueError:
            print('Either, no dinners were entered or there are no meals in the '
                  'category you specified. Please enter more meals or change '
                  'your cuisine type specification and try again.')
    
    def week_menue(self):
        week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 
                'Thursday', 'Friday', 'Saturday']
        weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        days = []
        attempt = 0
        for day in week:
            length = len(days)
            while len(days) == length and attempt < 50:
                attempt += 1
                today = self.meals[str(random.choice(self.dinners))]
                meal_plan = [sublist.iloc[:,0].to_string().lstrip('0 ') for sublist in days]
                hard_count = [sublist.iloc[:,3].to_string().lstrip('0 ') for sublist in days].count('hard')
                moderately_hard_count = [sublist.iloc[:,3].to_string().lstrip('0 ') for sublist in days].count('moderately hard')
                if today['difficulty'] == 'hard':
                    hard_count = hard_count + 1
                if today['difficulty'] == 'moderately hard':
                    moderately_hard_count = moderately_hard_count + 1
                moderately_hard_count = moderately_hard_count + hard_count
                if day == 'Friday':
                    while today['meat'] or today['difficulty'] == 'hard':
                        today = self.meals[str(random.choice(self.dinners))]
                        attempt + 1
                if day in weekday:
                    while today['difficulty'] == 'hard':
                        today = self.meals[str(random.choice(self.dinners))] 
                        attempt + 1
                if today['dinner'] not in meal_plan and hard_count < 2 and moderately_hard_count < 4:
                    today['Day'] = day
                    df = pd.DataFrame(today, index=[0])
                    days.append(df)
        data = pd.concat(days).reset_index(drop = True)
        day = data['Day']
        data = data.drop(['Day'], axis=1)
        data.insert(0, 'Day', day)
        if attempt > 48:
            print('Oops! Something went wrong. Please re-run: week = dinner_list.week_menue()' 
                  ' If this problem persists, add more meatless, easy, and' 
                  ' moderately easy dishes.')
        return data
    
    def dissatisfied(self, df, days):
        data = df.copy()
        data['order'] = data.index+1
        meal_list = [meal for meal in data['dinner']]
        for day in days:
            data = data[data['Day'] != day]
            meal = self.what_to_eat()
            while str(meal['dinner']).lstrip('0 ').rstrip(' Name: dinner, dtype: object').strip() in meal_list:
                meal = self.what_to_eat()
            meal['Day'] = day
            meal['order'] = (data['order'].max()*((data['order'].max()+1)/2))-sum(data['order'])
            data = data.append(meal).reset_index(drop = True)
            meal_list = [meal for meal in data['dinner']]
        data = data.sort_values(by=['order'])
        data = data.drop(['order'], axis=1)
        return data
            

dinner_list = DinnerPlan()
dinner_list.add_meal('smoked turkey', 'https://heygrillhey.com/smoked-turkey/',
            'American', 'hard', 'yes')
dinner_list.add_meal('cullen skink', 'https://www.thespruceeats.com/traditional-scottish-cullen-skink-recipe-435379',
            'Scottish', 'hard', 'no')
dinner_list.add_meal('fish and chips', 'https://www.thespruceeats.com/best-fish-and-chips-recipe-434856',
            'Sea-food', 'moderately easy', 'no')
dinner_list.add_meal('tacos', 'https://www.thewholesomedish.com/the-best-homemade-tacos/',
            'Mexican', 'moderately hard', 'yes')
dinner_list.add_meal('shrimp alfredo', 'https://www.dinneratthezoo.com/shrimp-alfredo/',
            'Sea-food', 'moderately easy', 'no')
dinner_list.add_meal('smoked fish mac and cheese', 'https://chezlerevefrancais.com/smoked-salmon-mac-cheese/',
            'Italian', 'moderately easy', 'no')
dinner_list.add_meal('hamburgers', 'https://heygrillhey.com/smoked-hamburgers/',
            'American', 'moderately hard', 'yes')
dinner_list.add_meal('fish schnitzel', 'https://www.foodtolove.co.nz/recipes/lemon-and-chilli-fish-schnitzel-7978',
            'Sea-food', 'moderately easy', 'no')
dinner_list.add_meal('calzone', 'https://www.spendwithpennies.com/homemade-calzone/',
            'Italian', 'moderately hard', 'yes')
dinner_list.add_meal('Duck soup', 'https://www.food.com/recipe/duck-soup-60255', 
                     'Thai', 'moderately easy', 'Yes')
dinner_list.add_meal('Grilled cheese', 'https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/', 
                     'American', 'easy', 'No')
dinner_list.add_meal('chile relleno', 'https://www.isabeleats.com/chile-relleno-recipe/', 
                     'Mexican', 'moderately easy', 'no')

week = dinner_list.week_menue()

weeknew = dinner_list.dissatisfied(week, ['Monday', 'Tuesday', 'Wednesday'])

q = dinner_list.what_to_eat()

add_dinner = InteractiveDinnerPlan()
add_dinner.add_meal()    
           
class InteractiveDinnerPlan(DinnerPlan):
    def add_meal(self):
        while True:
            dinner = str(input('dinner: ')).strip()
            if len(dinner) < 1:
                print('Please enter a dinner')
                continue
            else:
                break
        while True:
            recipe = str(input('recipe: '))
            if recipe == 'nothing':
                print('What are you doing? Put something!')
                continue
            else:
                break
        while True:
            cuisine_type = str(input('cuisine_type: '))
            if cuisine_type == 'nothing':
                print('What are you doing? Put something!')
                continue
            else:
                break
        while True:
            difficulty = str(input('difficulty: ')).strip()
            if difficulty.strip() not in ['easy', 'moderately easy', 'moderately hard', 'hard']:
                print('Use only easy, moderately easy, moderately hard, or hard')
                continue
            else:
                break
        while True:
            meat = str(input('meat: '))
            if meat.strip().lower() not in ['yes', 'no']:
                print('Please answer with yes or no')
                continue
            else:
                break
        self.dinners.append(dinner)
        self.meals[dinner] = {'recipe':recipe, 'cuisine_type':cuisine_type, 
                              'difficulty':difficulty, 'meat':meat.lower()}
        print(f'To perminately add this to the code copy and past the following'
              f" into the code: dinner_list.add_meal('{dinner}', "
              f"'{recipe}', '{cuisine_type}', '{difficulty}', '{meat.lower()}')")
            

    