from flask import Flask, render_template, request, send_file
import pandas as pd
from fuzzywuzzy import fuzz, process
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import openai
import os

# ✅ OpenRouter API Key
OPENROUTER_API_KEY = "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"

client = openai.OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

app = Flask(__name__)

last_prediction = None
last_gpt_results = None
last_lowest_price_details = None

def get_medicine_info_from_gpt(medicine_name, price):
    prompt = (
        f"Provide a clean and realistic bullet-point summary for this medicine:\n"
        f"Medicine: {medicine_name}\n"
        f"Price per tablet: INR {price}\n\n"
        f"Include the following sections:\n"
        f"- DOSAGE: Use realistic timing like 1-0-1, 1-1-1, or 0-1-1\n"
        f"- COMPOSITION: Ingredients and their quantities\n"
        f"- MAX USAGE: Recommended number of days and explanation\n"
        f"- SIDE EFFECTS: Common and serious effects\n"
        f"- WARNINGS & AGE RESTRICTIONS: Important safety info\n"
        f"- PRICE: State only 'INR {price}'\n\n"
        f"Format each section with an ALL CAPS heading followed by bullet points (•).\n"
        f"Do NOT use asterisks (*), hashtags (#), or markdown symbols."
    )
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=500,
            extra_headers={
                "HTTP-Referer": "https://yourdomain.com",
                "X-Title": "Medical Prescription Analyzer"
            }
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error retrieving info from GPT: {e}"

@app.route('/')
def home():
    return render_template('index.html', title='Medical Prescription')

@app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    global last_prediction, last_gpt_results, last_lowest_price_details
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            with open('input.png', 'wb') as f:
                f.write(file.read())

            from application_both_models import all_task
            prediction = all_task()

            with open('medicine_names.txt', 'r') as f:
                actual_medicine_names = [line.strip() for line in f]

            def get_best_match(name):
                match, _ = process.extractOne(name, actual_medicine_names, scorer=fuzz.token_sort_ratio)
                return match

            improved_predictions = [get_best_match(name) for name in prediction]

            medicine_data = pd.read_csv('medicine_data.csv')
            lowest_price_details = []
            gpt_results = []

            for medicine_name in improved_predictions:
                filtered_data = medicine_data[medicine_data['medicine_names'] == medicine_name]
                if not filtered_data.empty:
                    lowest_price_row = filtered_data.loc[filtered_data['price'].idxmin()]
                    price = lowest_price_row['price']
                    lowest_price_details.append({
                        'medicine_name': medicine_name,
                        'price': price
                    })

                    gpt_results.append({
                        'medicine_name': medicine_name,
                        'gpt_summary': get_medicine_info_from_gpt(medicine_name, price)
                    })

            last_prediction = "THE MEDICINE DETECTED ARE AS FOLLOWS:"
            last_gpt_results = gpt_results
            last_lowest_price_details = pd.DataFrame(lowest_price_details)

            return render_template(
                'disease-result.html',
                prediction=last_prediction,
                lowest_price_details=last_lowest_price_details,
                gpt_results=gpt_results,
                title="Medical Prescription Detection"
            )

    return render_template('disease.html', title='Medical Prescription')

@app.route('/download-report')
def download_report():
    if not last_gpt_results or last_lowest_price_details is None:
        return "No report available to download", 404

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16, alignment=1)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10)

    elements.append(Paragraph("Medical Prescription Analysis Report", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Detected Medicines with Lowest Price Options", heading_style))
    data = [["Medicine", "Price (INR)"]]
    for row in last_lowest_price_details.itertuples(index=False):
        data.append([row.medicine_name, f"INR {row.price}"])
    table = Table(data, colWidths=[3.5 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("GPT-Powered Medicine Analysis", heading_style))
    for i, entry in enumerate(last_gpt_results, 1):
        elements.append(Paragraph(f"{i}. <b>{entry['medicine_name'].upper()}</b>", heading_style))
        lines = entry["gpt_summary"].replace("₹", "INR").replace("*", "").split('\n')
        for line in lines:
            cleaned = line.strip()
            if cleaned.isupper():
                elements.append(Paragraph(f"<b>{cleaned}</b>", heading_style))
            elif cleaned.startswith("•"):
                elements.append(Paragraph(cleaned, ParagraphStyle(
                    name="JustifiedBullet",
                    parent=body_style,
                    alignment=4,
                    spaceAfter=6
                )))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='gpt_medicine_summary.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
