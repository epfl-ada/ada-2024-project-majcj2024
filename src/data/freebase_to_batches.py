# .py file used to save a .txt files with freebase IDs to then execute a SPARQL request on query.wikidata.org
import pandas as pd
import os

# data path
DATA = './data/'

# charcaters metadata loading
df_characters = pd.read_csv(DATA + 'character.metadata.tsv', sep='\t', header=None)
df_characters.columns = ['wikipedia_id', 'freebase_id', 'release_date', 'character_name', 'actor_birth',
                     'actor_gender', 'actor_height', 'actor_ethnicity', 'actor_name', 
                     'age_at_release', 'freebase_map', 'freebase_character_id', 'freebase_actor_id']

# collecting unique ethnicty freebase IDs into batches as query have limited processing limit
unique_ethnicities = df_characters['actor_ethnicity'].dropna().unique().tolist()
batch_size = 50

# defining path for the output file as the same where this .py file is saved
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file_path = os.path.join(script_dir, "unique_actor_ethnicities_batches.txt")

# writing unique_ethnicities into a .txt file
with open(output_file_path, "w") as file:
    for i in range(0, len(unique_ethnicities), batch_size):
        batch = unique_ethnicities[i:i+batch_size]
        formatted_batch = " ".join(f'"{id}"' for id in batch)
        
        # writing the formatted batch to the file with a separator
        file.write(f"Batch {i//batch_size + 1}:\n")
        file.write(formatted_batch + "\n\n" + "-"*50 + "\n\n")
    
print(f"Batches of unique, not-nan Freebase IDs have been saved to '{output_file_path}'")