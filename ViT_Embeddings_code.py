#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import concurrent.futures
import csv
import os
import torch
from transformers import ViTFeatureExtractor, ViTModel
from PIL import Image

model_name = 'google/vit-base-patch16-224'
feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)
model = ViTModel.from_pretrained(model_name)

def get_image_embeddings(image_path):
    
    image = Image.open(image_path).convert('RGB')
    inputs = feature_extractor(images=image, return_tensors="pt")

   
    with torch.no_grad():
        outputs = model(**inputs)

    
    embeddings = outputs.last_hidden_state.squeeze(0).mean(dim=0)

    return embeddings

def process_image_and_return(filename):
    image_path = os.path.join(folder_path, filename)
    embeddings = get_image_embeddings(image_path)
    return filename, embeddings

folder_path = "/content/drive/MyDrive/Dataset New/Final Images Used/Final Images 4"

image_filenames = [filename for filename in os.listdir(folder_path) if filename.endswith(('.png', '.jpg', '.jpeg','.webp'))]

with concurrent.futures.ThreadPoolExecutor() as executor:
    embeddings_list = list(executor.map(process_image_and_return, image_filenames))
    print(f"Processed {len(embeddings_list)} images")

csv_file = 'ViT image embeddings.csv'

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['filename', 'embedding'])
    for filename, embedding in embeddings_list:
        writer.writerow([filename, embedding.tolist()])

print(f"Embeddings saved to {csv_file}")

