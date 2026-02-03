#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
import pandas as pd
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input, ResNet50
from tensorflow.keras.models import Model

base_model = ResNet50(weights='imagenet')
model = Model(inputs=base_model.inputs, outputs=base_model.layers[-2].output)

num_features = model.output_shape[-1]

images_folder_path = r"C:\Users\2raun\Desktop\New Dataset Final\Final Images 4"

column_names = ['image_name'] + [f'feature_{i}' for i in range(num_features)]

df_header = pd.DataFrame(columns=column_names)

csv_path = r"C:\Users\2raun\Desktop\New Dataset Final\Final\resnet_emb.csv"
df_header.to_csv(csv_path, index=False)

def extract_features(folder_path):
    for img_file in os.listdir(folder_path):
        img_file_path = os.path.join(folder_path, img_file)
        if img_file.lower().endswith(('.jpg', '.jpeg', '.webp', '.png')):
            try:
                image_name = os.path.basename(img_file_path)  # Get the image file name
                image = load_img(img_file_path, target_size=(224, 224))
                image = img_to_array(image)
                image = preprocess_input(image)
                features = model.predict(image.reshape((1, image.shape[0], image.shape[1], image.shape[2])))
                df_of_features = pd.DataFrame(features, columns=[f'feature_{i}' for i in range(num_features)])
                df_of_features.insert(0, 'image_name', image_name)  # Insert image name column
                df_of_features.to_csv(csv_path, index=False, header=False, mode='a')
            except Exception as e:
                print(f"Error processing {img_file_path}: {e}")

extract_features(images_folder_path)

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

csv_file_path = r"C:\Users\2raun\Desktop\New Dataset Final\Final\resnet_emb.csv"
df = pd.read_csv(csv_file_path)

image_names = df.iloc[:, 0].values

resnet_features = df.iloc[:, 1:].values


pca_resnet = PCA(n_components=768)  


print("\nApplying PCA to ResNet Embeddings...")
resnet_reduced = pca_resnet.fit_transform(resnet_features)
print("ResNet Embeddings after PCA shape:", resnet_reduced.shape)
print(resnet_reduced)


reduced_df = pd.DataFrame(resnet_reduced)
reduced_df.insert(0, 'ImageName', image_names)


reduced_csv_file_path =  r"C:\Users\2raun\Desktop\New Dataset Final\Final\pca_resnet_emb.csv"
reduced_df.to_csv(reduced_csv_file_path, index=False)

print(f"Reduced ResNet embeddings saved to {reduced_csv_file_path}")

