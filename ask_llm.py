import os
import sys
import threading

try:
    import customtkinter as ctk
    from dotenv import load_dotenv
    from google import genai
except ImportError:
    print("Dependencies missing. Please run: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Check for API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "paste_your_key_here":
    print("Error: GEMINI_API_KEY is missing in .env file.")
    sys.exit(1)

# Initialize the Gemini Client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    print(f"Failed to initialize Gemini Client: {e}")
    sys.exit(1)

# Configure the window appearance to look modern
ctk.set_appearance_mode("System")  # Uses the user's system theme (dark/light)
ctk.set_default_color_theme("blue")

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Setup the main window
        self.title("Professional LLM Assistant")
        self.geometry("700x800")
        self.minsize(500, 600)

        # Chat history display area
        self.chat_display = ctk.CTkTextbox(
            self, 
            state="disabled", 
            wrap="word", 
            font=("Segoe UI", 15),
            fg_color=("gray95", "gray15") # Light mode / Dark mode colors
        )
        self.chat_display.pack(pady=20, padx=20, fill="both", expand=True)

        # Add a welcome message
        self.append_to_chat("Welcome to your Professional AI Assistant!", "System")
        self.append_to_chat("Note: If the response fails, Google's Free Tier servers might be experiencing high load.", "System")

        # Input frame at the bottom
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=(0, 20), padx=20, fill="x")

        # Text input field
        self.input_field = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Ask me anything...",
            font=("Segoe UI", 15),
            height=45
        )
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bind the Enter key to send the message
        self.input_field.bind("<Return>", self.send_message)

        # Send button
        self.send_button = ctk.CTkButton(
            self.input_frame, 
            text="Send", 
            command=self.send_message,
            font=("Segoe UI", 15, "bold"),
            width=100,
            height=45
        )
        self.send_button.pack(side="right")

    def append_to_chat(self, text, sender):
        """Helper to add text to the chat window AND print to console."""
        self.chat_display.configure(state="normal")
        
        # Fulfill the exact assignment requirement: "Prints the model's response to the console"
        # while also updating our beautiful GUI.
        if sender == "You":
            print(f"\nYou asked: {text}")
            self.chat_display.insert("end", f"👤 You:\n{text}\n\n")
        elif sender == "Gemini":
            print(f"\nModel's response:\n{text}\n")
            self.chat_display.insert("end", f"🤖 AI:\n{text}\n\n")
        else:
            print(f"\nSystem: {text}")
            self.chat_display.insert("end", f"⚙️ {text}\n\n")
            
        self.chat_display.see("end")  # Auto-scroll to bottom
        self.chat_display.configure(state="disabled")

    def send_message(self, event=None):
        """Triggered when the user clicks Send or hits Enter."""
        question = self.input_field.get().strip()
        if not question:
            return

        # Display the user's question
        self.append_to_chat(question, "You")
        self.input_field.delete(0, "end")
        
        # Disable input while waiting for the API
        self.input_field.configure(state="disabled")
        self.send_button.configure(state="disabled", text="Thinking...")
        
        # Run the API call in a background thread to prevent freezing the GUI
        threading.Thread(target=self.fetch_response, args=(question,), daemon=True).start()

    def fetch_response(self, question):
        """Calls the Gemini API in the background."""
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=question,
            )
            reply = response.text
        except Exception as e:
            error_msg = str(e)
            # Handle common Google Free Tier errors gracefully
            if "503" in error_msg:
                reply = "❌ Error: Google's servers are currently overloaded (503). Please wait a moment and try again."
            elif "429" in error_msg:
                reply = "❌ Error: API quota exceeded (429). Google might be limiting free tier usage."
            else:
                reply = f"❌ API Error: {error_msg}"

        # Safely update the GUI from the background thread
        self.after(0, self.update_gui_with_response, reply)

    def update_gui_with_response(self, reply):
        """Updates the chat window with the AI's response and re-enables inputs."""
        self.append_to_chat(reply, "Gemini")
        
        self.input_field.configure(state="normal")
        self.send_button.configure(state="normal", text="Send")
        self.input_field.focus()

if __name__ == "__main__":
    print("Starting Professional LLM Assistant...")
    print("Close the desktop application window to exit.")
    app = ChatApp()
    app.mainloop()
