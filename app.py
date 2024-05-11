from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

popular_university_df = pickle.load(open('C:\\Users\\ASUS\\machine-learning-projects\\university-recommendation\\popular_university_df.pkl', 'rb'))
university = pickle.load(open('C:\\Users\\ASUS\\machine-learning-projects\\university-recommendation\\university.pkl', 'rb'))
similarity_score_all = pickle.load(open('C:\\Users\\ASUS\\machine-learning-projects\\university-recommendation\\similarity_score_all.pkl', 'rb'))


def recommendation(institution_name, top_n=10):
    try:
        institution_name = institution_name.strip().lower()  # Preprocessing input

        # Find similar institution names in lowercase
        similar_names = university['institution'].str.strip().str.lower().str.contains(institution_name)

        # Check for similarity
        if similar_names.any():
            index = similar_names[similar_names].index[0]
            similarity_scores = similarity_score_all[index]
            similar_indices = similarity_scores.argsort()[::-1][1:top_n + 1]
    
            recommendations = [university.loc[university.index[i], 'institution'] for i in similar_indices]
            recommendations = [inst for inst in recommendations if inst.lower() != institution_name]
            return recommendations
        else:
            return []
    except IndexError:
        return []



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['GET', 'POST'])
def recommend_ui():
    if request.method == 'POST':
        university_name = request.form['university_name']
        recommendations = recommendation(university_name)
        return render_template('recommendation.html', recommendations=recommendations, searched_university=university_name)
    else:
        return render_template('recommend.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
