import sys
import os

def add_m_to_sequences(input_fasta, output_fasta):
    # Crear el archivo de salida si no existe
    if not os.path.exists(output_fasta):
        open(output_fasta, 'w').close()

    with open(input_fasta, 'r') as infile, open(output_fasta, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                outfile.write(line)
            else:
                sequence = line.strip()
                if not sequence.startswith('M'):
                    sequence = 'M' + sequence
                outfile.write(sequence + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dataset-M-adder.py <input_fasta> <output_fasta>")
        sys.exit(1)

    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
    add_m_to_sequences(input_fasta, output_fasta)