import pandas as pd

RELIGION_MAP = {
        # Christianity
        'christianity_protestant': ('Christianity', 'Protestant'),
        'christianity_romancatholic': ('Christianity', 'Roman Catholic'),
        'christianity_easternorthodox': ('Christianity', 'Eastern Orthodox'),
        'christianity_anglican': ('Christianity', 'Anglican'),
        'christianity_other': ('Christianity', 'Other'),

        # Judaism
        'judaism_orthodox': ('Judaism', 'Orthodox'),
        'judaism_conservative': ('Judaism', 'Conservative'),
        'judaism_reform': ('Judaism', 'Reform'),
        'judaism_other': ('Judaism', 'Other'),

        # Islam
        'islam_sunni': ('Islam', 'Sunni'),
        'islam_shi’a': ('Islam', "Shi’a"),
        'islam_ibadhi': ('Islam', 'Ibadhi'),
        'islam_nationofislam': ('Islam', 'Nation of Islam'),
        'islam_alawite': ('Islam', 'Alawite'),
        'islam_ahmadiyya': ('Islam', 'Ahmadiyya'),
        'islam_other': ('Islam', 'Other'),

        # Buddhism
        'buddhism_mahayana': ('Buddhism', 'Mahayana'),
        'buddhism_theravada': ('Buddhism', 'Theravada'),
        'buddhism_other': ('Buddhism', 'Other'),

        # Hinduism
        'hinduism_all': ('Hinduism', None),

        # Other Religions
        'sikhism_all': ('Sikhism', None),
        'shinto_all': ('Shinto', None),
        'baha’i_all': ('Baha’i', None),
        'taoism_all': ('Taoism', None),
        'jainism_all': ('Jainism', None),
        'confucianism_all': ('Confucianism', None),
        'zoroastrianism_all': ('Zoroastrianism', None),
        'syncretism_all': ('Syncretism', None),
        'animism_all': ('Animism', None),
        'noreligion_all': ('No Religion', None),
        'otherreligion_all': ('Other Religion', None),

    }

df = pd.read_csv("data/national.csv")
df = df[['year', 'state', 'code'] + list(RELIGION_MAP.keys())]
df = df.melt(id_vars=['year', 'state', 'code'], var_name='column', value_name='Followers')
df[['Religion', 'Subreligion']] = df['column'].apply(lambda x: pd.Series(RELIGION_MAP.get(x, (None, None))))
df.rename(columns={"year":"Year", "state": "Country", "code": "Country Code"}, inplace=True)
df = df[["Year", "Region","Country","Country Code","Religion", "Subreligion","Followers"]]
df["Followers"] = df["Followers"].fillna(0).astype(int)
df.to_csv("data/cleaned.csv", index=False)
