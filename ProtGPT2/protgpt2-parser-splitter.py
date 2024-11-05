import random as rd
import sys
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
                sequence += line
        # Yields the last sequence
        yield sequence

def outputFastaFiles(train_list, test_list, output_dir):
    with open(f"{output_dir}/train.txt", 'w') as output_train:
        for seq in train_list:
            output_train.write("<|endoftext|>\n" + seq)
    with open(f"{output_dir}/test.txt", 'w') as output_test:
        for seq in test_list:
            output_test.write("<|endoftext|>\n" + seq)

def main(args):
    """if len(sys.argv) != 3:
        print("Usage: python protgpt2-parser-splitter.py <input_fasta> <output_dir>")
        return"""

    """input_fasta = sys.argv[1]
    output_dir = sys.argv[2]"""

    sequences = []
    for seq in fastaReader(args.input_fasta):
        sequences.append(seq)
    total_seqs = len(sequences)
    #print("Total secuencias:", total_seqs)
    logger.info(f"Total secuencias leídas: {total_seqs}")

    train_size = round(len(sequences) * args.train_ratio)
    train_sequences = []
    rd.seed(args.seed)

    # Al final de este ciclo, sequences tendrá solamente las secuencias destinadas a test.
    for _ in range(train_size):
        rand_index = rd.randint(0, total_seqs-1)
        train_sequences.append(sequences.pop(rand_index))
        total_seqs -= 1
    """print("Secuencias para training:", len(train_sequences))
    print("Secuencias para testing:", len(sequences))
    print("Generando archivos FASTA para ProtGPT2 ...")"""
    logger.info(f"Secuencias para entrenamiento: {len(train_sequences)}")
    logger.info(f"Secuencias para validación: {len(sequences)}")
    outputFastaFiles(train_sequences, sequences, args.output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_fasta", type=str)
    parser.add_argument("--output_dir", type=str, default="protgpt2-data")
    parser.add_argument("--train_ratio", type=float, default=0.9)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    main(args)
    logger.info("Parseo finalizado.")