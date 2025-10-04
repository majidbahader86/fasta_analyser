FASTA Analyzer 🧬




FASTA Analyzer is a Python tool to parse and analyze DNA sequences from FASTA files. It calculates sequence metrics and exports results to a CSV file. Ideal for bioinformatics beginners or for lab data processing.

Features ✅

Parse FASTA files and extract sequences

Compute sequence metrics:

Sequence length

GC content (%)

Export results to CSV in a dedicated results/ folder

Ready for extension with GUI, batch processing, or visualizations

Demo / Screenshots 📸

Placeholder: add screenshots after GUI is ready or CSV output example

example output:
ID   | Description          | Sequence_Length | GC_Content
seq1 | Example sequence 1   | 34              | 55.88
seq2 | Example sequence 2   | 36              | 50.00

Project Structure 📂
fasta_analyser/
│── fasta_parser.py       # Main parser script
│── sample.fasta          # Example input FASTA file
│── output.csv            # Generated CSV output
│── results/              # Folder for CSV outputs
│── README.md             # Project documentation

Dependencies 🛠️

Python 3.x

BioPython
 → pip install biopython

pandas
 → pip install pandas

Optional (for GUI and visualizations later):

Tkinter (built-in with Python)

Matplotlib / Seaborn → pip install matplotlib seaborn

Installation & Usage 💻

Clone the repository:

git clone https://github.com/yourusername/fasta_analyser.git
cd fasta_analyser


(Optional) Create a virtual environment:

python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install biopython pandas


Place your FASTA file in the project folder (or use sample.fasta).

Run the parser:

python fasta_parser.py


Check the results/ folder for output.csv.

Example Output 📊
ID	Description	Sequence_Length	GC_Content
seq1	Example sequence 1	34	55.88
seq2	Example sequence 2	36	50.00
Next Steps / Enhancements 🚀

Add Tkinter GUI for easy file selection and CSV export

Add additional metrics: AT content, ambiguous nucleotides, sequence preview

Batch processing for multiple FASTA files

Visualizations: GC content distribution, sequence length histogram

Modularize code into separate files for professional structure:
parser.py, analyzer.py, exporter.py, gui.py

License 📄

MIT License

Majid, if you want, I can also create a ready-to-push GitHub folder structure with your current files, results folder, sample FASTA, and this README — so you can push it directly as a professional project portfolio.