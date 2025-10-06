# FASTA_Analyser 🧬

A simple Flask-based web application for analyzing biological FASTA files.

This tool allows users to upload FASTA files, view key information about DNA or protein sequences, and export results in CSV format. It uses **BioPython** for sequence parsing and analysis, providing an easy-to-use interface for researchers and students in bioinformatics or molecular biology.

---

## 🚀 Features

* Upload and analyze **FASTA files** directly from your browser
* Extract key details such as:

  * Sequence ID
  * Sequence length
  * GC content (for DNA sequences)
* Export results to **CSV format**
* Simple, lightweight web UI built with **Flask**
* Uses **BioPython** for biological data parsing

---

## 🧩 Tech Stack

* **Python 3.10+**
* **Flask**
* **BioPython**
* **Pandas**
* **HTML/CSS (Bootstrap for styling)**

---

## 📂 Project Structure

```
FASTA_Analyser/
│
├── app.py                # Flask main application file
├── static/               # CSS and JS files
│   └── style.css
├── templates/            # HTML templates
│   ├── index.html
│   └── results.html
├── uploads/              # Uploaded FASTA files
├── results/              # CSV exports
└── README.md
```

---

## ⚙️ Installation & Setup

1. **Clone this repository**

   ```bash
   git clone https://github.com/yourusername/FASTA_Analyser.git
   cd FASTA_Analyser
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install flask biopython pandas
   ```

4. **Run the Flask server**

   ```bash
   python app.py
   ```

5. **Access the app in your browser**

   ```
   http://127.0.0.1:5000
   ```

---

## 📤 How to Use

1. Run the Flask app locally.
2. Open the website in your browser.
3. Upload a `.fasta` file (you can find example FASTA files [here](https://www.ncbi.nlm.nih.gov/nuccore/)).
4. The app will:

   * Display sequence details
   * Calculate GC content
   * Allow you to download the CSV file of results

---

## 📊 Example Output

| Sequence ID | Sequence Length | GC Content (%) |
| ----------- | --------------- | -------------- |
| seq1        | 1200            | 48.5           |
| seq2        | 980             | 42.1           |

---

## 🔍 API Integration (Optional)

You can enhance this project by integrating a **free biological API** such as:

* **EBI NCBI API** for fetching sequence metadata
* **UniProt REST API** for protein data retrieval

Example:

```python
import requests

response = requests.get("https://rest.uniprot.org/uniprotkb/P69905.fasta")
print(response.text)
```

---

## 🧠 Future Enhancements

* Add multiple file upload support
* Visualize GC content using charts
* Integrate sequence alignment (BLAST API)
* Add login system for saving analysis history

---

## 📜 License

This project is open-source and free to use under the **MIT License**.

---

## 👨‍💻 Author

**Majid Bahader**
Python Backend Developer | Bioinformatics Enthusiast
📧 majidbahader86@gmail.com
