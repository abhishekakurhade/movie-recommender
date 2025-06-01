import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("C:/Users/abhis/OneDrive/Desktop/movie recomder/movies.csv")

# Clean and prepare data
df = df[['Film', 'Genre', 'Lead Studio', 'Audience score %', 'Rotten Tomatoes %']].dropna()
df['Audience score %'] = pd.to_numeric(df['Audience score %'], errors='coerce')
df['Rotten Tomatoes %'] = pd.to_numeric(df['Rotten Tomatoes %'], errors='coerce')
df = df.dropna(subset=['Audience score %', 'Rotten Tomatoes %'])

# Combine text features into one
df['combined_features'] = df['Genre'] + " " + df['Lead Studio']

# Vectorize text
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Normalize numeric scores
scaler = MinMaxScaler()
numeric_features = scaler.fit_transform(df[['Audience score %', 'Rotten Tomatoes %']])

# Combine all features
import numpy as np
final_matrix = np.hstack([tfidf_matrix.toarray(), numeric_features])

# Similarity matrix
cos_sim = cosine_similarity(final_matrix)

# Recommendation function
def recommend_by_title(title):
    if title not in df['Film'].values:
        return ["Movie not found!"]
    idx = df[df['Film'] == title].index[0]
    sim_scores = list(enumerate(cos_sim[idx]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    recommendations = [df.iloc[i[0]]['Film'] for i in sorted_scores]
    return recommendations

# ---------------------- Streamlit GUI ----------------------
st.title("🎬 Smarter Movie Recommender System")

tab1, tab2 = st.tabs(["🔍 Recommend by Movie Title", "🎯 Filter by Genre & Score"])

with tab1:
    st.subheader("Find movies similar to your favorite one")
    selected_movie = st.selectbox("Select a movie", sorted(df['Film'].unique()))
    if st.button("Get Recommendations"):
        recs = recommend_by_title(selected_movie)
        st.write("🧠 Recommended Movies Similar to:", selected_movie)
        for movie in recs:
            st.write("➡️", movie)

with tab2:
    st.subheader("Find movies by genre and audience score")
    selected_genre = st.selectbox("Choose a genre", sorted(df['Genre'].unique()))
    min_score = st.slider("Minimum Audience Score (%)", 0, 100, 70)

    if st.button("Filter Movies"):
        filtered = df[
            (df['Genre'] == selected_genre) &
            (df['Audience score %'] >= min_score)
        ][['Film', 'Audience score %']].sort_values(by='Audience score %', ascending=False)

        if filtered.empty:
            st.warning("No movies found for this genre and score.")
        else:
            st.write(f"🎯 {selected_genre} Movies with ≥ {min_score}% Audience Score:")
            for _, row in filtered.iterrows():
                st.write(f"➡️ **{row['Film']}** — {int(row['Audience score %'])}%")
