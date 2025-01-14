import pandas as pd
import json

# Function to escape newlines in text for Mermaid diagram
def escape_mermaid_text(text):
    """Replace newline characters with <br/> for Mermaid compatibility."""
    return text.replace("\n", "<br/>")

# Constants for the sequence diagram initialization
SEQ_TXT = """
%%{init: {'sequence': {'actorSpacing': 10, 'width': 150}}}%%
sequenceDiagram
"""

def process_events(df_events):
    """Process the events DataFrame and generate a Mermaid sequence diagram text."""
    
    # Set to store participants (senders and recipients)
    participants = set()

    # Initialize the sequence diagram text
    seq_text = SEQ_TXT

    # Loop through each event in the DataFrame
    for i in range(len(df_events['json_state'])):
        # Parse the JSON state of the event
        df_j = json.loads(df_events['json_state'][i])

        # Skip events that are not relevant (e.g., replies or missing messages)
        if ('message' in df_j.keys()) and (df_events['event_name'][i] != 'reply_func_executed'):
            
            sender = df_j['sender']
            recipient = df_events['source_name'][i]

            # Extract message content if available
            if "content" in str(df_j['message']):
                message = "Content: " + str(df_j['message']["content"])
            else:
                message = df_j['message']
            
            # Escape the message for Mermaid compatibility and truncate long messages
            message = escape_mermaid_text(message)
            max_len = 100
            if len(message) > max_len:
                message = message[:max_len] + '...'

            # Add sender and recipient to participants set
            participants.add(recipient)
            participants.add(sender)

            # Split message into main message and context if "Content" is present
            if "Content: " in message:
                message_parts = message.split("Content: ")
                main_message = message_parts[0].strip()
                context = "Content: " + message_parts[1].strip()
                seq_text += f"    {sender}->>{recipient}: {main_message}\n"
                seq_text += f"    note over {recipient}: {context}\n"
            else:
                seq_text += f"    {sender}->>{recipient}: {message}\n"

    # Add participants to the Mermaid diagram
    participants_text = ""
    for participant in participants:
        alias = "".join(word.capitalize() for word in participant.split("_"))
        participants_text += f"    participant {participant} as {participant.replace('_', ' ').title()}\n"
    
    # Prepend the participants to the sequence diagram text
    mermaid_text = SEQ_TXT + participants_text + seq_text[len(SEQ_TXT):]

    return mermaid_text

def save_diagram(mermaid_text, output_path="sequence_diagram.mmd"):
    """Save the Mermaid diagram to a .mmd file."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(mermaid_text)

def generate_sequence_diagram(file_path, output_path="sequence_diagram.mmd"):
    """Main function to generate the Mermaid diagram."""
    # Load the events data from the CSV file
    df_events = pd.read_csv(file_path)

    # Generate the Mermaid sequence diagram text
    mermaid_text = process_events(df_events)

    # Save the Mermaid diagram to a file
    save_diagram(mermaid_text, output_path)

    print(f"Sequence diagram has been successfully generated and saved to '{output_path}'.")

