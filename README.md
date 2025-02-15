
# PyPortal Wi-Fi Connection Display

This project demonstrates how to connect an Adafruit PyPortal to a Wi-Fi network and display the device's IP address on the screen. The code initializes the PyPortal's display, connects to Wi-Fi using the ESP32 co-processor, and shows the IP address once the connection is established.

---

## 🚀 **Features**

- **Wi-Fi Connection**: Connects to a Wi-Fi network using credentials stored in a `secrets.py` file.
- **IP Address Display**: Displays the device's IP address on the PyPortal's screen in a properly formatted way.
- **Retry Logic**: Implements retry logic with up to 10 attempts for Wi-Fi connection.
- **SD Card Check**: Verifies if an SD card is already mounted and skips setup if mounted.
- **Manual Display Initialization**: The display is initialized manually to avoid PyPortal's built-in initialization.
- **Correct Pin Usage**: Ensures the correct pins are used for the ESP32 co-processor on the PyPortal.
- **Improved IP Display Logic**: Converts `bytearray` IP to a human-readable string format.

---

## 🛠 **Hardware Requirements**
- Adafruit PyPortal
- MicroSD card (optional, for additional storage)
- USB-C cable for power and programming

---

## 💻 **Software Requirements**
- **CircuitPython 7.x or later**
- **Adafruit CircuitPython libraries**:
  - `adafruit_esp32spi`
  - `adafruit_display_text`
  - `adafruit_display_shapes`
  - `terminalio`
  - `displayio`
  - `busio`
  - `digitalio`
  - `storage`

---

## 🛠 **Setup Instructions**

### 1. Install CircuitPython:
- Download the latest version of CircuitPython for the PyPortal from the [CircuitPython website](https://circuitpython.org/board/pyportal/).
- Follow the [PyPortal CircuitPython guide](https://learn.adafruit.com/adafruit-pyportal) to install CircuitPython on your device.

### 2. Install Required Libraries:
- Download the necessary CircuitPython libraries from the [CircuitPython Library Bundle](https://circuitpython.org/libraries).
- Copy the following libraries to the `lib` folder on your PyPortal:
  - `adafruit_esp32spi`
  - `adafruit_display_text`
  - `adafruit_display_shapes`
  - `terminalio`
  - `displayio`
  - `busio`
  - `digitalio`
  - `storage`

### 3. Create `secrets.py`:
- Create a file named `secrets.py` in the root directory of your PyPortal.
- Add your Wi-Fi credentials as follows:

```python
secrets = {
    "ssid": "YOUR_WIFI_SSID",
    "password": "YOUR_WIFI_PASSWORD",
}
```
Replace `YOUR_WIFI_SSID` and `YOUR_WIFI_PASSWORD` with your actual Wi-Fi credentials.

### 4. Upload the Code:
- Copy the provided `code.py` to the root directory of your PyPortal.
- The PyPortal will automatically run the code when powered on.

---

## 🔧 **How It Works**

1. **Display Initialization**: Manually initializes the PyPortal display and creates a black background with a text label.
2. **Wi-Fi Connection**: Connects to the Wi-Fi network using `adafruit_esp32spi` with retry logic to handle failures.
3. **IP Address Display**: Converts the device's IP from `bytearray` to a readable string and displays it.
4. **Error Handling**: Displays an error message if the Wi-Fi connection fails after multiple attempts.

---

## 📜 **Code Overview**

- **Display Initialization**: Manually initializes the display, avoiding PyPortal's built-in method, and creates a black background using `Rect` from `adafruit_display_shapes`.
- **Wi-Fi Setup**: Uses correct ESP32 pins for PyPortal, ensures retry logic, and confirms the connection via `esp.is_connected`.
- **IP Display**: Converts raw IP to a human-readable format and displays it.
- **SD Card Check**: Checks if the SD card is mounted and skips setup if already mounted.

---

## 🛡 **Troubleshooting**

### **Wi-Fi Connection Issues:**
- Ensure the Wi-Fi credentials in `secrets.py` are correct.
- Verify that the PyPortal is within range of the Wi-Fi network.
- If the connection fails, the program will retry up to 10 times before displaying an error.

### **SD Card Issues:**
- If an SD card is inserted, the program checks if it is already mounted and skips the setup if necessary.

---

## 📝 **License**
This project is open-source and available under the MIT License. Feel free to modify and distribute it as needed.

---

**Thank you for using this PyPortal Wi-Fi Connection Display project! 🚀**
