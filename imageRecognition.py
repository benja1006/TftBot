import numpy as np
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras import layers
from keras.constraints import maxnorm
from keras.utils import np_utils
import os
import sys
import matplotlib.pyplot as plt

seed = 35
batch_size = 64
img_height = 188
img_width = 257

# import data from folders
(champ_train, champ_test) = keras.utils.image_dataset_from_directory(
    directory='champs',
    labels='inferred',
    image_size=(257, 188),
    seed=seed,
    validation_split=.2,
    subset="both",
    batch_size=batch_size
)

champ_names = champ_train.class_names

# prints a sample of the dataset
plt.figure(figsize=(10,10))
for champs, labels in champ_train.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(champs[i].numpy().astype("uint8"))
        plt.title(champ_names[labels[i]])
        plt.axis("off")
plt.show()

# prints the shape of the dataset
for image_batch, labels_batch in champ_train:
  print(image_batch.shape)
  print(labels_batch.shape)


# configuring dataset for performance
AUTOTUNE = tf.data.AUTOTUNE

# cache the dataset so that HD isn't a bottleneck
champ_train = champ_train.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
champ_test = champ_test.cache().prefetch(buffer_size=AUTOTUNE)

# rescale the images RGB values to be between 0 and 1
normalization_layer = keras.layers.Rescaling(1./255)

normalized_ds = champ_train.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))


# create model

num_classes = len(champ_names)


model = keras.Sequential([
  layers.Rescaling(1./255, input_shape=(img_width, img_height, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])
# compile model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# summerize model
model.summary()

# train the model

epochs=100

history = model.fit(
  champ_train,
  validation_data=champ_test,
  epochs=epochs
)

# visualize the

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
model.save(os.path.join(os.getcwd(), 'my_model'))
