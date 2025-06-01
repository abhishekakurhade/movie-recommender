# 🎬 Movie Recommender System 🎥

This is a **Movie Recommender System** built using **Python**, **Pandas**, and **Streamlit**. It allows users to get personalized movie recommendations based on a selected movie’s genre, audience score, or similarity.

---

## 📌 Features

- 📂 Uses a CSV dataset of movies (`movies.csv`)
- 🧠 Content-based recommendation (genre, audience score)
- 🖥️ Built using Streamlit for a clean web interface
- 🚀 Deployed easily using Streamlit Cloud

---

## 📁 Project Structure
movie-recommender/
├── app.py # Main Streamlit application
├── movies.csv # Dataset of movies
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## 🛠️ Installation

### 🔸 Clone the repository

```bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

Run the app locally
streamlit run app.py
