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
  
    def what_to_eat(self, cuisine_type = 'everything'):
        try:
            if cuisine_type == 'everything':
               choice = random.choice(self.dinners)
               meal = self.meals[choice]
               print(f"Your meal today is {choice} ({meal['recipe']}), which "
                     f"is {meal['cuisine_type']} which is {meal['difficulty']} to make")
            else:  
                dic = {dinner: self.meals[dinner]['cuisine_type'] for dinner in self.meals if self.meals[dinner]['cuisine_type']==cuisine_type}
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
        for day in week:
            length = len(days)
            while len(days) == length:
                today = self.meals[str(random.choice(self.dinners))]
                meal_plan = [sublist.iloc[:,0].to_string().lstrip('0 ') for sublist in days]
                hard_count = [sublist.iloc[:,3].to_string().lstrip('0 ') for sublist in days].count('hard')
                moderately_hard_count = [sublist.iloc[:,3].to_string().lstrip('0 ') for sublist in days].count('moderately hard') + hard_count            
                if today['difficulty'] == 'hard':
                    hard_count = hard_count + 1
                if day == 'Friday':
                    while today['meat']:
                        today = self.meals[str(random.choice(self.dinners))]
                if day in weekday:
                    while today['difficulty'] == 'hard':
                        today = self.meals[str(random.choice(self.dinners))] 
                if today['dinner'] not in meal_plan and hard_count < 2 and moderately_hard_count < 4:
                    today['Day'] = day
                    df = pd.DataFrame(today, index=[0])
                    days.append(df)
        data = pd.concat(days).reset_index(drop = True)
        day = data['Day']
        data = data.drop(['Day'], axis=1)
        data.insert(0, 'Day', day)
        return data
    
    def dissatisfied(self, df, days):
        data = df.copy()
        data['order'] = data.index+1
        for day in days:
            data = data[data['Day'] != day]
            meal = self.what_to_eat()
            meal['Day'] = day
            meal['order'] = (data['order'].max()*((data['order'].max()+1)/2))-sum(data['order'])
            data = data.append(meal).reset_index(drop = True)
        data = data.sort_values(by=['order'])
        data = data.drop(['order'], axis=1)
        return data
            

dinner_list = DinnerPlan()
dinner_list.add_meal('smoked turkey', 'https://heygrillhey.com/smoked-turkey/',
            'American', 'hard', True)
dinner_list.add_meal('cullen skink', 'https://www.thespruceeats.com/traditional-scottish-cullen-skink-recipe-435379',
            'Scottish', 'hard', False)
dinner_list.add_meal('fish and chips', 'https://www.thespruceeats.com/best-fish-and-chips-recipe-434856',
            'Sea-food', 'moderately easy', False)
dinner_list.add_meal('tacos', 'https://www.thewholesomedish.com/the-best-homemade-tacos/',
            'Mexican', 'easy', True)
dinner_list.add_meal('shrimp alfredo', 'https://www.dinneratthezoo.com/shrimp-alfredo/',
            'Sea-food', 'moderately easy', False)
dinner_list.add_meal('smoked fish mac and cheese', 'https://chezlerevefrancais.com/smoked-salmon-mac-cheese/',
            'Italian', 'moderately easy', False)
dinner_list.add_meal('hamburgers', 'https://heygrillhey.com/smoked-hamburgers/',
            'American', 'easy', True)
dinner_list.add_meal('fish schnitzel', 'https://www.foodtolove.co.nz/recipes/lemon-and-chilli-fish-schnitzel-7978',
            'Sea-food', 'moderately easy', False)
dinner_list.add_meal('calzone', 'https://www.spendwithpennies.com/homemade-calzone/',
            'Italian', 'moderately hard', True)

week = dinner_list.week_menue()

weeknew = dinner_list.dissatisfied(week, ['Monday', 'Tuesday'])

q = dinner_list.what_to_eat()

db = MovieDataBase()
db.add_movie('movie 1', 2232, 'action', 98)
db.add_movie('movie 2', 2232, 'action', 90)
db.add_movie('movie 3', 2232, 'comedy', 9)
db.add_movie('movie 4', 2232, 'drama', 8)
db.what_to_watch()
    
           
class InteractiveMovieDataBase(MovieDataBase):
    def add_movie(self):
        while True:
            title = str(input('title: ')).strip()
            if len(title) < 1:
                print('Please enter a title')
                continue
            else:
                break
        while True:
            try:
                year = int(input('year: '))
            except ValueError:
                print('Please only use numbers')
                continue
            if year < 1887:
                print('No films were made before 1887. Please enter a valid year.')
                continue
            elif year > 2020:
                print("The year you have entered has not occured yet, please enter a year 2020 or earlier.")
            else:
                break
        while True:
            category = str(input('category: ')).strip()
            if category.replace(" ","").replace("&","").replace("-","").replace("(","").replace(")","").replace("'","").isalpha()==False:
                print("Please enter a category that uses only the following symbols: letters, &, -, (), or '.")
                continue
            else:
                break
        while True:
            try:
                rating = int(input('rating: '))
            except ValueError:
                print('Please use only numbers')
                continue
            if rating < 0 or rating > 100:
                print('Please only use numbers between 0 and 100')
                continue
            else:
                break
        self.titles.append(title)
        self.movies[title] = {'year':int(year), 'category':category, 'rating':rating}
        print('{} ({}) added to the database.'.format(title,year))
            

    
    def movie_rankings(self):
        dicti = {title: self.movies[title]['rating'] for title in self.movies}
        new = {title: rating for title, rating in sorted(dicti.items(), key=lambda rate: -rate[1])}
        print (new)
        cate = [key for key in new.keys()]
        return cate  
