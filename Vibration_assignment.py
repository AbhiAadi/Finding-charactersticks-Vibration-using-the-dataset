#importing Libraries
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks


#Importing the data and assigning the datasets into variables
#Plotting the dataset.
excel_file_path = 'Vibration.xlsx'
data = pd.read_excel(excel_file_path)
time = data.iloc[3278:,0].values
time = time - time[0]
displacement = data.iloc[3278:,1].values
plt.plot(time, displacement)
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.title('Time vs Displacement')
plt.show()


#Transforming the to frequency domain using FFT.
#Plotting the frequency Graph
fft_result = np.fft.fft(displacement)
frequencies = np.fft.fftfreq(len(fft_result), d=(time[1] - time[0]))
amplitude_spectrum = np.abs(fft_result)

sorted_indices = np.argsort(amplitude_spectrum)[::-1]  
second_highest_peak_index = sorted_indices[1]
second_highest_peak_frequency = frequencies[second_highest_peak_index]
print("Index of the second highest peak:", second_highest_peak_index)
print("Frequency of the second highest peak:", second_highest_peak_frequency, "Hz")

plt.figure(figsize=(10, 6))
plt.plot(np.abs(frequencies), amplitude_spectrum)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Magnitude Spectrum')
plt.grid(True)
plt.show()

#For finding the settling time, I manually calculated the 1% value and used to calculate settling time.
settling_threshold = 0.01 * displacement[0]
settling_time_index = 250
print(time[settling_time_index])
settling_time = time[settling_time_index] - time[0]
print('Settling Time: ',settling_time)

#Plotting the peaks of displacements wrt time.
prominence_threshold = 0.1 
peaks, _ = find_peaks(displacement, prominence=prominence_threshold)

plt.figure(figsize=(10, 6))
plt.plot(time, displacement, label='Displacement (mV)')
plt.plot(time[peaks], displacement[peaks], 'ro', label='Peaks')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (mV)')
plt.title('Displacement vs. Time with Peaks')
plt.grid(True)
plt.legend()
plt.show()
print(peaks)

#Finding the damping ratio using Log decrement method.
second_highest_freq_idx = np.argsort(amplitude_spectrum)[-2]

# # Calculate damping ratio (ξ)
A1 = amplitude_spectrum[0]
A2 = amplitude_spectrum[second_highest_freq_idx]
# Calculate damping factor (ξ) for each pair of successive peaks
damping_ratio = -np.log(A2 / A1) / np.sqrt((np.log(A2 / A1))**2 + np.pi**2)

print("Damping Ratio (ζ):", damping_ratio)


#For Curve Fit, I use the log decrement equation to obtain the exponential decrement equation.
expo_curve = []
for i in range(len(time)):
    expo_curve.append(7.82*np.exp(-second_highest_peak_frequency*damping_ratio*time[i]))
print(expo_curve)

plt.figure(figsize=(10, 6))
plt.plot(time, expo_curve, label='Exponential Curve')
plt.plot(time, displacement , label = 'Displacement Curve')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (mV)')
plt.title('Displacement and Exponential curve vs. Time ')
plt.grid(True)
plt.legend()
plt.show()



