from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
PLOT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/plots')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PLOT_FOLDER'] = PLOT_FOLDER


def round_values(values):
    return {k: round(v, 2) if isinstance(v, (int, float)) else v for k, v in values.items()}


def create_plots(df):
    if not os.path.exists(app.config['PLOT_FOLDER']):
        os.makedirs(app.config['PLOT_FOLDER'])

    plot_files = {'boxplot': [], 'histogram': [], 'scatter': []}
    for column in df.columns:
        plt.figure()
        sns.boxplot(y=df[column])
        boxplot_path = os.path.join(app.config['PLOT_FOLDER'], f"{column}_boxplot.png")
        plt.savefig(boxplot_path)
        plt.close()
        plot_files['boxplot'].append(f"plots/{column}_boxplot.png")

        plt.figure()
        sns.histplot(df[column], kde=True)
        histogram_path = os.path.join(app.config['PLOT_FOLDER'], f"{column}_histogram.png")
        plt.savefig(histogram_path)
        plt.close()
        plot_files['histogram'].append(f"plots/{column}_histogram.png")

        plt.figure()
        sns.scatterplot(x=df.index, y=df[column])
        scatter_path = os.path.join(app.config['PLOT_FOLDER'], f"{column}_scatter.png")
        plt.savefig(scatter_path)
        plt.close()
        plot_files['scatter'].append(f"plots/{column}_scatter.png")

    return plot_files


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        df = pd.read_excel(filepath)

        # Berechnungen
        stats = {
            'Mean': round_values(df.mean().to_dict()),
            'Median': round_values(df.median().to_dict()),
            'Variance': round_values(df.var().to_dict()),
            'Standard Deviation': round_values(df.std().to_dict()),
            'Max': df.max().to_dict(),
            'Min': df.min().to_dict()
        }

        plot_files = create_plots(df)

        return render_template('result.html', stats=stats, plots=plot_files, selected_plot='boxplot')


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
