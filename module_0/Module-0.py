#!/usr/bin/env python
# coding: utf-8

# In[156]:


import numpy as np


# In[157]:


def score_game(game_core):
    count_ls = []
    np.random.seed(1)
    random_array = np.random.randint(1,101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)


# In[158]:


def game_core_v3(number):
    count = 1
    # Выбираем число 50, для уменьшения диапозона поиска вдвое
    predict = 50
    while number != predict:
        count+=1
        # Первый шаг, положительная ветка
        if number > predict:
            predict = 75
            
            # Второй шаг положительная ветка
            while number != predict:
                count+=1
                #Второй шаг(+), верхняя развилка
                if number > predict:
                    predict = 87
                    #Финальный перебор
                    while number != predict:
                        count+=1
                        if number > predict:
                            predict += 1
                        elif number < predict:
                            predict -= 1
                #Второй шаг(+), нижняя развилка
                elif number < predict:
                    predict = 63
                    #Финальный перебор
                    while number != predict:
                        count+=1
                        if number > predict:
                            predict += 1
                        elif number < predict:
                            predict -= 1
        
        # Первый шаг, отрицательная ветка
        elif number < predict:
            predict = 25
            
            # Второй шаг отрицательная ветка
            while number != predict:
                count+=1
                #Второй шаг(-), верхняя развилка
                if number > predict:
                    predict = 37
                    #Финальный перебор
                    while number != predict:
                        count+=1
                        if number > predict:
                            predict += 1
                        elif number < predict:
                            predict -= 1
                #Второй шаг(-), нижняя развилка
                if number < predict:
                    predict = 13
                    #Финальный перебор
                    while number != predict:
                        count+=1
                        if number > predict:
                            predict += 1
                        elif number < predict:
                            predict -= 1
           
    
    return(count) # выход из цикла, если угадали


# In[159]:


score_game(game_core_v3)

