!pip install requests pandas sqlalchemy psycopg2-binary plotly

import requests
import pandas as pd

# AniList GraphQL query to fetch user stats
query = '''
query ($username: String) {
  User(name: $username) {
    statistics {
      anime {
        genres { genre count }
        meanScore
        episodesWatched
        minutesWatched
        tags { tag { name } count }
        scores { score count }
        formats { format count }
      }
    }
  }
}
'''

def fetch_anilist_data(username):
    variables = {'username': username}
    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    return response.json()




def save_to_db(username):
    data = fetch_anilist_data(username)['data']['User']['statistics']['anime']

    # Insert into users table
    with engine.connect() as conn:
      with conn.begin():
          conn.execute(
              text("INSERT INTO users (username) VALUES (:username) ON CONFLICT (username) DO NOTHING"),
              {"username": username}
          )
          user_id = conn.execute(
              text("SELECT user_id FROM users WHERE username = :username"),
              {"username": username}
          ).scalar()
        
        # User stats
          stats_data = {
              'user_id': user_id,
              'episodes_watched': data['episodesWatched'],
              'minutes_watched': data['minutesWatched'],
              'mean_score': data['meanScore']
          }
          pd.DataFrame([stats_data]).to_sql('user_stats', con=conn, if_exists='append', index=False)
          
          # Genres
          genres = [{'user_id': user_id, 'genre': g['genre'], 'count': g['count']} for g in data['genres']]
          pd.DataFrame(genres).to_sql('genres', con=conn, if_exists='append', index=False)
          
          # Tags
          tags = [{'user_id': user_id, 'tag': t['tag']['name'], 'count': t['count']} for t in data['tags']]
          pd.DataFrame(tags).to_sql('tags', con=conn, if_exists='append', index=False)
          
          # Scores
          scores = [{'user_id': user_id, 'score': s['score'], 'count': s['count']} for s in data['scores']]
          pd.DataFrame(scores).to_sql('scores', con=conn, if_exists='append', index=False)
          
          # Formats
          formats = [{'user_id': user_id, 'format': f['format'], 'count': f['count']} for f in data['formats']]
          pd.DataFrame(formats).to_sql('formats', con=conn, if_exists='append', index=False)

# Example usage
#save_to_db("YourAnlistUserName")
