#!/usr/bin/env python
# coding: utf-8

# # Основные цели и задачи проекта.
# 

# Основные цели EDA:
# 
# 1. Сформулировать предположения и гипотезы для дальнейшего построения модели.
# 2. Проверить качество данных и очистить их, если это необходимо.
# 3. Определиться с параметрами модели.

# Суть проекта — отследить влияние условий жизни учащихся в возрасте от 15 до 22 лет на их успеваемость по математике, чтобы на ранней стадии выявлять студентов, находящихся в группе риска.
# 
# Задача - с помощью разведывательного анализа данных определить параметры модели, которая предсказывала бы результаты госэкзамена по математике для каждого ученика школы.

# Основные этапы:
# 
# 1. Первычный осмотр данных.
# 2. Проверка на наличие пустых значений.
# 3. Проверить данные на дубли, а так же на полностью скоррелированные значения.
# 4. Проверить данные на наличие выбросов.
# 5. Отобрать данные, пригодные для дальнейшего построения модели.

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import ttest_ind

pd.set_option('display.max_rows', 50) # показывать больше строк
pd.set_option('display.max_columns', 50) # показывать больше колонок

stud_math = pd.read_csv('D:\PD/stud_math.xls')


# Предобработка.
# Все функции используемые в работе

# In[2]:


def outliers (x):
    
    median = x.median()
    IQR = x.quantile(0.75) - x.quantile(0.25)
    perc25 = x.quantile(0.25)
    perc75 = x.quantile(0.75)
    print('25-й перцентиль: {},'.format(perc25), '75-й перцентиль: {},'.format(perc75), "IQR: {}, ".format(IQR),"Границы выбросов: [{f}, {l}].".format(f = perc25 - 1.5*IQR, l = perc75 + 1.5 * IQR))
    x.loc[x.between(perc25 - 1.5 * IQR, perc75 + 1.5 * IQR)].hist(bins = 15, range = (10, 30),label = 'IQR')
    
    plt.legend();
#    
def outliers_two (x):
    
    median = x.median()
    IQR = x.quantile(0.75) - x.quantile(0.25)
    perc25 = x.quantile(0.25)
    perc75 = x.quantile(0.75)
    print('25-й перцентиль: {},'.format(perc25), '75-й перцентиль: {},'.format(perc75), "IQR: {}, ".format(IQR),"Границы выбросов: [{f}, {l}].".format(f = perc25 - 1.5*IQR, l = perc75 + 1.5 * IQR))
    x.loc[x.between(perc25 - 1.5 * IQR, perc75 + 1.5 * IQR)].hist(bins = 15, range = (0, 10),label = 'IQR')
   
    plt.legend();
#
    
def outliers_three (x):
    
    median = x.median()
    IQR = x.quantile(0.75) - x.quantile(0.25)
    perc25 = x.quantile(0.25)
    perc75 = x.quantile(0.75)
    print('25-й перцентиль: {},'.format(perc25), '75-й перцентиль: {},'.format(perc75), "IQR: {}, ".format(IQR),"Границы выбросов: [{f}, {l}].".format(f = perc25 - 1.5*IQR, l = perc75 + 1.5 * IQR))
    x.loc[x.between(perc25 - 1.5 * IQR, perc75 + 1.5 * IQR)].hist(bins = 15, range = (0, 100),label = 'IQR')
    
    x.loc[x <= 100].hist(alpha = 0.5, bins = 15, range = (0, 100), label = 'Здравый смысл')
    plt.legend();
#
    
def uniq_values (y):
    display(pd.DataFrame(y.value_counts()))
    print("Значений, встретившихся в столбце более 10 раз:", (y.value_counts()>10).sum())
    print("Уникальных значений:", y.nunique())
#
    
def del_nan (x):

    x = x.apply(lambda x: None if pd.isnull(x) else None if x == 'NaN' 
                      else x)
#
    
def get_boxplot(column):
    fig, ax = plt.subplots(figsize = (14, 4))
    sns.boxplot(x = column, y = 'score', 
                data = stud_math.loc[stud_math.loc[:, column].isin(stud_math.loc[:, column].value_counts().index[:5])],
               ax = ax)
    plt.xticks(rotation = 45)
    ax.set_title('Boxplot for ' + column)
    plt.show()
#
    
def get_stat_dif(column):
    cols = stud_math.loc[:, column].value_counts().index[:10]
    combinations_all = list(combinations(cols, 2))
    for comb in combinations_all:
        if ttest_ind(stud_math.loc[stud_math.loc[:, column] == comb[0], 'score'], 
                        stud_math.loc[stud_math.loc[:, column] == comb[1], 'score']).pvalue \
            <= 0.05 / len(combinations_all): # Учли поправку Бонферони
            print('Найдены статистически значимые различия для колонки', column)
            break


# Для начала рассмотрим имеющиеся у нас данные

# In[3]:


display(stud_math.head(10))
stud_math.info()


# Для удобста дальнейшей работы переименуем названия столбцов

# In[4]:


stud_math.rename(columns = {'Pstatus':'pstatus', 'Medu':'medu', 'Fedu':'fedu', 'Mjob':'mjob','Fjob':'fjob', 'studytime, granular':'studytime_granular'}, inplace = True)


# Столбец "studytime, granular" необходимо убрать

# In[5]:


stud_math.drop('studytime_granular', axis = 1, inplace = True)


# Исходя из описания столбцов можно сделать вывод, что всего восемь столбцов - age, failures, absences, score, medu,fedu, studytime, goout.
# Остальные - так или иначе номинативные, так как представляют собой либо строковые величины, либо числовые категории, не представляющие собой интереса как числа.
# 
# 

# ### Распределение по возрасту

# "Выбросы" из распределения по возрасту извлекаться не будут, так как это отдельная категория учеников
# которые могут стать источником получения дополнительной полезной информации, а не случайное отклонившееся наблюдение.

# ## Распределение по образованию матери

# In[6]:


stud_math.medu.hist()
stud_math.medu.describe()


# ## Распределение по образованию отца

# In[7]:


stud_math.fedu.hist()
stud_math.fedu.describe()


# В распределении образования отца, мы можем наблюдать выброс, равный 40.0
# Вероятнее всего, это вызванно опечаткой, при наборе 4.0

# In[8]:


stud_math[stud_math['fedu'] == 40]


# Исправим эту ошибку

# In[9]:


stud_math.fedu.loc[11] = 4.0


# ## Распределение по времени в пути до школы

# In[10]:


stud_math.traveltime.hist()
stud_math.traveltime.describe()


# ## Распределение по времени на учёбу помимо школы в неделю

# In[11]:


stud_math.studytime.hist()
stud_math.studytime.describe()


# ## Распределение по количеству внеучебных неудач

# In[12]:


stud_math.failures.hist()
stud_math.failures.describe()


# ## Распределение по семейным отношениям

# In[13]:


stud_math.famrel.hist()
stud_math.famrel.describe()


# Вызывают вопросы значение -1. Предположим, что это ошибка ввода значения 1

# In[14]:


stud_math[stud_math['famrel'] == -1]


# In[15]:


stud_math.famrel.loc[25] = 1.0


# ## Распределение по свободному времени после школы

# In[16]:


stud_math.freetime.hist()
stud_math.freetime.describe()


# ## Распределение по проведенному времени с друзьями

# In[17]:


stud_math.goout.hist()
stud_math.goout.describe()


# ## Распределение по текущему состоянию здоровья

# In[18]:


stud_math.health.hist()
stud_math.health.describe()


# ## Распределение по количеству пропущенных занятий

# In[19]:


stud_math.absences.hist()
stud_math.absences.describe()


# ## Распределение по баллам за госэкзамен по математике

# In[20]:


stud_math.score.hist()
stud_math.score.describe()


# # Перейдем к рассмотрению числовых переменных и устранению выбросов.

# In[21]:


#Далее перейдем к рассмотрению тех количественных переменных, 
#которые могут содержать выбросы исходя из просмотра гистограмм распределения признака:

outliers(stud_math.age)


# In[22]:


outliers_two(stud_math.failures)


# In[23]:


outliers_two(stud_math.medu)


# In[24]:


outliers_two(stud_math.fedu)


# In[25]:


outliers_two(stud_math.studytime)


# In[26]:


outliers_two(stud_math.goout)


# In[27]:


outliers_two(stud_math.absences)


# Распределения баллов за госэкзамен проваерим на "здравый смысл"

# In[28]:


outliers_three(stud_math.score)


# # Проверка номинативных переменных на предмет уникальных значений, а так же заменим пропущенные значения.

# In[29]:


del_nan(stud_math.school)
uniq_values(stud_math.school)


# In[30]:


del_nan(stud_math.sex)
uniq_values(stud_math.sex)


# In[31]:


del_nan(stud_math.address)
uniq_values(stud_math.address)


# In[32]:


del_nan(stud_math.famsize)
uniq_values(stud_math.famsize)


# In[33]:


del_nan(stud_math.mjob)
uniq_values(stud_math.mjob)


# In[34]:


del_nan(stud_math.fjob)
uniq_values(stud_math.fjob)


# In[35]:


del_nan(stud_math.guardian)
uniq_values(stud_math.guardian)


# In[36]:


del_nan(stud_math.traveltime)
uniq_values(stud_math.traveltime)


# In[37]:


del_nan(stud_math.schoolsup)
uniq_values(stud_math.schoolsup)


# In[38]:


del_nan(stud_math.famsup)
uniq_values(stud_math.famsup)


# In[39]:


del_nan(stud_math.paid)
uniq_values(stud_math.paid)


# In[40]:


del_nan(stud_math.activities)
uniq_values(stud_math.activities)


# In[41]:


del_nan(stud_math.nursery)
uniq_values(stud_math.nursery)


# In[42]:


del_nan(stud_math.higher)
uniq_values(stud_math.higher)


# In[43]:


del_nan(stud_math.romantic)
uniq_values(stud_math.romantic)


# In[44]:


del_nan(stud_math.internet)
uniq_values(stud_math.internet)


# In[45]:


del_nan(stud_math.famrel)
uniq_values(stud_math.famrel)


# In[46]:


del_nan(stud_math.freetime)
uniq_values(stud_math.freetime)


# In[47]:


del_nan(stud_math.health)
uniq_values(stud_math.health)


# In[48]:


del_nan(stud_math.reason)
uniq_values(stud_math.reason)


# In[49]:


del_nan(stud_math.pstatus)
uniq_values(stud_math.pstatus)


# # Проведем корреляционный анализ и выясним, какие переменные коррелируют с итоговой оценкой по госэкзамену по математике.

# Применим матрицу корреляции только для числовых переменных

# In[50]:


#Применим матрицу корреляции только для числовых переменных:

stud_math.corr().loc[['age', 'failures', 'absences','medu','fedu','goout', 'studytime', 'goout', 'score']][['age', 'failures', 'absences','medu','fedu','goout', 'studytime', 'goout', 'score']]


# По результатам мы видим, что наиболее скоррелированы с колонкой score все столбцы, кроме absences.
# Особенно сильная корреляция с колонками - failures, medu, age, fedu, goout - коэффициент более 0.1 по модулю. Их предполагается использовать для будущей модели.
# 
# Наименее скоррелирован столбец absences.

# In[51]:


#Избавимся от него.

stud_math.drop('absences', axis = 1, inplace = True) #Избавляемся от слабоскоррелированного числового столбца.


# # Проанализируем номинативные переменные и устраним те, которые не влияют на колонку score.

# In[52]:


for col in ['school', 'sex', 'address', 'famsize', 'fjob','mjob','guardian','schoolsup','famsup','pstatus','reason','health','freetime','famrel','higher','internet','romantic']:
    get_boxplot(col)


# Исходя из графиков видно, что влиять на результат по госэкзамену могут следующие категориальные переменные - mjob, schoolsup, health, freetime, higher.

# # Проверим статистическую разницу в распределении оценок по номинативным признакам с помощью теста Стьюдента.

# In[53]:


for col in ['school', 'sex', 'address', 'famsize', 'fjob', 'mjob', 'guardian', 'schoolsup', 'famsup', 'pstatus', 'reason', 'health', 'freetime', 'famrel', 'higher', 'internet', 'romantic']:
    get_stat_dif(col)


# В соответствии с тестом Стьюдента статическую значимость для дальнейшего построения модели имеет только столбец с работой матери.

# In[54]:


#Избавимся от остальных номинавтивных столбцов.

stud_math.drop(['school', 'sex', 'address', 'famsize', 'fjob', 'guardian', 'schoolsup', 'famsup', 'pstatus', 'reason', 'health', 'freetime', 'famrel', 'higher', 'internet', 'romantic'], axis = 1, inplace = True)


# # Ниже представлены оставшиеся данные.

# In[55]:


stud_math.head()


# # Выводы
# 
# - Практически столбцы, кроме age, sex и school, имеются пустыв значения, которые были заменены на NaN;
# - Столбец studytime, granular был практически сразу исключен, так как не содержался в описании к датафрейму;
# - Столбцы fedu и famrel содержали ошибки. Эти ошибки были отнесены к некачественному сбору данных и заменены на имевшиеся в виду корректные данные. 
# - Интересным фактом является то, что такие переменные, как пропущенные занятия, состояние здоровья, количество свободного времени, желание получить высшее образование - практически не влияют на итоговую оценку госэкзамена по математике.
# - Статическую значимость для дальнейшего построения модели имеет только столбец с работой матери, а работа отца - нет.
# - Построение модели предполагается осуществлять с использованием следующих переменных: age, medu, fedu, mjob, traveltime, studytime, failures, paid, activities, nursery, goout, score.
