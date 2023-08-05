from datetime import date, timedelta


TOKEN_HH = "#####"
TOKEN_TG = "#####"


# set date
dt = date.today() - timedelta(days=1)


# professional role code
professional_role = {

    "it": [
        156,
        12,
        150,
        25,
        34,
        155,
        96,
        164,
        113,
        148,
        124,
        125,
        126,
        ],

    "finance": [
        16,
        18,
        155,
        134,
        142,
        ],

    "lawyer": [
        145,
        146,
        ],

    "marketing": [
        3,
        10,
        12,
        34,
        55,
        68,
        99,
        ],
    }


# set parameters for download vacancies
params = {
            'per_page': 100,
            'only_with_salary': 'true',
            'currency': 'RUR',
            'date_from': dt,
            'date_to': dt,
        }


# variable for string prepare for publication
enter = [
        r"</p>", r"<div>", r"</div>",
        r"</li>", r"<ul>", r"<ol>", r"</ul>", r"</ol>",
        r"<br />",
        ]
empt = [r"<p>", ]
ch = [r"<li>", ]


# group info
group = {

    'tech': {
        'login': '@testgroupmezz',
        'id': '-1001927912168'},

    'it': {
        'login': '@itrabota_rf',
        'id': '-1001874568508'},

    'finance': {
        'login': '@rabota_fin_buh',
        'id': '-1001600013970'},

    'lawyer': {
        'login': '@ur_rabota',
        'id': '-1001947055600'},

    'marketing': {
        'login': '@rabota_marketing',
        'id': '-1001921409301'},
    }
