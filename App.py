import os
import re
import base64
import markdown
from flask import Flask, render_template, request, send_file
from pygments import highlight  # Added import for Pygments
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

app = Flask(__name__)


def is_directory_empty(directory_path):
    try:
        # Check if the directory is empty by listing its contents
        if os.listdir(directory_path):
            print(f"The directory '{directory_path}' is not empty.")
            return False
        else:
            print(f"The directory '{directory_path}' is empty.")
            return True
    except OSError as e:
        print(f"An error occurred: {e}")
        return False


def _openDir(path):
    current_dir = path
    entries = os.listdir(current_dir)
    
    entry_details = []
    for entry in entries:
        entry_dict = {}
        entry_dict["name"] = entry

        full_path = os.path.join(current_dir, entry)
        if os.path.isfile(full_path):
            entry_dict["type"] = "file"
            file_size_bytes = os.path.getsize(full_path)
            file_size_kb = file_size_bytes / 1024.0 
            entry_dict["size"] = "{:.2f} KB".format(file_size_kb)
        else:
            entry_dict["type"] = "directory"
            entry_dict["size"] = "empty" if  is_directory_empty(full_path) else ""
        
        entry_details.append(entry_dict)

    return entry_details

""" @app.route('/save')
def saveToFile():
    # Perform actions for button 1
    # Add your logic here
    return "Save Button was clicked"
 """
""" @app.route('/button1')
def button1():
    # Perform actions for button 1
    # Add your logic here
    return "Button 1 was clicked"

@app.route('/button2')
def button2():
    # Perform actions for button 2
    # Add your logic here
    return "Button 2 was clicked" """

@app.route('/handle_text_edit_button_click/<button_text>', methods=['POST'])
def handle_text_edit_button_click(button_text):
    if request.method == 'POST':
        try:
            # Get the file content from the payload
            payload = request.get_json()
            file_content = payload.get('file_content')
            path = payload.get('file_path')
            
            # Process the file content and button text as needed
            # For demonstration purposes, just printing the received data
            print(f"Received Button Text: {button_text}")
            print(f"Received File Content: {file_content}")
            print(f"Received Path: {path}")
            with open(path, "w", encoding='utf-8') as f:
                f.write(file_content)

            # Add your logic here to handle the received data

            return "Data received successfully"  # Return a response as needed
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "Invalid request method"

@app.route('/handle_button_click/<entry_name>', methods=['POST'])
def handle_button_click(entry_name):
    if request.method == 'POST':
        try:
            # Get the file content from the payload
            payload = request.get_json()
            input_path = payload.get('file_path')
            # Process the entry_name from the button click
            # You can use entry_name to perform specific actions
            # Example: return some data or perform some operation
            # Remove the surrounding single quotes
            input_path = input_path.strip("'")

            # Split the path by the directory separator '\\'
            path_parts = input_path.split('\\')

            # Join all parts except the last one to get the remaining part
            global current_dir 
            current_dir = '\\'.join(path_parts[:-1]) + '\\'
            #print(f"Button for {entry_name} was clicked.")
            #return f"Button for {entry_name} was clicked."
            entry_details = _openDir(current_dir)

            return render_template("index.html", entries=entry_details)
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "Invalid request method"

@app.route('/process_text', methods=['POST'])
def process_text():
    user_text = request.form['user_text']
    # Perform actions with the user_text data (e.g., print it)
    print("User input:", user_text)
    global current_dir 
    current_dir = user_text
    entry_details = _openDir(current_dir)

    return render_template("index.html", entries=entry_details, current_dir=current_dir)


@app.route("/")
def index():
    global current_dir 
    current_dir = os.getcwd()
    current_dir = r'C:\Users\bened\Documents\Development\NUS-Docu'
    current_dir = r'C:\Users\bened\Documents\Development\weva\IT_OT_testbed'
    entry_details = _openDir(current_dir)

    return render_template("index.html", entries=entry_details, current_dir=current_dir)

def is_markdown_file(file_path):
    extension = os.path.splitext(file_path)[1]  # Get the file extension
    return extension.lower() == '.md'

def is_image_file(file_path):
    # Adjust this function to determine if the file is an image (e.g., PNG, JPG, etc.)
    return file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

@app.route("/<path:entry>")
def file(entry):
    full_path = os.path.join(current_dir, entry)
    if os.path.isfile(full_path):
        try:
            if is_image_file(entry):
                # If it's an image, directly return the file using Flask's send_file
                return send_file(full_path, mimetype='image/png')  # Adjust mimetype as needed

            if is_markdown_file(entry):
                with open(full_path, "r", encoding='utf-8') as f:
                    content = f.read()
                
                # Convert Markdown content to HTML without images (for Marked.js)
                html_content = markdown.markdown(content, extensions=['markdown.extensions.extra'])

                return render_template('markdown_file.html', html_content=html_content)
           
            else:
                with open(full_path,  "r", encoding='utf-8') as f:
                    content = f.read()
    
                    #lexer = get_lexer_for_filename(full_path)
                    #formatter = HtmlFormatter(style='colorful')

                    # Highlight the file content using Pygments
                    #highlighted_code = highlight(content, lexer, formatter)
                    #print(highlighted_code)
                

                return render_template('text_file.html', file_content=content, current_dir=full_path)
                #return render_template("file_content.html", highlighted_code=highlighted_code)
            

            
        except Exception as e:
            print(f"Error: {str(e)}")
            return f"Error: {str(e)}"
        
    else:
        entry_details = _openDir(full_path)
        return render_template("index.html", entries=entry_details, current_dir=current_dir)


if __name__ == "__main__":
    app.run(debug=True, port=5000)