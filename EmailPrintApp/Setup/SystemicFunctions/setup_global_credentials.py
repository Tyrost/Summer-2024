import tkinter as tk

class PlaceholderTextEditor:
    def __init__(self, window, placeholder_text, width, height, font):

        self.window = window
        self.placeholder_text = placeholder_text
        self.font = font
        self.current_text = ''
        
        self.text_editor = tk.Text(window, font=font, width=width, height=height, wrap='word')
        
        self.text_editor.insert('1.0', placeholder_text)
        self.text_editor.config(fg='grey')
        
        self.text_editor.bind('<FocusIn>', self.remove_placeholder)
        self.text_editor.bind('<FocusOut>', self.add_placeholder)
        self.text_editor.bind('<Return>', self.return_pressed)
        self.text_editor.bind('<Escape>', self.escape_pressed)

    def remove_placeholder(self, event):
        if self.text_editor.get('1.0', 'end-1c') == self.placeholder_text:
            self.text_editor.delete('1.0', 'end')
            self.text_editor.config(fg='black')
    
    def add_placeholder(self, event):
        if not self.text_editor.get('1.0', 'end-1c'):
            self.text_editor.insert('1.0', self.placeholder_text)
            self.text_editor.config(fg='grey')
    
    def return_pressed(self, event):
        current_text = self.text_editor.get('1.0', 'end-1c').strip()
        if current_text and current_text != self.placeholder_text:
            print(f"Text Submitted: {current_text}")
            self.current_text = current_text
            self.show_temporary_placeholder(f"{self.placeholder_text.split()[0]} Set")
        self.stop_editing()
        return 'break'
    
    def escape_pressed(self, event):
        self.text_editor.delete('1.0', 'end')
        self.text_editor.insert('1.0', self.placeholder_text)
        self.text_editor.config(fg='grey')
        self.stop_editing()
        return 'break'
    
    def update_current_text(self, event):
        self.current_text = self.text_editor.get('1.0', 'end-1c').strip()
        if self.current_text == self.placeholder_text:
            self.current_text = ''
    
    def get_text(self):
        return self.current_text
    
    def show_temporary_placeholder(self, temp_text):
        self.text_editor.delete('1.0', 'end')
        self.text_editor.insert('1.0', temp_text)
        self.text_editor.config(fg='grey')
        
        def reset_placeholder():
            self.text_editor.delete('1.0', 'end')
            self.text_editor.insert('1.0', self.placeholder_text)
            self.text_editor.config(fg='grey')
        
        self.window.after(5000, reset_placeholder)
    
    def stop_editing(self):
        self.text_editor.config(state='disabled')
        self.window.focus_set()  # Remove focus from the text editor
        
        def enable_editing():
            self.text_editor.config(state='normal')
        
        # Re-enable editing after a short delay
        self.window.after(100, enable_editing)