# FAQ Assistant

## Overview

The FAQ Assistant is an Flask web application that answers user queries using a combination of predefined FAQs and the Google Gemini API. It also includes an admin panel to manage FAQs and view logs. The project is built using Flask, MongoDB, Python and Google Generative AI.

## Features

🔹 **AI-Powered Responses** – Uses Google Gemini API for answering queries.  
🔹 **FAQ Matching** – Matches user queries with existing FAQs.  
🔹 **Admin Panel** – Allows admins to update FAQs.  
🔹 **MongoDB Logging** – Stores logs of FAQ updates.

## Tech Stack

- **Backend**: Python, Flask  
- **AI Model**: Google Gemini API  
- **Database**: MongoDB  
- **Frontend**: HTML, JavaScript (for API calls)

## Installation & Setup

### 1️. Clone the Repository

```bash
git clone https://github.com/your-repo/faq-assistant.git
cd faq-assistant
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a .env file and add your Google API Key:

```bash
GOOGLE_API_KEY=your_api_key_here
```

### 4. Start MongoDB

```bash
mongod
```

### 5. Run the Flask App

```bash
python app.py
```

The app will be available at: http://127.0.0.1:5000/

## Documentation of the Solution:

### Link:
https://docs.google.com/document/d/1CUa7UP9xhPXKJ8dyMfJvQrGbV4Y4PB5t/edit?usp=sharing&ouid=104962134286291058341&rtpof=true&sd=true

## Recorded Video of Flask Website

### Link:
https://drive.google.com/file/d/1wrnI2DsT7nf-3tAUDYzl9M5TonXAbXDn/view?usp=sharing






