import logging
import requests
import pandas as pd
import numpy as np
import json
from data.info import professional_role, enter, empt, ch
from datetime import date, timedelta


# set date
dt = date.today() - timedelta(days=1)


# write logs
logging.basicConfig(
    filename=r"data/log_hh.txt",
    level=logging.INFO,
    format="%(asctime)s %(funcName)s %(processName)s %(message)s"
    )


class Job:

    def __init__(self, professional_role, token, salary, params):
        self.professional_role = professional_role
        self.token = token
        self.salary = salary
        self.params = params

    # get vacancies list with short info
    def get_vacant_prof_lst(self, prof, page: int):
        API_URL = 'https://api.hh.ru/vacancies'
        self.params['page'] = page
        self.params['professional_role'] = prof
        r = requests.get(API_URL, params=self.params, headers={'Authorization': 'Bearer %s' % self.token}, timeout=40)
        r = r.json()
        return r

    # get number of pages
    def get_pages(self, prof):
        API_URL = 'https://api.hh.ru/vacancies'
        self.params['professional_role'] = prof
        r = requests.get(API_URL, params=self.params, headers={'Authorization': 'Bearer %s' % self.token}, timeout=40)
        r = r.json()
        self.params['professional_role'] = ''
        return r['pages']

    # get number of vacancies
    def get_nums(self, prof):
        API_URL = 'https://api.hh.ru/vacancies'
        self.params['professional_role'] = prof
        r = requests.get(API_URL, params=self.params, headers={'Authorization': 'Bearer %s' % self.token}, timeout=40)
        r = r.json()
        self.params['professional_role'] = ''
        return r['found']

    # get full information about the vacancy
    def get_vacant(self, vacant_id):
        API_URL = 'https://api.hh.ru/vacancies/%s' % vacant_id
        r = requests.get(API_URL, headers={'Authorization': 'Bearer %s' % self.token}, timeout=40)
        r = r.json()
        return r


# get phone number from dict
def get_phones(i):
    result_lst = [("{}, {}".format(x['formatted'], x['comment'])).replace(", None", "") for x in i['phones']]
    result = ", ".join(result_lst)
    return result


# set schedule hashtag
def get_schedule(schedule):
    result = "#{}".format(schedule.replace(" ", "").lower())
    return result


# set professionale role hashtag
def get_prof(prof_role):
    for role in prof_role:
        result_lst = ["#{}".format(x.replace(" ", "").replace("-", "").lower()) for x in role['name'].split(", ")]
        result = ", ".join(result_lst)
    return result


# bulk substring replacement
def replace_lst(old_str, lst, new_str):
    for x in lst:
        old_str = old_str.replace(x, new_str)
    return old_str


# formatting
def print_txt(x):
    x.replace("\\s", " ")
    while x.count("\n "):
        x = x.replace("\n ", "\n")
    while x.count("\n\n"):
        x = x.replace("\n\n", "\n")
    x = x.replace("\n<strong>", "\n\n<strong>")
    return x


def get_data(role):
    vacant_df_lst = pd.DataFrame()

    for i in professional_role[role.professional_role]:
        # get basic information
        vacant_short = role.get_vacant_prof_lst(i, 0)
        # cycle through pages

        for page in range(vacant_short['pages']):
            vacant_short = role.get_vacant_prof_lst(i, page)

            for a in vacant_short['items']:
                # split salary on 2 columns
                try:
                    a['salary_from'] = a['salary']['from']
                    a['salary_to'] = a['salary']['to']
                    a['salary_currency'] = a['salary']['currency']
                    a.pop('salary')
                except:
                    pass

            vacant_df = pd.DataFrame.from_dict(vacant_short['items'])
            try:
                # delete vacancies without contacts
                vacant_df = vacant_df.dropna(subset=['contacts'])
            except:
                pass

            try:
                # filter salary
                vacant_df = vacant_df[(vacant_df['salary_from']>=role.salary) & (vacant_df['salary_currency']=='RUR')]
            except:
                pass

            # concatinate dataframe
            vacant_df_lst = pd.concat([vacant_df_lst, vacant_df])

    return vacant_df_lst


def vacancy(role, role_vac_df):
    vacant_detail_lst = []

    for r_id in role_vac_df['id']:
        role_vac = role.get_vacant(r_id)
        vacant_detail_lst.append(role_vac)

    vacant_detail_df = pd.DataFrame(vacant_detail_lst)
    vacant_detail_df['professional_roles'] = vacant_detail_df['professional_roles'].apply(lambda x: get_prof(x))
    vacant_detail_df['area'] = vacant_detail_df['area'].apply(lambda x: dict(x)['name'])
    vacant_detail_df['experience'] = vacant_detail_df['experience'].apply(lambda x: dict(x)['name'])
    vacant_detail_df['schedule'] = vacant_detail_df['schedule'].apply(lambda x: get_schedule(dict(x)['name'].lower()))
    vacant_detail_df['employment'] = vacant_detail_df['employment'].apply(lambda x: dict(x)['name'])
    vacant_detail_df['salary_from'] = vacant_detail_df['salary'].apply(lambda x: dict(x)['from'])
    vacant_detail_df['salary_to'] = vacant_detail_df['salary'].apply(lambda x: dict(x)['to'])
    vacant_detail_df['salary_currency'] = vacant_detail_df['salary'].apply(lambda x: dict(x)['currency'])
    vacant_detail_df['contacts_name'] = vacant_detail_df['contacts'].apply(lambda x: dict(x)['name'])
    vacant_detail_df['contacts_email'] = vacant_detail_df['contacts'].apply(lambda x: dict(x)['email'])
    vacant_detail_df['contacts_phones'] = vacant_detail_df['contacts'].apply(get_phones)
    vacant_detail_df['description'] = vacant_detail_df['description'].apply(lambda x: replace_lst(x, enter, "\n"))
    vacant_detail_df['description'] = vacant_detail_df['description'].apply(lambda x: replace_lst(x, empt, ""))
    vacant_detail_df['description'] = vacant_detail_df['description'].apply(lambda x: replace_lst(x, ch, "- "))
    vacant_detail_df['published'] = False
    vacant_detail_df.replace(np.nan, None)

    df_list = pd.DataFrame(
        vacant_detail_df, columns=[
            'id',
            'name',
            'professional_roles',
            'area', 'experience',
            'schedule',
            'employment',
            'salary_from',
            'salary_to',
            'salary_currency',
            'description',
            'contacts_name',
            'contacts_email',
            'contacts_phones',
            'has_test',
            'apply_alternate_url',
            'published',
            'published_time'
            ]
        )
    result = df_list

    return result
