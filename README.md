# MyOnlineAssistant-API

Chatbot API Service - Cheri

What she can do:
Answer user's questions, change emotions based on questions and perform some functions.
First time I did it by Django, after that I converted it to API service by Flask.

- Use Natural Language Toolkit (nltk) to handle text.
- Use Standford library to grab a personal name and organization.
- Use Machine Learning to understand meanings. Algorithm:
Input -> 128 dots, activation: ReLU -> Dropout(0.5) -> 64 dots, activation: ReLU -> Dropout(0.5) -> Output, activation: Softmax

Note: Check develop branch for the newest code (TensorFlow 2.1)
