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

# ✅ Check if SD card is mounted
if storage.getmount("/"):
    print("✅ SD card is already mounted, skipping SD setup.")

# ✅ Initialize Display (Manually, Avoiding PyPortal's Built-in Init)
display = board.DISPLAY

# ✅ Create a Simple Background Rectangle (instead of an image)
splash = displayio.Group()
bg_rect = Rect(0, 0, display.width, display.height, fill=0x000000)  # Black background
splash.append(bg_rect)

# ✅ Create a Label to Display IP Address
text_area = label.Label(
    terminalio.FONT,
    text="Connecting...",
    color=0xFFFFFF,  # White text
    x=50,
    y=100
)
splash.append(text_area)

# ✅ Show the Display Group
display.root_group = splash

# ✅ Setup Wi-Fi using the **CORRECT PINS for PyPortal**
print("Initializing Wi-Fi...")

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp32_cs = digitalio.DigitalInOut(board.ESP_CS)  # ✅ Correct Pin
esp32_ready = digitalio.DigitalInOut(board.ESP_BUSY)  # ✅ Correct Pin
esp32_reset = digitalio.DigitalInOut(board.ESP_RESET)  # ✅ Correct Pin
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

# ✅ Connect to Wi-Fi with Retry Logic
print("Connecting to Wi-Fi...")

MAX_RETRIES = 10
retries = 0

while retries < MAX_RETRIES:
    try:
        wifi.connect()
        print("✅ Wi-Fi Connected!")
        break  # Exit loop if successful
    except RuntimeError as e:
        print(f"❌ Wi-Fi failed: {e}")
        retries += 1
        time.sleep(2)

# ✅ FIX: Use `esp.is_connected` Instead of `WL_CONNECTED`
if not esp.is_connected:
    print("❌ Failed to confirm Wi-Fi connection. Exiting.")
    text_area.text = "Wi-Fi Error"
    while True:
        time.sleep(1)

# ✅ FIX: Convert `bytearray` to Proper IP Address String
raw_ip = esp.ip_address
formatted_ip = ".".join(str(b) for b in raw_ip)  # Converts bytearray to readable IP format
print(f"✅ Connected! IP Address: {formatted_ip}")
text_area.text = f"IP: {formatted_ip}"  # Display the properly formatted IP

# ✅ Keep the Program Running
while True:
    time.sleep(1)
