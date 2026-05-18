from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
docs = [
"I enjoy running in the park every morning for exercise.",
"The gym has several modern running machines for cardio workouts.",
"Many people use a treadmill running machine during winter.",
"Professional runners train every day to improve their running speed.",
"Machine learning models analyze image data for object recognition.",
"Researchers train neural networks to classify medical images.",
"I took a beautiful image of the sunset near the beach.",
"Food bloggers upload delicious restaurant images on social media.",
"People often search for restaurant images before choosing a place to eat.",
"Computer vision systems learn patterns from large image datasets."
]

model = TfidfVectorizer()
tfidf = model.fit_transform(docs)

print(tfidf)
while True:
    words = input('query words: ')
    q_tfidf = model.transform([words])
    cos_sim = cosine_similarity(q_tfidf, tfidf).flatten()
    idxs = cos_sim.argsort()[:-2:-2] #상위 2개
    for idx in idxs:
        print(docs[idx])
