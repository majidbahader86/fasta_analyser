# src/parser.py
import re
import time
import os
from Bio import SeqIO, Entrez
import pandas as pd

# Entrez email MUST be set in environment before using fetch functions
Entrez.email = os.environ.get("ENTREZ_EMAIL", "")

def extract_accession(description: str):
    """
    Try to find a RefSeq-like accession in the sequence description.
    Heuristic: looks for patterns like NM_000000.1, NP_000000.1, XP_123456.1, or plain ACCESSION.NUM
    Returns accession string or None.
    """
    if not description:
        return None
    # common pattern: letters + underscore + digits + optional .version
    m = re.search(r'\b([A-Z]{1,3}_\d+(?:\.\d+)?)\b', description)
    if m:
        return m.group(1)
    # fallback: look for 'gi|' token or simple accession-like tokens
    m = re.search(r'\bgi\|\d+\b', description)
    if m:
        return m.group(0)
    # any token with letters+digits might be an accession
    m = re.search(r'\b([A-Za-z0-9\.\-_]{5,25})\b', description)
    if m:
        # crude filter to avoid picking generic words — keep if contains digit
        tok = m.group(1)
        if re.search(r'\d', tok):
            return tok
    return None

def fetch_ncbi_metadata(accession: str, db_try_order=('nuccore', 'protein')):
    """
    Given an accession-like string, attempt to retrieve metadata from NCBI using Entrez.
    Returns a dict with fields or None if not found.
    """
    if not accession or Entrez.email == "":
        return None
    # be polite and throttle: NCBI recommends keeping requests modest
    time.sleep(0.34)  # ~3 requests/second max
    for db in db_try_order:
        try:
            # search for the accession in the db
            handle = Entrez.esearch(db=db, term=accession, retmode="json")
            record = Entrez.read(handle)
            handle.close()
            idlist = record.get("IdList", [])
            if not idlist:
                continue
            uid = idlist[0]
            # fetch GenBank record and parse with SeqIO (gives annotations)
            handle = Entrez.efetch(db=db, id=uid, rettype="gb", retmode="text")
            try:
                seqrec = SeqIO.read(handle, "gb")
                handle.close()
                meta = {
                    "ncbi_db": db,
                    "ncbi_uid": uid,
                    "ncbi_title": seqrec.description,
                    "ncbi_organism": seqrec.annotations.get("organism", ""),
                    "ncbi_source": seqrec.annotations.get("source", ""),
                }
                return meta
            except Exception:
                # fallback: try esummary to get title-like summary
                handle.close()
                handle = Entrez.esummary(db=db, id=uid, retmode="xml")
                try:
                    summary = Entrez.read(handle)
                    handle.close()
                    # summary structure can vary; be defensive
                    if summary and "DocumentSummarySet" in summary:
                        docs = summary["DocumentSummarySet"].get("DocumentSummary", [])
                        if docs:
                            doc = docs[0]
                            return {
                                "ncbi_db": db,
                                "ncbi_uid": uid,
                                "ncbi_title": doc.get("Title") or doc.get("Title", ""),
                                "ncbi_organism": doc.get("Organism", ""),
                            }
                except Exception:
                    pass
        except Exception:
            continue
    return None

def parse_fasta(file_path: str, do_ncbi_lookup: bool = True, output_csv: str = None):
    """
    Parse the FASTA file and return a pandas DataFrame.
    If do_ncbi_lookup True, for each sequence header we try to fetch NCBI metadata (if accession found).
    """
    records = []
    for rec in SeqIO.parse(file_path, "fasta"):
        seq = str(rec.seq).upper()
        L = len(seq) if seq else 0
        gc_count = seq.count("G") + seq.count("C")
        at_count = seq.count("A") + seq.count("T")
        acc = extract_accession(rec.description)
        ncbi = fetch_ncbi_metadata(acc) if (do_ncbi_lookup and acc) else None
        row = {
            "id": rec.id,
            "description": rec.description,
            "length": L,
            "gc_percent": round((gc_count / L * 100), 2) if L else None,
            "at_percent": round((at_count / L * 100), 2) if L else None,
            "first_10": seq[:10],
            "last_10": seq[-10:],
            "accession_hint": acc,
        }
        if ncbi:
            row.update({
                "ncbi_db": ncbi.get("ncbi_db"),
                "ncbi_uid": ncbi.get("ncbi_uid"),
                "ncbi_title": ncbi.get("ncbi_title"),
                "ncbi_organism": ncbi.get("ncbi_organism"),
            })
        records.append(row)
    df = pd.DataFrame(records)
    if output_csv:
        df.to_csv(output_csv, index=False)
    return df
