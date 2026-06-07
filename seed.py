import requests
import pymysql
from dotenv import load_dotenv
import os
from pathlib import Path
import time

load_dotenv(Path(__file__).parent / '.env')

API_KEY = os.getenv('RAPIDAPI_KEY')
API_HOST = 'free-api-live-football-data.p.rapidapi.com'
BASE_URL = f'https://{API_HOST}'
headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': API_HOST}

def get_db():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

TEAMS = [
    ('Manchester City',    'premier_league', 'england', True,  False, True,  False, False, True,  False, False, True,  False, True,  True,  False, True,  True,  True,  True,  False),
    ('Arsenal',            'premier_league', 'england', False, True,  True,  False, True,  False, False, False, True,  False, True,  False, False, False, False, False, True,  False),
    ('Liverpool',          'premier_league', 'england', True,  True,  True,  False, True,  False, False, False, True,  False, True,  False, True,  True,  True,  False, True,  True),
    ('Chelsea',            'premier_league', 'england', True,  True,  False, False, False, True,  False, False, True,  False, True,  True,  False, False, False, False, True,  False),
    ('Manchester United',  'premier_league', 'england', True,  True,  False, False, True,  False, False, False, True,  True,  True,  False, False, False, False, False, True,  False),
    ('Real Madrid',        'la_liga',        'spain',   True,  True,  True,  False, False, False, True,  False, True,  True,  True,  False, True,  True,  True,  True,  True,  True),
    ('FC Barcelona',       'la_liga',        'spain',   True,  True,  False, False, False, True,  False, False, True,  True,  True,  False, False, False, True,  False, True,  True),
    ('Atletico Madrid',    'la_liga',        'spain',   False, True,  True,  False, True,  False, False, False, True,  False, True,  False, False, True,  False, False, False, True),
    ('Athletic Bilbao',    'la_liga',        'spain',   False, True,  False, False, True,  False, False, False, False, True,  False, False, False, False, False, False, True,  False),
    ('Villarreal',         'la_liga',        'spain',   False, False, False, False, True,  False, False, False, False, False, False, False, False, True,  False, False, False, False),
    ('Bayern Munich',      'bundesliga',     'germany', True,  True,  True,  False, True,  False, False, False, True,  True,  True,  False, False, True,  False, True,  True,  True),
    ('Borussia Dortmund',  'bundesliga',     'germany', True,  True,  False, False, True,  False, False, False, True,  True,  True,  False, False, True,  True,  False, False, True),
    ('Bayer Leverkusen',   'bundesliga',     'germany', False, True,  True,  False, True,  False, False, False, False, False, False, False, True,  False, False, False, False, False),
    ('RB Leipzig',         'bundesliga',     'germany', False, False, False, True,  True,  False, False, False, False, False, False, True,  False, False, False, False, False, False),
    ('Eintracht Frankfurt','bundesliga',     'germany', False, True,  False, False, True,  False, False, False, False, False, False, False, False, True,  False, False, False, False),
    ('Paris Saint-Germain','ligue1',         'france',  False, False, True,  False, False, True,  False, False, True,  False, True,  True,  True,  False, True,  False, False, True),
    ('Olympique Marseille','ligue1',         'france',  True,  True,  False, False, False, False, True,  False, True,  False, False, False, False, False, False, True,  False, False),
    ('Olympique Lyon',     'ligue1',         'france',  False, False, False, False, True,  False, False, False, True,  True,  False, False, False, False, False, False, False, False),
    ('Monaco',             'ligue1',         'france',  False, False, False, False, True,  False, False, False, False, True,  False, True,  False, False, False, False, False, False),
    ('Lille',              'ligue1',         'france',  False, False, False, False, True,  False, False, False, False, False, False, False, True,  False, False, False, False, False),
    ('Inter Milan',        'serie_a',        'italy',   True,  True,  True,  False, False, True,  False, False, True,  False, True,  False, True,  True,  False, True,  False, True),
    ('AC Milan',           'serie_a',        'italy',   True,  True,  False, False, True,  False, False, False, True,  False, True,  False, False, False, False, False, False, True),
    ('Juventus',           'serie_a',        'italy',   True,  True,  False, False, False, False, True,  False, True,  True,  True,  False, False, False, False, False, False, False),
    ('Napoli',             'serie_a',        'italy',   False, False, False, False, False, True,  False, False, False, False, True,  False, True,  False, False, False, False, False),
    ('AS Roma',            'serie_a',        'italy',   False, True,  False, False, True,  False, False, False, False, False, True,  False, False, True,  False, True,  False, True),
]
# Team attribute IDs
TEAM_ATTR = {
    'is_team': 2,
    'team_won_ucl': 51,
    'team_won_league_3yr': 52,
    'team_stadium_80k': 53,
    'team_won_cwc': 54,
    'team_famous_rivalry': 55,
    'team_5plus_ucl': 56,
    'team_founded_before_1900': 57,
    'team_ucl_final_5yr': 58,
    'team_named_stadium': 59,
    'team_euro_trophy_5yr': 60,
    'team_top3_league': 61,
    'team_relegated': 62,
    'team_plays_red': 63,
    'team_plays_blue': 64,
    'team_plays_white': 65,
    'team_plays_yellow': 66,
    'team_10plus_titles': 67,
    'team_famous_academy': 68,
    'team_100m_signing': 69,
    'team_state_owned': 70,
    'team_recent_champion': 71,
    'team_in_premier_league': 91,
    'team_in_la_liga': 92,
    'team_in_bundesliga': 93,
    'team_in_ligue1': 94,
    'team_in_serie_a': 95,
    'is_english': 20,
    'is_spanish': 15,
    'is_german': 16,
    'is_french': 17,
    'is_italian': 33,
}

# =====================
# NATIONS DATA  
# =====================
NATIONS = [
    # name, won_wc, won_wc_2plus, won_continental, south_america, africa, asia, north_america, wc_semi_10yr, pop_50m, hosted_wc, top10_fifa, ballon_dor, yellow, blue, red, white, wc_last_20yr, current_holder, wc_final_10yr, under_10m
    ('Brazil',      True,  True,  True,  True,  False, False, False, True,  True,  True,  True,  True,  True,  False, False, False, False, False, False, False),
    ('France',      True,  False, True,  False, False, False, False, True,  True,  True,  True,  True,  False, True,  False, False, True,  False, True,  False),
    ('Germany',     True,  True,  True,  False, False, False, False, True,  True,  True,  True,  True,  False, False, False, True,  False, False, False, False),
    ('Argentina',   True,  True,  True,  True,  False, False, False, True,  True,  False, True,  True,  False, True,  False, False, True,  True,  True,  False),
    ('Spain',       True,  False, True,  False, False, False, False, True,  True,  True,  True,  True,  False, False, True,  False, True,  False, False, False),
    ('England',     True,  False, False, False, False, False, False, True,  True,  True,  True,  False, False, False, False, True,  False, False, True,  False),
    ('Portugal',    False, False, True,  False, False, False, False, False, False, False, True,  True,  False, False, True,  False, False, False, False, False),
    ('Netherlands', False, False, False, False, False, False, False, True,  False, False, True,  False, True,  False, False, False, False, False, False, False),
    ('Italy',       True,  True,  True,  False, False, False, False, False, True,  True,  True,  False, False, True,  False, False, False, False, False, False),
    ('Morocco',     False, False, False, False, True,  False, False, True,  True,  False, False, False, False, False, True,  False, False, False, False, False),
    ('Croatia',     False, False, False, False, False, False, False, True,  False, False, True,  False, False, False, True,  False, False, False, True,  True),
    ('Belgium',     False, False, False, False, False, False, False, False, False, False, True,  False, False, False, True,  False, False, False, False, False),
    ('Uruguay',     True,  True,  True,  True,  False, False, False, False, False, True,  False, False, False, True,  False, False, False, False, False, True),
    ('USA',         False, False, False, False, False, False, True,  False, True,  True,  False, False, False, False, False, True,  False, False, False, False),
    ('Japan',       False, False, False, False, False, True,  False, False, True,  False, False, False, False, True,  False, False, False, False, False, False),
    ('Senegal',     False, False, False, False, True,  False, False, False, False, False, False, False, False, False, False, True,  False, False, False, True),
]

NATION_ATTR = {
    'is_nation': 3,
    'nation_won_wc': 71,
    'nation_won_wc_2plus': 72,
    'nation_won_continental': 73,
    'nation_south_america': 74,
    'nation_africa': 75,
    'nation_asia': 76,
    'nation_north_america': 77,
    'nation_wc_semi_10yr': 78,
    'nation_50m_pop': 79,
    'nation_hosted_wc': 80,
    'nation_top10_fifa': 81,
    'nation_ballon_dor': 82,
    'nation_plays_yellow': 83,
    'nation_plays_blue': 84,
    'nation_plays_red': 85,
    'nation_plays_white': 86,
    'nation_wc_last_20yr': 87,
    'nation_current_wc_holder': 88,
    'nation_wc_final_10yr': 89,
    'nation_under_10m_pop': 90,
}

def update_team(name, league, country, ucl, founded_1900, top3, relegated,
                red, blue, white, yellow, titles_10, academy, signing_100m,
                state_owned, recent_champ, ucl_final, euro_trophy, cwc, rivalry, ucl_5plus):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM characters WHERE name = %s AND type = 'team'", (name,))
    result = cursor.fetchone()
    if not result:
        print(f"  ✗ {name} not found")
        db.close()
        return
    char_id = result['id']

    cursor.execute("DELETE FROM character_attributes WHERE character_id = %s", (char_id,))

    attrs = {
        'is_team': 1,
        'team_won_ucl': int(ucl),
        'team_won_league_3yr': int(recent_champ),
        'team_stadium_80k': 0,
        'team_won_cwc': int(cwc),
        'team_famous_rivalry': int(rivalry),
        'team_5plus_ucl': int(ucl_5plus),
        'team_founded_before_1900': int(founded_1900),
        'team_ucl_final_5yr': int(ucl_final),
        'team_named_stadium': 0,
        'team_euro_trophy_5yr': int(euro_trophy),
        'team_top3_league': int(top3),
        'team_relegated': int(relegated),
        'team_plays_red': int(red),
        'team_plays_blue': int(blue),
        'team_plays_white': int(white),
        'team_plays_yellow': int(yellow),
        'team_10plus_titles': int(titles_10),
        'team_famous_academy': int(academy),
        'team_100m_signing': int(signing_100m),
        'team_state_owned': int(state_owned),
        'team_recent_champion': int(recent_champ),
        'team_in_premier_league': int(league == 'premier_league'),
        'team_in_la_liga': int(league == 'la_liga'),
        'team_in_bundesliga': int(league == 'bundesliga'),
        'team_in_ligue1': int(league == 'ligue1'),
        'team_in_serie_a': int(league == 'serie_a'),
        'is_english': int(country == 'england'),
        'is_spanish': int(country == 'spain'),
        'is_german': int(country == 'germany'),
        'is_french': int(country == 'france'),
        'is_italian': int(country == 'italy'),
    }

    for attr_key, value in attrs.items():
        attr_id = TEAM_ATTR.get(attr_key)
        if attr_id:
            cursor.execute(
                "INSERT INTO character_attributes (character_id, attribute_id, value) VALUES (%s, %s, %s)",
                (char_id, attr_id, value)
            )

    db.commit()
    db.close()
    print(f"  ✓ {name} updated")

def update_nation(name, won_wc, won_wc_2plus, won_cont, south_am, africa, asia,
                  north_am, wc_semi, pop_50m, hosted_wc, top10, ballon,
                  yellow, blue, red, white, wc_20yr, current, wc_final, under_10m):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM characters WHERE name = %s AND type = 'nation'", (name,))
    result = cursor.fetchone()
    if not result:
        print(f"  ✗ {name} not found")
        db.close()
        return
    char_id = result['id']

    cursor.execute("DELETE FROM character_attributes WHERE character_id = %s", (char_id,))

    attrs = {
        'is_nation': 1,
        'nation_won_wc': int(won_wc),
        'nation_won_wc_2plus': int(won_wc_2plus),
        'nation_won_continental': int(won_cont),
        'nation_south_america': int(south_am),
        'nation_africa': int(africa),
        'nation_asia': int(asia),
        'nation_north_america': int(north_am),
        'nation_wc_semi_10yr': int(wc_semi),
        'nation_50m_pop': int(pop_50m),
        'nation_hosted_wc': int(hosted_wc),
        'nation_top10_fifa': int(top10),
        'nation_ballon_dor': int(ballon),
        'nation_plays_yellow': int(yellow),
        'nation_plays_blue': int(blue),
        'nation_plays_red': int(red),
        'nation_plays_white': int(white),
        'nation_wc_last_20yr': int(wc_20yr),
        'nation_current_wc_holder': int(current),
        'nation_wc_final_10yr': int(wc_final),
        'nation_under_10m_pop': int(under_10m),
    }

    for attr_key, value in attrs.items():
        attr_id = NATION_ATTR.get(attr_key)
        if attr_id:
            cursor.execute(
                "INSERT INTO character_attributes (character_id, attribute_id, value) VALUES (%s, %s, %s)",
                (char_id, attr_id, value)
            )

    db.commit()
    db.close()
    print(f"  ✓ {name} updated")

def main():
    print("=== TENZI DATA SEEDER ===\n")

    print("Updating teams...")
    for team in TEAMS:
        update_team(*team)
        time.sleep(0.1)

    print("\nUpdating nations...")
    for nation in NATIONS:
        update_nation(*nation)
        time.sleep(0.1)

    print("\n=== DONE ===")

if __name__ == '__main__':
    main()