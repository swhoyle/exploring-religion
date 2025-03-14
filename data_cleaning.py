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

COUNTRY_TO_REGION_MAP = {
    # North America
    'United States of America': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
    'Bahamas': 'North America', 'Cuba': 'North America', 'Haiti': 'North America',
    'Dominican Republic': 'North America', 'Jamaica': 'North America', 'Trinidad and Tobago': 'North America',
    'Barbados': 'North America', 'Dominica': 'North America', 'Grenada': 'North America', 'St. Lucia': 'North America',
    'St. Vincent and the Grenadines': 'North America', 'Antigua & Barbuda': 'North America',
    'St. Kitts and Nevis': 'North America', 'Belize': 'North America', 'Guatemala': 'North America',
    'Honduras': 'North America', 'El Salvador': 'North America', 'Nicaragua': 'North America',
    'Costa Rica': 'North America', 'Panama': 'North America',

    # South America
    'Colombia': 'South America', 'Venezuela': 'South America', 'Guyana': 'South America',
    'Suriname': 'South America', 'Ecuador': 'South America', 'Peru': 'South America',
    'Brazil': 'South America', 'Bolivia': 'South America', 'Paraguay': 'South America',
    'Chile': 'South America', 'Argentina': 'South America', 'Uruguay': 'South America',

    # Europe
    'United Kingdom': 'Europe', 'Ireland': 'Europe', 'Netherlands': 'Europe', 'Belgium': 'Europe', 
    'Luxembourg': 'Europe', 'France': 'Europe', 'Monaco': 'Europe', 'Liechtenstein': 'Europe', 
    'Switzerland': 'Europe', 'Spain': 'Europe', 'Andorra': 'Europe', 'Portugal': 'Europe', 
    'Germany': 'Europe', 'German Federal Republic': 'Europe', 'German Democratic Republic': 'Europe', 
    'Poland': 'Europe', 'Austria': 'Europe', 'Hungary': 'Europe', 'Czechoslovakia': 'Europe', 
    'Czech Republic': 'Europe', 'Slovakia': 'Europe', 'Italy': 'Europe', 'San Marino': 'Europe', 
    'Malta': 'Europe', 'Albania': 'Europe', 'Montenegro': 'Europe', 'Macedonia': 'Europe', 
    'Croatia': 'Europe', 'Yugoslavia': 'Europe', 'Bosnia and Herzegovina': 'Europe', 
    'Kosovo': 'Europe', 'Slovenia': 'Europe', 'Greece': 'Europe', 'Cyprus': 'Europe', 
    'Bulgaria': 'Europe', 'Moldova': 'Europe', 'Romania': 'Europe', 'Russia': 'Europe', 
    'Estonia': 'Europe', 'Latvia': 'Europe', 'Lithuania': 'Europe', 'Ukraine': 'Europe', 
    'Belarus': 'Europe', 'Armenia': 'Europe', 'Georgia': 'Europe', 'Azerbaijan': 'Europe', 
    'Finland': 'Europe', 'Sweden': 'Europe', 'Norway': 'Europe', 'Denmark': 'Europe', 'Iceland': 'Europe',

    # Africa
    'Cape Verde': 'Africa', 'Sao Tome and Principe': 'Africa', 'Guinea-Bissau': 'Africa', 
    'Equatorial Guinea': 'Africa', 'Gambia': 'Africa', 'Mali': 'Africa', 'Senegal': 'Africa', 
    'Benin': 'Africa', 'Mauritania': 'Africa', 'Niger': 'Africa', 'Ivory Coast': 'Africa', 
    'Guinea': 'Africa', 'Burkina Faso': 'Africa', 'Liberia': 'Africa', 'Sierra Leone': 'Africa', 
    'Ghana': 'Africa', 'Togo': 'Africa', 'Cameroon': 'Africa', 'Nigeria': 'Africa', 'Gabon': 'Africa', 
    'Central African Republic': 'Africa', 'Chad': 'Africa', 'Congo': 'Africa', 
    'Democratic Republic of the Congo': 'Africa', 'Uganda': 'Africa', 'Kenya': 'Africa', 
    'Tanzania': 'Africa', 'Burundi': 'Africa', 'Rwanda': 'Africa', 'Somalia': 'Africa', 
    'Djibouti': 'Africa', 'Ethiopia': 'Africa', 'Eritrea': 'Africa', 'Angola': 'Africa', 
    'Mozambique': 'Africa', 'Zambia': 'Africa', 'Zimbabwe': 'Africa', 'Malawi': 'Africa', 
    'South Africa': 'Africa', 'Namibia': 'Africa', 'Lesotho': 'Africa', 'Botswana': 'Africa', 
    'Swaziland': 'Africa', 'Madagascar': 'Africa', 'Comoros': 'Africa', 'Mauritius': 'Africa', 
    'Seychelles': 'Africa', 'Morocco': 'Africa', 'Algeria': 'Africa', 'Tunisia': 'Africa', 
    'Libya': 'Africa', 'Sudan': 'Africa',

    # Mideast
    'Iran': 'Mideast', 'Turkey': 'Mideast', 'Iraq': 'Mideast', 'Egypt': 'Mideast', 'Syria': 'Mideast', 
    'Lebanon': 'Mideast', 'Jordan': 'Mideast', 'Israel': 'Mideast', 'Saudi Arabia': 'Mideast', 
    'Yemen Arab Republic': 'Mideast', 'Yemen': 'Mideast', "Yemen People's Republic": 'Mideast', 
    'Kuwait': 'Mideast', 'Bahrain': 'Mideast', 'Qatar': 'Mideast', 'United Arab Emirates': 'Mideast', 
    'Oman': 'Mideast', 'Afghanistan': 'Mideast',

    # Asia
    'Turkmenistan': 'Asia', 'Tajikistan': 'Asia', 'Kyrgyzstan': 'Asia', 'Uzbekistan': 'Asia', 
    'Kazakhstan': 'Asia', 'China': 'Asia', 'Mongolia': 'Asia', 'Taiwan': 'Asia', 'North Korea': 'Asia', 
    'South Korea': 'Asia', 'Japan': 'Asia', 'India': 'Asia', 'Bhutan': 'Asia', 'Pakistan': 'Asia', 
    'Bangladesh': 'Asia', 'Myanmar': 'Asia', 'Sri Lanka': 'Asia', 'Maldives': 'Asia', 'Nepal': 'Asia', 
    'Thailand': 'Asia', 'Cambodia': 'Asia', 'Laos': 'Asia', 'Vietnam': 'Asia', 'Republic of Vietnam': 'Asia', 
    'Malaysia': 'Asia', 'Singapore': 'Asia', 'Brunei': 'Asia', 'Philippines': 'Asia', 'Indonesia': 'Asia', 
    'East Timor': 'Asia',

    # Oceania
    'Australia': 'Oceania', 'Papua New Guinea': 'Oceania', 'New Zealand': 'Oceania', 
    'Vanuatu': 'Oceania', 'Solomon Islands': 'Oceania', 'Kiribati': 'Oceania', 'Tuvalu': 'Oceania', 
    'Fiji': 'Oceania', 'Tonga': 'Oceania', 'Nauru': 'Oceania', 'Marshall Islands': 'Oceania', 
    'Palau': 'Oceania', 'Federated States of Micronesia': 'Oceania', 'Samoa': 'Oceania'
}

df = pd.read_csv("data/national.csv")
df = df[['year', 'state', 'code'] + list(RELIGION_MAP.keys())]
df = df.melt(id_vars=['year', 'state', 'code'], var_name='column', value_name='Followers')
df["Region"] = df["state"].map(COUNTRY_TO_REGION_MAP)
df[['Religion', 'Subreligion']] = df['column'].apply(lambda x: pd.Series(RELIGION_MAP.get(x, (None, None))))
df.rename(columns={"year":"Year", "state": "Country", "code": "Country Code"}, inplace=True)
df = df[["Year", "Region","Country","Country Code","Religion", "Subreligion","Followers"]]
df["Followers"] = df["Followers"].fillna(0).astype(int)
df.to_csv("data/cleaned.csv", index=False)
