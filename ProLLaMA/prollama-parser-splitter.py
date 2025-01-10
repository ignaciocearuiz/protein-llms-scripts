import random as rd
import json
import os
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def fastaReader(input_fasta: str):
    with open(input_fasta, 'r') as input:
        # Create variables for storing identifiers and sequence
        sequence = ""
        first_line = True
        
        for line in input:
            if line.startswith('>'):
                if first_line:
                    # This only happens when the first line of the FASTA file is parsed.
                    first_line = False
                    continue
                else:
                    # This happens every time a new FASTA record is encountered.
                    # Start by yielding the entry that has been built up.
                    yield sequence

                    # Then reinitialise the sequence variable to build up a new record.
                    sequence = ""
            else:
                # This happens every time a sequence line is encountered.
                sequence += line.replace("\n", "")
        # Yields the last sequence
        yield sequence

def outputJSONFiles(train_list, test_list, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    json_train_data = json.dumps(train_list, indent=4)
    with open(f"{output_dir}/train_split.json", 'w') as output_train:
        output_train.write(json_train_data)
    
    # Solo genera el archivo JSON si hay secuencias para testeo.
    if len(test_list) != 0:
        json_test_data = json.dumps(test_list)
        with open(f"{output_dir}/test_split.json", 'w') as output_test:
            output_test.write(json_test_data)

def main(args):
    sequences = []
    for seq in fastaReader(args.input_fasta):
        data = dict()
        data["instruction"] = "[Generate by protein family]"
        data["input"] = f"Family=<{args.family_name} family>"
        data["output"] = f'Seq=<{seq}>'
        sequences.append(data)

    total_seqs = len(sequences)
    logger.info(f"Nombre familia: {args.family_name}")
    logger.info(f"Total secuencias leídas: {total_seqs}")

    train_size = round(len(sequences) * args.train_ratio)
    train_sequences = []

    # Al final de este ciclo, sequences tendrá solamente las secuencias destinadas a test.
    for _ in range(train_size):
        rand_index = rd.randint(0, total_seqs-1)
        train_sequences.append(sequences.pop(rand_index))
        total_seqs -= 1
    logger.info(f"Secuencias para training: {len(train_sequences)}")
    logger.info(f"Secuencias para testing: {len(sequences)}")
    
    outputJSONFiles(train_sequences, sequences, args.output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_fasta", type=str)
    parser.add_argument("--family_name", type=str)
    parser.add_argument("--output_dir", type=str, default="prollama-data")
    parser.add_argument("--train_ratio", type=float, default=0.9)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    main(args)
    logger.info("Parseo finalizado.")