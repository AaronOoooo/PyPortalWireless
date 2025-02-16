import time
import board
import terminalio
import displayio
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import busio
import digitalio
import storage

# Import Wi-Fi credentials
try:
    from secrets import secrets
except ImportError:
    print("❌ WiFi secrets are missing! Add them to secrets.py")
    raise

# ✅ Initialize Display
def initialize_display():
    """Initialize the PyPortal display and create a simple background."""
    display = board.DISPLAY
    splash = displayio.Group()
    bg_rect = Rect(0, 0, display.width, display.height, fill=0x000000)  # Black background
    splash.append(bg_rect)
    display.root_group = splash
    return display, splash

# ✅ Create Text Labels
def create_labels(splash):
    """Create and return text labels for displaying network information."""
    text_area_ip = label.Label(
        terminalio.FONT,
        text="Connecting...",
        color=0xFFFFFF,  # White text
        x=10,
        y=30
    )
    splash.append(text_area_ip)

    text_area_ssid = label.Label(
        terminalio.FONT,
        text="SSID: ...",
        color=0xFFFFFF,  # White text
        x=10,
        y=60
    )
    splash.append(text_area_ssid)

    text_area_mac = label.Label(
        terminalio.FONT,
        text="MAC: ...",
        color=0xFFFFFF,  # White text
        x=10,
        y=90
    )
    splash.append(text_area_mac)

    return text_area_ip, text_area_ssid, text_area_mac

# ✅ Initialize Wi-Fi
def initialize_wifi():
    """Initialize the ESP32 co-processor and Wi-Fi manager."""
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp32_cs = digitalio.DigitalInOut(board.ESP_CS)  # ✅ Correct Pin
    esp32_ready = digitalio.DigitalInOut(board.ESP_BUSY)  # ✅ Correct Pin
    esp32_reset = digitalio.DigitalInOut(board.ESP_RESET)  # ✅ Correct Pin
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)
    return esp, wifi

# ✅ Connect to Wi-Fi
def connect_to_wifi(wifi, max_retries=10):
    """Connect to Wi-Fi with retry logic."""
    retries = 0
    while retries < max_retries:
        try:
            wifi.connect()
            print("✅ Wi-Fi Connected!")
            return True
        except RuntimeError as e:
            print(f"❌ Wi-Fi failed: {e}")
            retries += 1
            time.sleep(2)
    return False

# ✅ Format IP Address
def format_ip(raw_ip):
    """Convert a bytearray IP address to a human-readable string."""
    return ".".join(str(b) for b in raw_ip)

# ✅ Format MAC Address
def format_mac(raw_mac):
    """Convert a bytearray MAC address to a human-readable string."""
    return ":".join(f"{b:02X}" for b in raw_mac)

# ✅ Main Function
def main():
    # ✅ Check if SD card is mounted
    if storage.getmount("/"):
        print("✅ SD card is already mounted, skipping SD setup.")

    # ✅ Initialize Display and Labels
    display, splash = initialize_display()
    text_area_ip, text_area_ssid, text_area_mac = create_labels(splash)

    # ✅ Initialize Wi-Fi
    print("Initializing Wi-Fi...")
    esp, wifi = initialize_wifi()

    # ✅ Connect to Wi-Fi
    print("Connecting to Wi-Fi...")
    if not connect_to_wifi(wifi):
        print("❌ Failed to confirm Wi-Fi connection. Exiting.")
        text_area_ip.text = "Wi-Fi Error"
        while True:
            time.sleep(1)

    # ✅ Display IP Address
    raw_ip = esp.ip_address
    formatted_ip = format_ip(raw_ip)
    print(f"✅ Connected! IP Address: {formatted_ip}")
    text_area_ip.text = f"IP: {formatted_ip}"

    # ✅ Display SSID
    ssid = secrets["ssid"]  # Retrieve SSID from secrets.py
    print(f"✅ SSID: {ssid}")
    text_area_ssid.text = f"SSID: {ssid}"

    # ✅ Display MAC Address
    mac_address = format_mac(esp.MAC_address)
    print(f"✅ MAC Address: {mac_address}")
    text_area_mac.text = f"MAC: {mac_address}"

    # ✅ Keep the Program Running
    while True:
        time.sleep(1)

# Run the main function
if __name__ == "__main__":
    main()