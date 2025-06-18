
# 💊 Medicine Prescription Analyzer

A web-based application that analyzes **handwritten medical prescriptions** using a combination of **deep learning models** and **GPT-based natural language processing**. It extracts, interprets, and classifies medicines, dosages, and instructions from scanned or photographed handwritten prescriptions.

---

## 🚀 Features

- 📤 Upload handwritten prescription images (JPEG, PNG, etc.)
- 🧠 Combines **deep learning** for handwriting recognition with **GPT** for intelligent interpretation
- 🔎 Extracts key details:
  - Medicine names
  - Dosage and frequency
  - Instructional context
- 🤖 Dual-model architecture for robust predictions
- 📄 Uses CSV datasets for training data and label mappings

---

## 🛠️ Technologies Used

| Component       | Technology                        |
|----------------|------------------------------------|
| Backend         | Python, Flask                     |
| Frontend        | HTML (Jinja templates)            |
| ML Models       | CNN-based classifiers (PyTorch or similar) |
| NLP Interpreter | OpenAI GPT (e.g., GPT-3.5, GPT-4) |
| Data Storage    | CSV files                         |

---

## 🧬 Project Structure

```
├── app.py                      # Flask app and API routes
├── application_both_models.py # ML model logic
├── dataloader_iam.py          # Image preprocessing
├── config.py                  # Paths and constants
├── benchmarks.py              # Performance analysis
├── medicine_data.csv          # Dataset of medicine labels
├── classes.txt                # Class names
├── templates/                 # HTML templates
├── static/                    # Uploaded images
```

---

## 🔗 How It Works

1. **Upload** a handwritten prescription image.
2. Image is **preprocessed** and passed to deep learning models.
3. The output labels (e.g., drug name, dosage) are interpreted by a **GPT model** for context-aware classification.
4. The **final output** includes cleaned-up text with extracted details, shown on the web interface.

---

## 🧪 GPT Integration

- **Use Case**: Interpreting ambiguous or shorthand instructions, disambiguating drug names, and generating structured summaries.
- **Example**: Raw model output – `"paracitamol 2/d"`, GPT transforms it into – `"Paracetamol, 500mg, twice a day"`.

---

## 📦 Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/medicine-prescription-analyzer.git
   cd medicine-prescription-analyzer
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-api-key  # or store it in config.py
   ```

5. Run the Flask app:
   ```bash
   python app.py
   ```

6. Go to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🧠 Use Cases

- Automating handwritten prescription reading in pharmacies and hospitals
- Digitizing old or unstructured prescription data
- Providing structured output for integration with EMR/eRx systems

---

## 🚧 Future Enhancements

- Real-time OCR with better handwriting recognition
- Integration with live pharmacy databases
- Save/export reports as PDFs
- Multi-language support
- Role-based access (doctor, pharmacist, patient)

---

## 📄 License

MIT License – Open-source, free to use and modify.
