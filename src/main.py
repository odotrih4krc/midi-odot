import machine
import time
import ustruct

# MIDI settings
MIDI_CHANNEL = 0  # MIDI Channel (0-15)
MIDI_BAUDRATE = 31250  # Standard MIDI baud rate

# Define pins for potentiometers and buttons
pot_pins = [machine.Pin(26), machine.Pin(27), machine.Pin(28)]  # Analog pins for pots
button_pins = [machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP), 
               machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)]  # Digital pins for buttons

# Function to send MIDI messages
def send_midi_message(status, data1, data2=0):
    midi_message = ustruct.pack('BBB', status, data1, data2)
    uart.write(midi_message)

# Initialize UART for MIDI communication
uart = machine.UART(1, baudrate=MIDI_BAUDRATE, tx=machine.Pin(0))

# Main loop
try:
    while True:
        # Read potentiometer values and send MIDI CC messages
        for i, pot in enumerate(pot_pins):
            pot_value = int(pot.read_u16() / 256)  # Scale 0-65535 to 0-127
            send_midi_message(0xB0 | MIDI_CHANNEL, i, pot_value)  # Control Change Message

        # Read button states and send MIDI Note On/Off messages
        for i, button in enumerate(button_pins):
            if button.value() == 0:  # Button pressed (active low)
                send_midi_message(0x90 | MIDI_CHANNEL, i + 60, 127)  # Note On (C4, C#4, etc.)
                time.sleep(0.1)  # Debounce delay
                send_midi_message(0x80 | MIDI_CHANNEL, i + 60, 0)  # Note Off
                time.sleep(0.1)  # Debounce delay

        time.sleep(0.1)  # Main loop delay

except KeyboardInterrupt:
    pass