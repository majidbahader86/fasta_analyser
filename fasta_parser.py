from Bio import SeqIO
import pandas as pd

def parse_fasta(file_path, output_csv="output.csv"):
    records = []
    for record in SeqIO.parse(file_path, "fasta"):
        records.append({
            "ID": record.id,
            "Description": record.description,
            "Sequence_Length": len(record.seq),
            "GC_Content": (record.seq.count("G") + record.seq.count("C")) / len(record.seq) * 100
        })

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"Saved results to {output_csv}")

if __name__ == "__main__":
    parse_fasta("sample.fasta")
