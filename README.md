# Voiceprint-Identification
Voiceprint Identification for QMIND

## Usage

### GUI
The GUI is Tkinter-based for real time classification. 
![image](https://user-images.githubusercontent.com/65412039/111880975-be84e180-8984-11eb-8b48-c8d314fd8c11.png)
#### Add a User Profile
Add a user profile by simply typing the user name and pressing the *Add User* button. The GUI will then guide you through the process of adding a user by prompting you to say a couple sentences and recording your data. Thats it! 

step 1.


### Model

The word model trains a keras sequential on files in the 'words' folder. To train a model on audio data, use file structure words/'word'/'name'/'file'.wav (ex words/the/john/1.wav) and call word model as follows
```python
words = ["alexa","the", "be", "to", "of", "and"]
model = word_model(words)
```
this should output

Epoch 1/50
5/5 [==============================] - 0s 63ms/step - loss: 1.7061 - accuracy: 0.3459 - val_loss: 0.7850 - val_accuracy: 0.8491  
.  
.  
.  
Epoch 50/50
5/5 [==============================] - 0s 33ms/step - loss: 0.0259 - accuracy: 0.9937 - val_loss: 0.0223 - val_accuracy: 0.9811  
  
and make predictions by calling *predict_speaker*
```python
name, confidence = predict_speaker("test/eli.wav", model)
# 'eli', .9099897
```
this outputs the name and confidence, 
