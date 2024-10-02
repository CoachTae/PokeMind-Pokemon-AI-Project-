import json
import sys
import torch
import torch.nn as nn

class EmbeddingModel(nn.Module):
    '''
    initial_categories: Number of categories (rows) to initialize the matrix with.

    embedding_dim: Number of values to be given to each category (for the system to learn)
    '''
    def __init__(self, initial_categories=10, embedding_dim=10):
        super(EmbeddingModel, self).__init__()
        
        # Initialize embedding layer with some initial capacity
        self.embedding = nn.Embedding(initial_categories, embedding_dim)
        
        # Dictionary to track categories and their assigned indices
        self.category_to_index = {}
        self.num_categories = initial_categories
        self.embedding_dim = embedding_dim
    
    def add_category(self, category):
        # Add a new category if it's not already in the dictionary
        if category not in self.category_to_index:
            # Assign the next available index to this category
            self.category_to_index[category] = len(self.category_to_index)
            
            # If the embedding matrix is full, we need to expand it
            if self.category_to_index[category] >= self.num_categories:
                self.expand_embedding_matrix()
    
    def expand_embedding_matrix(self):
        # Create a new embedding matrix with additional capacity
        new_embedding = nn.Embedding(self.num_categories + 10, self.embedding_dim)
        
        # Copy the learned weights from the old embedding to the new one
        with torch.no_grad():
            new_embedding.weight[:self.num_categories] = self.embedding.weight
        
        # Replace the old embedding with the new, larger one
        self.embedding = new_embedding
        self.num_categories += 10  # Increase capacity by 10
    
    def forward(self, category):
        # Look up the category index in the dictionary
        category_index = torch.tensor([self.category_to_index[category]], dtype=torch.long)
        
        # Pass the index to the embedding layer to get the embedding vector
        return self.embedding(category_index)

emb_index_map = {"Sprite ID": {},
                 "Face Direction": {},
                 "Item ID": {},
                 "Menu Type": {},
                 "Move ID": {},
                 "Effect": {},
                 "Type": {},
                 "Pokemon ID": {},
                 "Status": {},
                 "Battle Type": {},
                 "Type of Battle": {},  # Not sure the diff between this and the one above. Check Battle.py for more notes.
                 "Crit Flag": {},
                 "Map ID": {},
                 "Flags": {},
              }

with open('Embedding Map.json', 'w') as file:
    json.dump(emb_index_map, file, indent=4)
