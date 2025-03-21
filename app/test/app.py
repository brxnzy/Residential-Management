from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import time
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Create a BytesIO buffer to store the PDF
        buffer = io.BytesIO()
        
        # Create PDF in memory
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica", 16)
        c.drawString(30, 750, "Form Data PDF")
        
        c.setFont("Helvetica", 12)
        c.drawString(30, 700, f"Name: {name}")
        c.drawString(30, 680, f"Email: {email}")
        c.drawString(30, 660, "Message:")
        
        # Handle multiline message
        lines = message.split('\n')
        y_position = 640
        for line in lines:
            c.drawString(30, y_position, line)
            y_position -= 15
        
        c.save()
        
        # Move to the beginning of the buffer
        buffer.seek(0)
        
        # Return the PDF file and stay on the same page
        return send_file(
            buffer,
            as_attachment=True,
            download_name="form_data.pdf",
            mimetype='application/pdf'
        )
        
    # GET request - show the form
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)