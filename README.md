# 🤖 Professional LLM Desktop Assistant

![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-purple.svg)

---

## 📌 What This Script Does

This project is a desktop application that allows a user to chat with a Large Language Model (LLM). 
Specifically, the script (`ask_llm.py`):
1. **Takes a user's question as text input** via a modern Graphical User Interface (GUI).
2. **Sends that input** asynchronously to the chosen LLM API.
3. **Prints the model's response** directly into the beautiful chat display window.

In addition to the core requirements, it features **background thread processing** (so the UI never freezes while waiting for the network) and **graceful error handling** (catching common server issues without crashing).

---

## 🧠 Which LLM API Was Used and Why

This application uses the **Google Gemini API** (specifically the `gemini-2.5-flash` model via the `google-genai` SDK).

**Why it was chosen:**
1. **Generous Free Tier:** Google provides a highly capable free tier, making it the perfect choice for academic and development assignments without requiring a credit card or incurring unexpected costs.
2. **Speed & Capability:** The `gemini-2.5-flash` model offers exceptionally fast response times, which is critical for providing a smooth, responsive user experience in a GUI chat application.
3. **Modern Tooling:** The new official `google-genai` Python library is lightweight, modern, and easy to integrate securely.

---

## 🚀 Step-by-Step Instructions to Set Up and Run Locally

### Step 1: Install Prerequisites
1. Ensure you have **Python 3.9 or higher** installed on your machine.
2. Get a free API key from [Google AI Studio](https://aistudio.google.com/).

### Step 2: Install Project Dependencies
Open your terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Your API Key
For security best practices, this project uses a `.env` file instead of hardcoded keys.
1. Copy the provided `.env.example` file and rename it to `.env`:
   - **Windows:** `copy .env.example .env`
   - **Mac/Linux:** `cp .env.example .env`
2. Open the `.env` file in a text editor.
3. Replace the placeholder text with your actual Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   ```

### Step 4: Run the Application
In your terminal, start the program by running:
```bash
python ask_llm.py
```
A desktop window will appear. Simply type your question in the bottom input field, hit **Enter** (or click **Send**), and the model's response will print to the console window!

---

## 📁 Project Structure

| File | Description |
| :--- | :--- |
| `ask_llm.py` | The main application script containing the UI and threading logic. |
| `requirements.txt` | The Python dependencies required to run the project. |
| `.env.example` | A template for securely storing environment variables. |
| `.env` | *(Created during setup)* Your local file containing your secret API key. |
| `README.md` | This documentation file. |
