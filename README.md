# **JARVIS**
Jarvis is an AI voice agent which has func call ability and speak Turkish.

# Turkish AI Assistant with Speech and Functionality Integration

## Overview

There is 2 versions in this repository one of them is using ChatGPT and the other is LLama. ChatGPT version is more advenced and well developed than LLama version. Llama version is just a template for how to build your own AI Voice Agent. You can add your own funcs and customize them.


## ChatGPT Version
This project is a Python-based Turkish AI Assistant "Jarvis", that integrates various advanced functionalities including taking screenshot, capturing a webcam photo, extracting user's clipboard, opening programs which user will configure in the func and opening websites. The assistant can interact with the user via voice commands, take screenshots, analyze webcam images, open programs and websites, and much more. 

It leverages several powerful AI APIs and libraries such as OpenAI, Google Cloud Text-to-Speech, and Gemini, making it capable of handling both textual and visual inputs. The assistant's flexibility allows users to control their system, interact with websites, and even analyze images based on their spoken commands.

## Features

### 1. **Voice Recognition and Speech Output**
   - The assistant listens for a predefined wake word to become active. Default value for the wake word is ("Jarvis").
   - It uses Google’s Speech-to-Text API to process user commands and OpenAI’s GPT models to provide intelligent responses.
   - Text-to-Speech functionality is provided through Google Cloud's Text-to-Speech API, allowing the assistant to speak back in a natural-sounding voice.

### 2. **Image Analysis**
   - The assistant can take screenshots of the user's screen or capture images via the webcam.
   - These images can then be analyzed to extract relevant information or contextual data, providing a visual understanding to complement text-based interactions.

### 3. **Functionality and Automation**
   - The assistant can perform various tasks like opening programs (e.g., games, browsers), extracting clipboard content, or even opening websites based on user's voice input.
   - A function call handler intelligently determines what action to take based on the user's voice command.

### 4. **Customizable Configuration**
   - The assistant is highly configurable with adjustable settings for temperature, response length, and safety filters.
   - Integrates with multiple APIs including OpenAI's GPT model and Google's Gemini for generative tasks, ensuring high-quality conversational AI interactions.

## How It Works

### 1. Voice Recognition:

  - The assistant uses Google’s Speech-to-Text API to continuously listen for the wake word.
  - Once the wake word "Jarvis" (It is recommended to change the wake word in case of using Turkish speech recognition ) is detected, it becomes active and listens for the user's command.
### 2. Function Handling:

  - Based on the user's spoken input, the assistant calls the appropriate function (e.g., taking a screenshot, opening a program, or capturing webcam images).

### 3. Text & Voice Interaction:

  - The assistant generates a response using OpenAI’s GPT-3.5, and the response is then converted to speech using Google Cloud Text-to-Speech API.

### 4. Image Analysis:

  - The assistant can analyze screenshots and webcam images, using AI models to extract relevant visual information and respond accordingly.
    

## Example Commands
   
### First say the wake word and wait for the response. Then, tell what do you want to do. These commands are just examples of usage. User can use similar voice commands.
  - STDIN "Jarvis"
  - STDOUT "Efendim"
  - STDIN "Ekranıma bak" takes screenshot and analyzes it.
  - STDIN "Jarvis"
  - STDOUT "Efendim"
  - STDIN "Kamerama bak" captures a webcam photo and analyzes it.
  - STDIN "Jarvis"
  - STDOUT "Efendim"
  - STDIN "Spotify'ı aç." opens Spotify. ( You should set the keywords and paths for each app in the open_any_program() func. ).
  - STDIN "Jarvis"
  - STDOUT "Efendim"
  - STDIN "Youtube'u aç." opens Youtube on browser. 

## Contributions

Feel free to fork this repository, create issues, and contribute to its improvement. Contributions are always welcome!


## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- API keys for:
  - OpenAI GPT-3.5 for ChatGPT version
  - Groq for LLama version
  - Google Cloud Text-to-Speech API
  - Gemini Generative AI
- Required libraries and dependencies

### Installing Dependencies
To set up the environment, first create a virtual environment and activate it. Then, install the necessary Python packages.

```bash
# Create a virtual environment (optional but recommended)
python -m venv Jarvis
# Activate the environment
# For Windows
Jarvis\Scripts\activate
# For macOS/Linux
source Jarvis/bin/activate

# Install required packages
pip install -r requirements.txt
