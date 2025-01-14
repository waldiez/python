# Import the generate_sequence_diagram function from the generate_diagram module
from gen_seq_diagram import generate_sequence_diagram

# Specify the path to the input CSV file
file_path = 'waldiez_out/20250114113129/logs/events.csv'

# Optionally, specify the output path for the Mermaid diagram
output_path = 'output_sequence_diagram.mmd'

# Call the function to generate the sequence diagram
generate_sequence_diagram(file_path, output_path)