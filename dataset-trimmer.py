import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

## SCRIPT PARA DISMINUIR EL TAMAÑO DE UN CONJUNTO DE SECUENCIAS EN FORMATO FASTA

def fastaReader(input_fasta: str):
    with open(input_fasta, 'r') as input:
        # Create variables for storing identifiers and sequence
        identifier = None
        sequence = []
        
        for line in input:
            line = line.strip()
            if line.startswith('>'):
                if identifier is None:
                    # This only happens when the first line of the FASTA file is parsed.
                    identifier = line
                else:
                    # This happens every time a new FASTA record is encountered.
                    # Start by yielding the entry that has been built up.
                    yield identifier, sequence

                    # Then reinitialise the sequence variable to build up a new record.
                    identifier = line
                    sequence = []
            else:
                # This happens every time a sequence line is encountered.
                sequence.append(line)
        # Yields the last record
        yield identifier, sequence

def outputFastaFile(sequences, output_fasta):
    with open(output_fasta, 'w') as output:
        for id, seq in sequences:
            output.write(id+'\n')
            output.write("\n".join(seq)+'\n')

def main(args):
    sequences = set()
    for id, seq in fastaReader(args.input_fasta):
        sequences.add((id, tuple(seq)))
    total_seqs = len(sequences)
    logger.info(f"Total secuencias leídas: {total_seqs}")

    for i in range(total_seqs - args.new_size):
        sequences.pop()
    logger.info(f"Almacenando {len(sequences)} secuencias aleatorias en {args.output_fasta}...")
    outputFastaFile(sequences, args.output_fasta)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_fasta", type=str)
    parser.add_argument("--new_size", type=int)
    parser.add_argument("--output_fasta", type=str)
    args = parser.parse_args()

    main(args)
    logger.info("END")