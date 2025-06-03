import os
import subprocess
import logging
import webbrowser
from urllib.parse import quote
from langchain_community.chat_models import ChatOllama
from tenacity import retry, stop_after_attempt, wait_random_exponential

class EmailGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.available_models = ["llama3", "mistral"]
        self._init_model()
        self.sender_email = "senser_name@co.in"  # Your Thunderbird email

    def _init_model(self):
        """Initialize Ollama connection with fallback models"""
        try:
            for model_name in self.available_models:
                try:
                    self.model = ChatOllama(
                        model=model_name,
                        base_url="http://localhost:11435",
                        temperature=0.7
                    )
                    test_response = self.model.invoke("Hello")
                    if test_response:
                        self.logger.info(f"Using model: {model_name}")
                        return
                except Exception as e:
                    continue
            self.logger.warning("No working model found, using fallback template")
        except Exception as e:
            self.logger.error(f"Ollama connection failed: {str(e)}")

    def _send_via_thunderbird(self, subject, body, recipient):
        """Send email using Thunderbird's command line interface"""
        try:
            # Construct the Thunderbird compose command
            compose_cmd = (
                f'subject="{subject}",'
                f'to="{recipient}",'
                f'body="{body}",'
                f'from="{self.sender_email}"'
            )

            # Platform-specific commands
            if os.name == 'posix':  # Linux/macOS
                subprocess.run(['thunderbird', '-compose', compose_cmd], check=True)
            elif os.name == 'nt':   # Windows
                thunderbird_path = os.path.expandvars(r'%APPDATA%\Thunderbird\thunderbird.exe')
                if os.path.exists(thunderbird_path):
                    subprocess.run([thunderbird_path, '-compose', compose_cmd], check=True)
                else:
                    self.logger.warning("Thunderbird not found at default location")
                    return False
            return True
        except Exception as e:
            self.logger.warning(f"Thunderbird CLI failed: {str(e)}")
            return False

    def _create_mailto_link(self, subject, body, recipient):
        """Create a mailto link as fallback"""
        mailto = (
            f"mailto:{recipient}?"
            f"subject={quote(subject)}&"
            f"body={quote(body)}&"
            f"from={quote(self.sender_email)}"
        )
        return mailto

    def generate_and_send_email(self, laptop: dict, review_summary: str, recipient_email: str, recipient_name: str = "Sir"):
        """Generate and send email through Thunderbird"""
        # Generate email content
        if self.model:
            try:
                prompt = (
                    f"Write a professional email from {self.sender_email} recommending "
                    f"{laptop['name']} (₹{laptop['price']}) to {recipient_name}. "
                    f"Key points: {review_summary}. Include purchase link: {laptop.get('url', 'Not available')}"
                )
                email_content = self.model.invoke(prompt).content.strip()
            except Exception as e:
                email_content = self._fallback_email(laptop, review_summary, recipient_name)
        else:
            email_content = self._fallback_email(laptop, review_summary, recipient_name)

        subject = f"Purchase Recommendation: {laptop['name']} (₹{laptop['price']})"
        
        # Try sending via Thunderbird CLI
        if not self._send_via_thunderbird(subject, email_content, recipient_email):
            # Fallback to mailto link
            mailto_link = self._create_mailto_link(subject, email_content, recipient_email)
            print("\n✉️ Thunderbird not accessible via command line.")
            print("Please click this link to open email in Thunderbird:")
            print(f"\n{mailto_link}\n")
            
            # Try opening mailto link automatically
            try:
                webbrowser.open(mailto_link)
            except Exception as e:
                print("Couldn't open email client automatically. Please copy the above link.")

        print("\n📧 Email Details:")
        print("-" * 50)
        print(f"From: {self.sender_email}")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print("\nBody:")
        print(email_content)
        print("-" * 50)

    def _fallback_email(self, laptop: dict, review_summary: str, recipient_name: str) -> str:
        """Fallback email template"""
        return f"""Dear {recipient_name},

I recommend purchasing:

• {laptop['name']} 
• Price: ₹{laptop['price']}
• Seller: {laptop['seller']}
• Link: {laptop.get('url', 'Not available')}

Review Summary:
{review_summary}

Please let me know if you approve this purchase.

Best regards,
{self.sender_email}"""