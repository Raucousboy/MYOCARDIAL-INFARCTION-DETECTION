import serial
import time
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import heartpy as hp

# Initialize serial communication with Arduino
ser = serial.Serial('COM5', 9600)  # Adjust 'COM3' based on your serial port
time.sleep(2)  # Wait for the serial connection to initialize

# Parameters
fs = 500  # Sampling frequency in Hz
duration = 10  # Duration in seconds to collect data
hr_data = []
hrv_data = []
ecg_data = []

# Collect ECG data
start_time = time.time()
while (time.time() - start_time) < duration:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        try:
            hr, hrv, ecg_value = map(float, line.split(','))
            hr_data.append(hr)
            hrv_data.append(hrv)
            ecg_data.append(ecg_value)
        except ValueError:
            print(f"Could not convert data: {line}")
            continue  # Skip to the next line if conversion fails

# Close the serial connection
ser.close()

# Convert data to numpy arrays for further processing
hr_data = np.array(hr_data)
hrv_data = np.array(hrv_data)
ecg_data = np.array(ecg_data)

# Function to filter ECG signal
def filter_ecg_signal(ecg_signal, fs):
    # High-pass filter (0.5 Hz)
    hp_cutoff = 0.5
    hp_b, hp_a = signal.butter(1, hp_cutoff / (fs / 2), btype='high')
    ecg_hp_filtered = signal.filtfilt(hp_b, hp_a, ecg_signal)

    # Low-pass filter (40 Hz)
    lp_cutoff = 40
    lp_b, lp_a = signal.butter(1, lp_cutoff / (fs / 2), btype='low')
    ecg_lp_filtered = signal.filtfilt(lp_b, lp_a, ecg_hp_filtered)

    # Notch filter (50 Hz)
    notch_freq = 50
    quality_factor = 30
    notch_b, notch_a = signal.iirnotch(notch_freq, quality_factor, fs)
    ecg_filtered = signal.filtfilt(notch_b, notch_a, ecg_lp_filtered)

    return ecg_filtered

# Filter the ECG signal
ecg_filtered = filter_ecg_signal(ecg_data, fs)

# Function to extract features from the ECG signal
def extract_features(ecg_signal, fs):
    wd, m = hp.process(ecg_signal, fs)
    features = {
        'RR_intervals': m['RR_list'],
        'Heart_rate': m['bpm'],
        'QRS_complex': m['qrs_inds'],
        'HRV': m['hrv'],
        'ST_elevation': m['st_slope'],  # Simplified; detailed analysis may need custom code
        'ST_depression': m['st_depression'], 
        } # Simplified; detailed analysis may need