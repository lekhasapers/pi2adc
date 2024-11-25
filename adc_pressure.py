#by Lekha Sapers
import spidev
import time 

spibus = spidev.SpiDev() #assuming the bus is an adc
spibus.open(0,0) #bus number and chip selection
#spibus.mode = 0b01
spibus.max_speed_hz = 1350000 #documentation says can handle up to 125Mhz

VREF = 5  # ADC reference voltage 
MAX_PRESSURE = 700  # Maximum pressure in kPa 
MIN_VOLTAGE = 2.7  # based on datasheet
MAX_VOLTAGE = 5.5  #" "


def read_adc(channel): #reading adc value from mcp
    if channel < 0 or channel > 7:
        raise ValueError("Invalid channel, must be 0-7")
    command = [1, (8 + channel) << 4, 0]
    response = spibus.xfer2(command)
    data = ((response[1] & 3) << 8) | response[2] #ripped these lines from rasppi forum, not entirely sure what they mean
    return data

def adc_to_pressure(adc_value):
    voltage = (adc_value / 1023) * VREF  # Convert ADC value to voltage
    pressure = ((voltage - MIN_VOLTAGE) / (MAX_VOLTAGE - MIN_VOLTAGE)) * MAX_PRESSURE
    pressure = max(0, min(pressure, MAX_PRESSURE))  # Clamp pressure to valid range
    return pressure

#def adc_to_volts(data, places):
    #volts = (data * 3.3) / float(1023)
    #volts = round(volts,places)
    #return volts

# Map pressure to notes in one octave
def pressure_to_note(pressure):
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C+']
    index = int((pressure / MAX_PRESSURE) * (len(notes) - 1))
    return notes[index]

try:
    #print("Measuring pressure and mapping to notes...")
    while True:
        adc_value = read_adc(0)  
        pressure = adc_to_pressure(adc_value)
        note = pressure_to_note(pressure)
        print(f"ADC Value: {adc_value}, Pressure: {pressure:.2f} kPa), Note: {note}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    spibus.close()


#Resources: 
#https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf
#https://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/

