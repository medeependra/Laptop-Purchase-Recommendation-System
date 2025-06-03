from scraper import scraper
from analyzer import ReviewAnalyzer
from email_generator import EmailGenerator
import pandas as pd
import os
import time

def launch_google_shopping(max_price=60000):
    """Open Google Shopping in Edge for manual data collection"""
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.edge.options import Options
    from webdriver_manager.microsoft import EdgeChromiumDriverManager

    url = f"https://www.google.com/search?q=laptops+under+{max_price}+inr&tbm=shop"

    options = Options()
    options.add_argument("--start-maximized")
    
    print("\n🖥️ Launching Microsoft Edge...")
    try:
        driver = webdriver.Edge(
            service=Service(EdgeChromiumDriverManager().install()),
            options=options
        )
        driver.get(url)
        
        print("\n🌐 Google Shopping has been opened in Microsoft Edge.")
        print("📝 Please enter the top 5 products into 'manual_laptops.csv'")
        print("   CSV format: name,price,seller,url")
        print("   Example: HP Victus Gaming,59990,Amazon,https://www.amazon.in/dp/B0C6VYX4DJ")
        input("\n✅ Press Enter after completing and saving 'manual_laptops.csv'...")
        
    except Exception as e:
        print(f"❌ Error launching browser: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

def main():
    # Step 1: Open Google Shopping
    launch_google_shopping(60000)

    # Step 2: Load manual data
    csv_path = "manual_laptops.csv"
    while not os.path.exists(csv_path):
        print("\n⚠️ 'manual_laptops.csv' not found. Please create it with the laptop data.")
        input("Press Enter to retry after creating the file...")
        time.sleep(1)

    laptops_df = pd.read_csv(csv_path)
    laptops_df["source"] = "Manual CSV"
    
    print("\n=== ✅ Loaded Laptop Data ===")
    print(laptops_df[['name', 'price', 'seller']].to_string(index=False))

    # Step 3: Select best product (by price)
    best_laptop = laptops_df.sort_values('price').iloc[0].to_dict()

    # Step 4: Mock reviews
    reviews = [
        "Battery life is outstanding",
        "Boots fast and handles multitasking well",
        "Display is sharp but speaker quality is average"
    ]

    # Step 5: Analyze reviews
    print("\n🔍 Analyzing reviews...")
    analyzer = ReviewAnalyzer()
    analysis = analyzer.analyze_reviews(reviews)

    print(f"📈 Sentiment Score: {analysis['sentiment']:.2f}")
    print(f"📝 Review Summary: {analysis['summary']}")

    # Step 6: Generate and send email
    print("\n✉️ Preparing email in Thunderbird...")
    email_gen = EmailGenerator()
    
    # Configure recipient details
    recipient_email = "name@gmail.com"  # Change to actual recipient
    recipient_name = "Manager"                 # Change as needed
    
    email_gen.generate_and_send_email(
        best_laptop,
        analysis["summary"],
        recipient_email,
        recipient_name
    )

    print("\n✅ Process completed! Check your Thunderbird client.")

if __name__ == "__main__":
    main()