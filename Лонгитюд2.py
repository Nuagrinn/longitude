#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[175]:


data = pd.read_csv("data.csv",engine='python', delimiter=';')


# In[176]:


data = data.fillna('Пропустили вопрос').replace({'Высшее, бакалавр или специалист':'Высшее',
                                              'Высшее, магистр':'Высшее',
                                              'Кандидат наук, доктор наук': 'Высшее',
                                              'Два и более высших образований':'Высшее',
                                              'Среднее профессиональное (например, колледж или техникум)': 'Без высшего',
                                              'Неоконченное высшее':'Без высшего',
                                              'Начальное профессиональное (например, профессиональное училище)': 'Без высшего',
                                              'Среднее (полное) общее или ниже': 'Без высшего',
                                              'Затрудняюсь ответить': 'Пропустили вопрос',
                                                'Нет, но есть детская комната, которую он делит с братом/сестрой (братьями, сестрами)':'Нет, делит с братом/сестрой',
                                                'Нет, ребенок живет в одной комнате со взрослыми родственниками': 'Нет, живет со взрослыми'
                                                })


# In[177]:


data.head()


# In[178]:


def classifier(row):
    if row['q86mom_edu'] == 'Высшее' or row['q86dad_edu'] == 'Высшее':
        return 'Высшее хотя бы у одного родителя'
    elif row['q86mom_edu'] == 'Пропустили вопрос' and row['q86dad_edu'] == 'Пропустили вопрос':
        return 'Пропустили вопрос'
    elif (row['q86mom_edu'] == 'Без высшего' and row['q86dad_edu'] == 'Пропустили вопрос') or (row['q86dad_edu'] == 'Без высшего' and row['q86mom_edu'] == 'Пропустили вопрос'):
        return 'Один без высшего, а один пропустил'
    elif row['q86mom_edu'] == 'Без высшего' and row['q86dad_edu'] == 'Без высшего':
        return 'Оба без высшего'


# In[179]:


data['parents_edu'] = data.apply(classifier, axis=1)
edu_dist = {'Уровень образования родителей': data['parents_edu'].value_counts(normalize=True)}
edu_dist_df = pd.DataFrame(edu_dist)
edu_dist_df


# In[180]:


data['parents_edu'].value_counts()


# In[181]:


edu_dist_df.plot(kind='bar').set_title('Уровень образования родителей')
plt.xticks(rotation=45)
sns.set_palette('RdBu_r')


# In[182]:


x, y, hue = 'parents_edu', 'prop', 'q87room'


prop_df = (data['parents_edu']
           .groupby(data['q87room'])
           .value_counts(normalize=True)
           .rename(y)
           .reset_index())

sns.barplot(x='parents_edu',y=y,hue='q87room', data=prop_df).legend(title='Комната ребенка')
plt.rcParams['figure.figsize'] = [8, 6]
sns.set_palette('Blues')
plt.xticks(rotation=45)
plt.xlabel('Образование родителей', fontsize=14)
plt.ylabel('Процентное соотношение', fontsize=14)


# In[183]:


data_mom_edu = data.loc[data['q86mom_edu'] != 'Пропустили вопрос']


# In[185]:


data_mom_edu.shape


# In[186]:


data_parents_edu = data.loc[data['parents_edu'] != 'Пропустили вопрос']


# In[187]:


data_parents_edu.shape


# In[188]:


data_parents_edu['parents_edu'].value_counts()


# In[189]:


data['parents_edu'].value_counts()


# In[190]:


data_mom_edu['q86mom_edu'].value_counts()


# In[193]:


prop_df


# In[194]:


x, y, hue = 'q14', 'prop', 'q86mom_edu'


prop_df = (data_mom_edu['q14']
           .groupby(data_mom_edu['q86mom_edu'])
           .value_counts(normalize=True)
           .rename(y)
           .reset_index())
prop_df['prop'] = prop_df['prop']*100

sns.barplot(x='q14',y=y,hue='q86mom_edu', data=prop_df,
            hue_order=['Высшее', 'Без высшего'],
            order=['3 и более часов в день',
                   '1-2 часа каждый день',
                   'Менее 1 часа в день',
                    'Вообще не трачу']).legend(title='Образование мамы')
plt.rcParams['figure.figsize'] = [8, 6]
sns.set_palette(flatui)
plt.xticks(rotation=45)
plt.xlabel('Время, уделяемое родителями ', fontsize=14)
plt.ylabel('Процентное соотношение', fontsize=14)


# In[195]:


x, y, hue = 'q87room', 'prop', 'q86mom_edu'


prop_df = (data_mom_edu['q87room']
           .groupby(data_mom_edu['q86mom_edu'])
           .value_counts(normalize=True)
           .rename(y)
           .reset_index())
prop_df['prop'] = prop_df['prop']*100

sns.barplot(x='q87room',y=y,hue='q86mom_edu', data=prop_df,
            hue_order=['Высшее', 'Без высшего']).legend(title='Образование мамы')
plt.rcParams['figure.figsize'] = [8, 6]
sns.set_palette(flatui)
plt.xticks(rotation=45)
plt.xlabel('Личная комната ребенка', fontsize=14)
plt.ylabel('Процентное соотношение', fontsize=14)


# In[ ]:




