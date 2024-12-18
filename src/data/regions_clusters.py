na = [
    'United States of America', 'Canada'
]

sa_and_ca = [
    'Mexico', 'Cuba', 'Puerto Rico', 'Panama', 'Jamaica', 'Costa Rica', 'Bahamas', 'Haiti',
    'Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela', 'Peru', 'Uruguay', 'Bolivia', 'Aruba'
]

western_europe = [
    'United Kingdom', 'France', 'Italy', 'Germany', 'Spain', 'Netherlands', 'Sweden', 
    'West Germany', 'Denmark', 'Belgium', 'Norway', 'Ireland', 'Switzerland', 'Austria', 
    'Czech Republic', 'Finland', 'England', 'Greece', 'Portugal', 'Iceland', 'Luxembourg', 
    'Scotland', 'Wales', 'Monaco', 'Malta', 'Northern Ireland', 'Isle of Man', 
    'Kingdom of Great Britain', 'Weimar Republic'
]

eastern_europe = [
    'Czechoslovakia', 'Poland', 'Hungary', 'German Democratic Republic', 'Yugoslavia', 
    'Croatia', 'Romania', 'Bulgaria', 'Estonia', 'Bosnia and Herzegovina', 'Slovakia', 
    'Slovenia', 'Albania', 'Ukraine', 'Republic of Macedonia', 'Lithuania', 
    'Serbia', 'Serbia and Montenegro', 'Federal Republic of Yugoslavia', 
    'Socialist Federal Republic of Yugoslavia', 'Slovak Republic', 'Montenegro', 
    'Ukrainian SSR', 'Crimea', 'Georgian SSR', 'Uzbek SSR'
]

south_africa_and_central_africa = [
    'South Africa', 'Nigeria', 'Democratic Republic of the Congo', 'Mali', 'Kenya', 
    'Cameroon', 'Ethiopia', 'Zimbabwe', 'Congo', 'Zambia', 'Guinea-Bissau', 
    'Senegal', 'Burkina Faso', 'Guinea'
]

north_africa_and_middle_east = [
    'Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Libya', 'Iran', 'Iraq', 'Israel', 
    'Turkey', 'Lebanon', 'Jordan', 'United Arab Emirates', 'Palestinian territories', 
    'Palestinian Territories', 'Kuwait', 'Bahrain', 'Qatar', 'Afghanistan', 'Iraqi Kurdistan', 
    'Mandatory Palestine'
]

india = [
    'India'
]

remaining_asia = [
    'Japan', 'Hong Kong', 'South Korea', 'Philippines', 'Thailand', 'Taiwan', 'Indonesia', 
    'Malaysia', 'Sri Lanka', 'Singapore', 'Bangladesh', 'Nepal', 'Macau', 'Vietnam', 'Mongolia', 'Republic of China'
]

oceania = [
    'Australia', 'New Zealand'
]

# defining continents dictionary
regions = {
    'North America': na,
    'Central and South America': sa_and_ca,
    'Western Europe': western_europe,
    'Eastern Europe': eastern_europe,
    'South Africa and Central Africa': south_africa_and_central_africa,
    'North Africa and Middle East': north_africa_and_middle_east,
    'India': india,
    'Remaining Asia': remaining_asia,
    'Oceania': oceania
}

continents = {
    'North America': na,
    'South America': sa_and_ca,
    'Europe': western_europe + eastern_europe,
    'Africa': south_africa_and_central_africa + north_africa_and_middle_east,
    'Asia': india + remaining_asia,
    'Oceania': oceania
}

# dictionary to map each country to a continent
country_to_region = {}
for region, countries in regions.items():
    for country in countries:
        country_to_region[country] = region
