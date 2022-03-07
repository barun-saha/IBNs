# NLU Model for IBNs


This repository contains a synthetically generated dataset to train a Natural Language Understanding (NLU) model for developing Intent-based Networks (IBNs). A set of sample intents that capture some common network operations, such as creation of a flow between two endpoints, are provided. The intents are expressed in English. Relevant network entities, such as IP address, are also annotated in the text.

The NLU model is trained using [Rasa](https://rasa.com/) (version 2.8). The training configuration file is also provided. Once an NLU model has been trained, it can be used to identify the intent and entities from a given English sentence. The recognized intent provides an indication of what action needs to be triggered in the IBN.


The scope of the NLU model can be further extended by adding more network intents and annotated examples. 

If you are using the NLU dataset for IBNs, please consider citing this repository.