import logging
import argparse

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def join_fasta_files(output_file: str, input_files: list):
    sequence_counter = 0
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                for line in infile:
                    if line.startswith('>'):
                        outfile.write(f'>seq_{sequence_counter}\n')
                        sequence_counter += 1
                    else:
                        #sequence = '\n'.join(sequence[i:i+60] for i in range(0, len(sequence), 60))
                        outfile.write(line)
    return sequence_counter

def main(args):
    input_list = args.input_files.split(',')
    logger.info(f"Número de archivos a unir: {len(input_list)}.")

    total_seqs = join_fasta_files(args.output_file, input_list)
    logger.info(f"{total_seqs} secuencias escritas en el archivo de salida.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Join multiple FASTA files into one.")
    parser.add_argument('--output_file', type=str, help='The output FASTA file.')
    parser.add_argument('--input_files', type=str, help='The input FASTA files to be joined, separated by a comma.')
    args = parser.parse_args()

    main(args)
    logger.info("FIN.")