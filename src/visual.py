import plotly.express as px

def plot_top_genres(username):
    # Get user_id
    user_id = pd.read_sql(f"SELECT user_id FROM users WHERE username = '{username}'", engine).iloc[0]['user_id']
    
    # Query genres
    df = pd.read_sql(f"""
        SELECT genre, count 
        FROM genres 
        WHERE user_id = {user_id}
        ORDER BY count DESC 
        LIMIT 10
    """, engine)
    
    fig = px.bar(df, x='genre', y='count', title=f"Top Genres for {username}")
    fig.show()

def plot_score_distribution(username):
    user_id = pd.read_sql(f"SELECT user_id FROM users WHERE username = '{username}'", engine).iloc[0]['user_id']
    
    df = pd.read_sql(f"""
        SELECT score, count 
        FROM scores 
        WHERE user_id = {user_id}
        ORDER BY score
    """, engine)
    
    fig = px.line(df, x='score', y='count', title="Anime Score Distribution")
    fig.show()
