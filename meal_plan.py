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

    def add_meal(self, dinner, recipe, cuisine_type, difficulty, 
                 prep_time, cook_time, meat, healthy):
        if dinner in self.dinners:
            print('The dinner listed is already in the database')
        else:
            if difficulty in ['easy', 'moderately easy', 'moderately hard', 'hard']\
                and meat in ['yes', 'no'] and str(cook_time).isnumeric()==True\
                and str(prep_time).isnumeric()==True and healthy in ['yes', 'no']:
                self.dinners.append(dinner)
                total_time = prep_time+cook_time
                self.meals[dinner] = {'dinner': dinner, 'recipe':recipe, 
                                      'cuisine_type': cuisine_type, 
                                      'difficulty':difficulty,
                                      'prep time': f'{prep_time} minutes',                                      
                                      'cook time': f'{cook_time} minutes',
                                      'total time': f'{total_time} minutes',
                                      'meat':meat, 'healthy': healthy}
                print(f'{dinner} added to the database.')
            else:
                print('Difficulty should be listed as easy, moderately easy, '
                      'moderately hard, or hard, meat and healthy should be either yes or no, '
                      'prep_time and cook_time should be a number (not spelled out)')
  
    def what_to_eat(self, cuisine_type=False, difficulty=False, prep_time=False, 
                    cook_time=False, total_time=False, meat=False, healthy=False,
                    printing=True):
        try:
            dic = {dinner: [self.meals[dinner]['cuisine_type'], 
                            self.meals[dinner]['difficulty'], 
                            self.meals[dinner]['prep time'], 
                            self.meals[dinner]['cook time'],
                            self.meals[dinner]['total time'], 
                            self.meals[dinner]['meat'],
                            self.meals[dinner]['healthy']] for dinner in self.meals}
            if cuisine_type:  
                dic = {key: value for key, value in dic.items() if self.meals[key]['cuisine_type'].lower() == cuisine_type.lower()}
            if difficulty:
                dic = {key: value for key, value in dic.items() if self.meals[key]['difficulty'] == difficulty}
            if prep_time:
                dic = {key: value for key, value in dic.items() if int(self.meals[key]['prep time'].rstrip(' minutes')) <= prep_time}
            if cook_time:
                dic = {key: value for key, value in dic.items() if int(self.meals[key]['cook time'].rstrip(' minutes')) <= cook_time}
            if total_time:
                dic = {key: value for key, value in dic.items() if int(self.meals[key]['total time'].rstrip(' minutes')) <= total_time}            
            if meat:
                dic = {key: value for key, value in dic.items() if self.meals[key]['meat'] == meat}            
            if healthy:
                dic = {key: value for key, value in dic.items() if self.meals[key]['healthy'] == healthy}
            cat = [key for key in dic.keys()]
            choice = (random.choice(cat)) 
            meal = self.meals[choice]
            if printing:
                print(f"Your meal today is {choice} ({meal['recipe']}), which "
                      f"is {meal['cuisine_type']} and is {meal['difficulty']} to make. "
                      f"The total cook time is {meal['total time']}")
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
                    while today['meat'] == 'yes' or today['difficulty'] == 'hard':
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
            print('Oops! Something went wrong! Please re-run: week = dinner_list.week_menue()' 
                  ' If this problem persists, add more meatless, easy, and' 
                  ' moderately easy dishes.')
        return data

    def dissatisfied(self, df, days, cuisine_types=[False,False,False,False,False,False,False], 
                     difficulties=[False,False,False,False,False,False,False], 
                     prep_times=[False,False,False,False,False,False,False],
                     cook_times=[False,False,False,False,False,False,False], 
                     total_times=[False,False,False,False,False,False,False], 
                     meats=[False,False,False,False,False,False,False], 
                     healths=[False,False,False,False,False,False,False]):
        data = df.copy()
        attempt = 0
        data['order'] = data.index+1
        meal_list = [meal for meal in data['dinner']]
        for day, cuisine_type, difficulty, prep_time, cook_time, total_time, meat, health in zip(
                days, cuisine_types, difficulties, prep_times, cook_times, 
                total_times, meats, healths):
            data = data[data['Day'] != day]
            meal = self.what_to_eat(cuisine_type=cuisine_type, difficulty=difficulty, 
                                    prep_time=prep_time, cook_time=cook_time, 
                                    total_time=total_time, meat=meat, 
                                    healthy=health, printing=False)
            while str(meal['dinner']).lstrip('0 ').rstrip(' Name: dinner, dtype: object').strip() in meal_list\
                and attempt<21:
                meal = self.what_to_eat(cuisine_type=cuisine_type, difficulty=difficulty, 
                                    prep_time=prep_time, cook_time=cook_time, 
                                    total_time=total_time, meat=meat, 
                                    healthy=health, printing=False)
                if attempt==20:
                    print("Oops! Something went wrong! There probably aren't "
                          "any meals not already in week that meet your specifications. "
                          "You can either rerun week, change the specifications, "
                          "or add more meals with that specification and rerun "
                          'the code.')
                attempt += 1
            meal['Day'] = day
            meal['order'] = (data['order'].max()*((data['order'].max()+1)/2))-sum(data['order'])
            data = data.append(meal).reset_index(drop = True)
            meal_list = [meal for meal in data['dinner']]
        data = data.sort_values(by=['order']).reset_index(drop = True)
        data = data.drop(['order'], axis=1)
        return data
      
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
            difficulty = str(input('difficulty: ')).lower()
            if difficulty.lower() not in ['easy', 'moderately easy', 'moderately hard', 'hard']:
                print('Use only easy, moderately easy, moderately hard, or hard')
                continue
            else:
                break
        while True:
            prep_time = input('prep time: ')
            if str(prep_time).isnumeric()==False:
                print('Enter a number that represents the amount of preperation '
                      'time the meal takes in minutes. (enter only the number)')
                continue
            else:
                break
        while True:
            cook_time = input('cook time: ')
            if str(cook_time).isnumeric()==False:
                print('Enter a number that represents the amount of cook '
                      'time the meal takes in minutes. (enter only the number)')
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
        while True:
            healthy = str(input('healthy: '))
            if healthy.strip().lower() not in ['yes', 'no']:
                print('Please answer with yes or no')
                continue
            else:
                break
        total_time = cook_time+prep_time
        self.dinners.append(dinner)
        self.meals[dinner] = {'recipe':recipe, 'cuisine_type':cuisine_type, 
                              'difficulty':difficulty, 'prep time':prep_time, 
                              'cook time':cook_time, 'total time':total_time, 
                              'meat':meat.lower(), 'healthy':healthy.lower()}
        print(f'To perminately add this to the code copy and past the following'
              f" into the code: dinner_list.add_meal('{dinner}', "
              f"'{recipe}', '{cuisine_type}', '{difficulty}', {int(prep_time)}, "
              f"{int(cook_time)}, '{meat.lower()}', '{healthy.lower()}')")


dinner_list = DinnerPlan()
dinner_list.add_meal('smoked turkey', 'https://heygrillhey.com/smoked-turkey/',
            'American', 'hard', 15, 420, 'yes', 'yes')
dinner_list.add_meal('cullen skink', 'https://www.thespruceeats.com/traditional-scottish-cullen-skink-recipe-435379',
            'Scottish', 'hard', 40, 240, 'no', 'yes')
dinner_list.add_meal('fish and chips', 'https://www.thespruceeats.com/best-fish-and-chips-recipe-434856',
            'Sea-food', 'moderately easy', 20, 25, 'no', 'no')
dinner_list.add_meal('tacos', 'https://www.thewholesomedish.com/the-best-homemade-tacos/',
            'Mexican', 'moderately hard', 5, 15, 'yes', 'no')
dinner_list.add_meal('shrimp alfredo', 'https://www.dinneratthezoo.com/shrimp-alfredo/',
            'Sea-food', 'moderately easy', 10, 35, 'no', 'yes')
dinner_list.add_meal('smoked fish mac and cheese', 'https://chezlerevefrancais.com/smoked-salmon-mac-cheese/',
            'Italian', 'moderately easy', 20, 300, 'no', 'no')
dinner_list.add_meal('hamburgers', 'https://heygrillhey.com/smoked-hamburgers/',
            'American', 'moderately hard', 5, 45, 'yes', 'no')
dinner_list.add_meal('fish schnitzel', 'https://www.foodtolove.co.nz/recipes/lemon-and-chilli-fish-schnitzel-7978',
            'Sea-food', 'moderately easy', 10, 25, 'no', 'yes')
dinner_list.add_meal('calzone', 'https://www.spendwithpennies.com/homemade-calzone/',
            'Italian', 'moderately hard', 20, 30, 'yes', 'no')
dinner_list.add_meal('Duck soup', 'https://www.food.com/recipe/duck-soup-60255', 
                     'Thai', 'moderately easy', 10, 45, 'yes', 'yes')
dinner_list.add_meal('Grilled cheese', 'https://www.allrecipes.com/recipe/23891/grilled-cheese-sandwich/', 
                     'American', 'easy', 5, 10, 'no', 'yes')
dinner_list.add_meal('chile relleno', 'https://www.isabeleats.com/chile-relleno-recipe/', 
                     'Mexican', 'moderately easy', 15, 30, 'no', 'yes')
dinner_list.add_meal('Salmon, spinich, and quina', 'Sam has it',
                     'French', 'easy', 5, 20, 'no', 'yes')
dinner_list.add_meal('cereal', 'in the dome piece', 'American', 'easy', 2, 0, 'no', 'yes')


'''
This will give you a random meal for the day.
You can put the following conditions on it: cuisine_type, difficulty, prep_time,
cook_time, total_time, meat, or healthy in the style below. 
For difficulty, choices are easy, moderatly easy, moderately hard, or hard
For prep_time, cook_time, and total_time, put the maximum number (as an intiger)
you want in minutes
For meat and healthy put only yes or no
'''
today = dinner_list.what_to_eat(healthy='yes', total_time=60)


'''This will give you a week of meals, no more than three moderately hard or hard
dishes, no meat on Friday, and no repeat meals.'''
week = dinner_list.week_menue()

'''This will allow you to switch out any number of days or create a meal plan with
more specifications.

If you want to put conditions on the new meals you can specify cuisine_types,
difficulties, prep_times, cook_times, total_times, meats, and healths
in the way below, follwoing the guide set forth in the comment above today = ...'''
weeknew = dinner_list.dissatisfied(week, ['Monday', 'Tuesday', 'Wednesday'], 
                                   cuisine_types=['Sea-food', 'Scottish', 'American'])


'''Run the following if you want to add a meal to the database, it will give you
the code to copy and past to the block of code above. After adding the recipe re-run
the code starting with dinner_list = DinnerPlan()'''
add_dinner = InteractiveDinnerPlan()
add_dinner.add_meal()    
           

            

    