import cv2
import json
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

def get_prediction(cv2_image):
    # Define your model architecture
    IMG_SIZE=48
    input_layer = Input(shape=(IMG_SIZE, IMG_SIZE, 1))
    base_model = Sequential()

    # Conv layer 1
    x = Conv2D(32, kernel_size=(3, 3), activation='relu')(input_layer)
    x = BatchNormalization()(x)
    x = Dropout(0.25)(x)

    # Conv layer 2
    x = Conv2D(64, kernel_size=(3, 3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.25)(x)

    # Conv layer 3
    x = Conv2D(128, kernel_size=(3, 3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Dropout(0.25)(x)

    x = Flatten()(x)

    # Dense layer 1
    x = Dense(128, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)

    output_layer = Dense(6, activation='softmax')(x)

    model = Model(inputs=input_layer, outputs=output_layer)

    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

    # Load the pre-trained weights
    model.load_weights('scripts/engagement_model_weights.h5')

    # Load and preprocess an example image
    # img_array = cv2.resize(cv2_image, (IMG_SIZE, IMG_SIZE))
    # img_array = img_array.reshape((1, IMG_SIZE, IMG_SIZE, 1))
    img_array = cv2_image
    img_array = img_array / 255.0

    # Display the processed image
    # plt.subplot(1, 2, 2)
    # plt.imshow(img_array[0, :, :, 0], cmap='gray')  # Access the first (and only) image in the batch
    # plt.title('Processed Image')
    #
    # plt.show()

    # Make predictions
    predictions = model.predict(img_array)

    class_labels = ['looking away', 'bored', 'confused', 'drowsy', 'engaged', 'frustrated']

    # Get the index of the maximum value in predictions
    predicted_class_index = np.argmax(predictions)

    # Get the corresponding class label
    predicted_class_label = class_labels[predicted_class_index]

    # print('Predicted Class Label:', predicted_class_label)
    # print('Predictions:', predictions)
    response = {class_labels[i]: float(predictions[0][i]) for i in range(len(class_labels))}
    return response

if __name__ == '__main__':
    quit(-1)
    # image_path = 'bored.jpg'
    # cv2_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # get_prediction(cv2_image)