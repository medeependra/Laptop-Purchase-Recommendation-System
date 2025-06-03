# Laptop-Purchase-Recommendation-System


## 📁 Project Structure
Purchasing_Agent/
├── main.py # Main application script
├── scraper.py # Web scraping functionality
├── analyzer.py # Review analysis module
├── email_generator.py # Email generation and sending
├── manual_laptops.csv # Sample data file (created during execution)
├── requirements.txt # Python dependencies
└── README.txt # This file

## 🌟 Key Features
- Opens Google Shopping in Microsoft Edge for laptop research
- Manual CSV input for product selection
- Sentiment analysis of product reviews
- AI-powered email drafting using Ollama
- Direct email sending through Thunderbird
- Multiple fallback mechanisms for reliability

## 📚 Libraries Required
    selenium==4.9.1
    webdriver-manager==3.8.6
    pandas==2.0.3
    transformers==4.31.0
    nltk==3.8.1
    langchain-community==0.0.11
    python-dotenv==1.0.0
    requests==2.31.0

## 🛠️ Installation
1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Install required packages:
   ```bash
   pip install -r requirements.txt

Download NLTK data:
    import nltk
    nltk.download(['vader_lexicon', 'stopwords', 'punkt'])

Set up Ollama:
    ollama pull llama3
    ollama serve

💻 Platform Requirements:
    Windows 10/11 (with Edge browser)
    Mozilla Thunderbird installed and configured (with dsharma@ndsinfo.com account)
    Python 3.8+
    4GB+ RAM

🚀 Execution Instructions:

    Run the main script:
          python main.py
      
Follow on-screen instructions:
      Browser will open to Google Shopping
      Enter top 5 laptops in manual_laptops.csv
      Press Enter when done
      System will:
      Analyze reviews
      Generate recommendation email
      Open Thunderbird with draft email

⚙️ Configuration Options:
      Edit main.py to change:
      Budget amount (default: ₹60,000)
      Recipient email/name
      Edit email_generator.py to:
      Change default sender 
      Modify email templates

🛑 Known Limitations
    Requires manual CSV input for product data
    Thunderbird must be installed and set as default mail client
    Internet connection required for initial setup

🔄 Workflow Diagram
    Launch Edge → Google Shopping
    Manual CSV creation
    Data analysis
    Email generation
    Thunderbird integration
