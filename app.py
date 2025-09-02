
import os
from flask import Flask, render_template, request, jsonify
from services.openai_service import ai_answer
from services.pubchem_service import fetch_compound
from services.balancer import balance_equation
import json

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    with open(os.path.join(data_dir, 'elements.json')) as f:
        app.config['ELEMENTS'] = json.load(f)
    with open(os.path.join(data_dir, 'glossary.json')) as f:
        app.config['GLOSSARY'] = json.load(f)
    with open(os.path.join(data_dir, 'reactions.json')) as f:
        app.config['REACTIONS'] = json.load(f)
    with open(os.path.join(data_dir, 'quiz.json')) as f:
        app.config['QUIZ'] = json.load(f)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/search')
    def search():
        q = (request.args.get('q') or '').strip()
        results = {"elements": [], "glossary": [], "reactions": [], "compound": None, "query": q}
        if not q:
            return render_template('search.html', results=results)
        for sym, el in app.config['ELEMENTS'].items():
            if q.lower() in sym.lower() or q.lower() in el['name'].lower():
                results['elements'].append({"symbol": sym, **el})
        for term, defn in app.config['GLOSSARY'].items():
            if q.lower() in term.lower() or q.lower() in defn.lower():
                results['glossary'].append({"term": term, "definition": defn})
        for rxn in app.config['REACTIONS']:
            if q.lower() in rxn['name'].lower() or q.lower() in rxn['equation'].lower():
                results['reactions'].append(rxn)
        try:
            comp = fetch_compound(q)
            if comp: results['compound'] = comp
        except Exception:
            pass
        return render_template('search.html', results=results)

    @app.route('/element/<symbol>')
    def element(symbol):
        el = app.config['ELEMENTS'].get(symbol.capitalize())
        if not el:
            return render_template('element.html', element=None, symbol=symbol), 404
        return render_template('element.html', element={"symbol": symbol.capitalize(), **el}, symbol=symbol.capitalize())

    @app.route('/glossary')
    def glossary():
        return render_template('glossary.html', glossary=app.config['GLOSSARY'])

    @app.route('/reaction')
    def reaction_page():
        return render_template('reaction.html', reactions=app.config['REACTIONS'])

    @app.route('/balance', methods=['POST'])
    def balance():
        data = request.get_json(silent=True) or {}
        eq = (data.get('equation') or '').strip()
        if not eq:
            return jsonify({"error": "No equation provided"}), 400
        try:
            balanced = balance_equation(eq)
            return jsonify({"balanced": balanced})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/ai')
    def ai_page():
        return render_template('ai_assistant.html')

    @app.route('/ask_ai', methods=['POST'])
    def ask_ai():
        data = request.get_json(silent=True) or {}
        question = (data.get('question') or '').strip()
        if not question:
            return jsonify({"error": "No question provided"}), 400
        try:
            answer = ai_answer(question)
            return jsonify({"answer": answer})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/quiz')
    def quiz():
        return render_template('quiz.html', questions=app.config['QUIZ'])

    @app.route('/health')
    def health():
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
