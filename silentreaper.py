import requests
import time
from datetime import datetime

# === CONFIG SETTINGS ===
TICKET_URL = "https://example.com/ticket-page"  # Replace with actual ticket site URL
REQUEST_INTERVAL = 0.5  # Interval between requests in seconds
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# === FUNCTION TO CHECK TICKET STATUS ===
def is_ticket_available(html_text):
    """
    Check if the ticket is available based on the page's HTML.
    You can customize this logic based on the actual website.
    """
    # Example: Return True if the page does NOT contain "Sold Out"
    return "Sold Out" not in html_text and "sold out" not in html_text

# === FUNCTION TO ATTEMPT TICKET PURCHASE ===
def attempt_purchase():
    """
    Send a purchase request.
    Modify the data dict to match the form fields required by the ticket site.
    """
    purchase_data = {
        "ticket_id": "123456",   # Example field
        "quantity": 1           # Example field
    }
    try:
        response = requests.post(TICKET_URL, headers=HEADERS, data=purchase_data)
        if response.status_code == 200:
            print(f"[{datetime.now()}] Purchase request sent successfully!")
        else:
            print(f"[{datetime.now()}] Purchase request failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] Error sending purchase request: {e}")

# === MAIN BOT LOOP ===
def ticket_bot():
    print("🎟 Ticket bot is running...")
    while True:
        try:
            response = requests.get(TICKET_URL, headers=HEADERS)
            if response.status_code == 200:
                if is_ticket_available(response.text):
                    print(f"[{datetime.now()}] Ticket detected! Attempting to purchase...")
                    attempt_purchase()
                    break  # Stop the bot after trying to purchase
                else:
                    print(f"[{datetime.now()}] Ticket not available yet. Checking again...")
            else:
                print(f"[{datetime.now()}] Failed to load page: HTTP {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now()}] Request error: {e}")

        time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    ticket_bot()
