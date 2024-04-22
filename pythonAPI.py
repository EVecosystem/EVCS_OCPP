import sys
sys.path.append("E:\OPAL-RT\hypersim_2023.2.1.o404\Windows\HyApi\python")
import HyWorksApiGRPC as HyWorksApi
import time
import matplotlib.pyplot as plt
import threading

# Initialize lists to store values
power_values = []
freq_values = []
volt_values = []
time_steps = []

set_delay = 0.02649


# Function to retrieve data
def retrieve_data():
    # Start time
    start_time = time.time()
    while True:
        # Time elapsed since the start
        elapsed_time = time.time() - start_time

        # Break the loop if elapsed time is greater than some threshold
        if elapsed_time > 20:  # Set your desired duration here
            break

        # # Retrieve data
        # sensor2 = HyWorksApi.getLastSensorValues(['LdAAA.P', 'LdAAA.Freq', 'LdAAA.Vrms'])


        # print("Sim Time:", HyWorksApi.getSimulationTime())
        # # Break the loop if elapsed time is greater than some threshold
        # if HyWorksApi.getSimulationTime() == 16:  # Set your desired duration here
        #     break

        # Wait for 0.2 seconds

        # Retrieve data
        start2 = time.time()
        sensor2 = HyWorksApi.getLastSensorValues(['LdAAA.P', 'LdAAA.Freq', 'LdAAA.Vrms'])
        print("Start time getSensor:", start2)

        # Append data to lists
        power_values.append(sensor2[0])
        freq_values.append(sensor2[1])
        volt_values.append(sensor2[2])
        time_steps.append(elapsed_time)

        time.sleep(0.00005)

        # time.sleep(0.00005)
        # print('**************************')
        # print('Power: {0}'.format(sensor2[0]))
        # print('Freq: {0}'.format(sensor2[1]))
        # print('Volt: {0}'.format(sensor2[2]))


# Function to update power values
def update_power_values():
    time.sleep(5)
    power_values2 = ['100000000', '0', '100000000', '0', '100000000', '0', '100000000', '0', '100000000', '0']
                     #'100000000', '0', '100000000', '0', '100000000', '0']
    # print("Simulation Time:", HyWorksApi.getSimulationTime())
    # if HyWorksApi.getSimulationTime() == 6:
    #     for i, value in enumerate(power_values2, start=1):
    #         HyWorksApi.setComponentParameter("LdAAA", "Po", str(value))
    #         time.sleep(1)  # Adjust sleep time as necessary
    # if getsimulationtime==5 #doublecheck to see if it starts exactly 5s after or if theres some delay due to python API
    for i, value in enumerate(power_values2, start=1):
        start = time.time()
        HyWorksApi.setComponentParameter("LdAAA", "Po", str(value))
        print("Start time setCompParam:", start)
        time.sleep(1-set_delay)  # Adjust sleep time as necessary


# def run_acquisition():
#     ScopeViewApi.startAcquisition()
#     sensor = HyWorksApi.getLastSensorValues(['LdAAA.P', 'LdAAA.Freq', 'LdAAA.Vrms'])
#     print('Power Sensor: ', sensor[0])
#     print('Frequency Sensor: ', sensor[1])
#     print('Voltage Sensor: ', sensor[2])


def startHypersim():
    # Open the design
    try:
        HyWorksApi.startAndConnectHypersim()
        designPath = r'E:/Rinith Reghunath/hyp/Model/MODEL/RR_IEEE_9Bus_autobackup_2022_04_12_03_39_25.ecf'
        HyWorksApi.openDesign(designPath)

        HyWorksApi.setPreference('simulation.calculationStep', '50e-6')
        calcStep = HyWorksApi.getPreference('simulation.calculationStep')

        print(('calcStep = ' + calcStep))
        print(('code directory : ' + HyWorksApi.getPreference('simulation.codeDirectory')))
        print(('mode : ' + HyWorksApi.getPreference('simulation.architecture')))

        HyWorksApi.mapTask()
        HyWorksApi.genCode()
        HyWorksApi.startLoadFlow()
        HyWorksApi.analyze()
        HyWorksApi.startSim()
        print("Simulation Time:", HyWorksApi.getSimulationTime())
        # time.sleep(5)  # time to load.
        print('Simulation Started')

        # Initial data retrieval
        sensor = HyWorksApi.getLastSensorValues(['LdAAA.P', 'LdAAA.Freq', 'LdAAA.Vrms'])
        # start_time2 = time.time()
        # print("Before running setCompParam:", time.time() - start_time2)
        # HyWorksApi.setComponentParameter("LdAAA", "Po", str(100000000))
        # print("After running setCompParam:", time.time() - start_time2)
        # sensor = HyWorksApi.getLastSensorValues(['LdAAA.P', 'LdAAA.Freq', 'LdAAA.Vrms'])
        # print("After running getSensorVals:", time.time() - start_time2)
        # power_values.append(sensor[0])
        # freq_values.append(sensor[1])
        # volt_values.append(sensor[2])
        # time_steps.append(0)
        # print("Before running setCompParam:", time.time() - start_time2)
        # HyWorksApi.setComponentParameter("LdAAA", "Po", str(0))
        # print("After running setCompParam:", time.time() - start_time2)
        # sensor = HyWorksApi.getLastSensorValues(['LdAAA.P', 'LdAAA.Freq', 'LdAAA.Vrms'])
        # print("After running getSensorVals:", time.time() - start_time2)
        power_values.append(sensor[0])
        freq_values.append(sensor[1])
        volt_values.append(sensor[2])
        time_steps.append(0)

        print('Power start: {0}'.format(sensor[0]))
        print('Freq start: {0}'.format(sensor[1]))
        print('Volt start: {0}'.format(sensor[2]))

        # Create and start threads
        data_thread = threading.Thread(target=retrieve_data)
        update_thread = threading.Thread(target=update_power_values)
        data_thread.start()
        update_thread.start()

        # Join threads to wait for their completion
        data_thread.join()
        update_thread.join()

        # # Loop for data retrieval every 0.2 seconds
        # while True:
        #     # Time elapsed since the start
        #     elapsed_time = time.time() - start_time
        #
        #     # Break the loop if elapsed time is greater than some threshold
        #     if elapsed_time > 5:  # Set your desired duration here
        #         break
        #
        #     # Wait for 0.2 seconds
        #     time.sleep(0.2)
        #
        #     # Retrieve data
        #     current2 = HyWorksApi.getLastSensorValues(['LdAAA.P', 'LdAAA.Freq', 'LdAAA.Vrms'])
        #
        #     # Append data to lists
        #     power_values.append(current2[0])
        #     freq_values.append(current2[1])
        #     volt_values.append(current2[2])
        #     time_steps.append(elapsed_time)
        #
        #     print('Power: {0}'.format(current2[0]))
        #     print('Freq: {0}'.format(current2[1]))
        #     print('Volt: {0}'.format(current2[2]))

        # Plotting
        plt.figure(figsize=(12, 8))  # Increase figure size

        plt.subplot(3, 1, 1)
        plt.plot(time_steps, power_values, marker='o', markersize=3, linestyle='-', color='b', alpha=0.7)  # Adjust marker size, line style, and alpha
        plt.title('Power')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (in pu)')
        with open('power_data.csv', 'w') as csvfile:
            csvfile.write('Time,Power\n')
            for time, power in zip(time_steps, power_values):
                csvfile.write(f'{time},{power}\n')

        plt.subplot(3, 1, 2)
        plt.plot(time_steps, freq_values, marker='o', markersize=3, linestyle='-', color='r', alpha=0.7)  # Adjust marker size, line style, and alpha
        plt.title('Frequency')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (in Hz)')
        plt.ylim(58, 62)  # Set y-axis limits for frequency
        plt.yticks(range(58, 63, 1))  # Set y-axis ticks for frequency

        plt.subplot(3, 1, 3)
        plt.plot(time_steps, volt_values, marker='o', markersize=3, linestyle='-', color='g', alpha=0.7)  # Adjust marker size, line style, and alpha
        plt.title('Voltage')
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (in pu)')
        plt.ylim(0.7, 1.2)  # Set y-axis limits for voltage
        plt.yticks([i/10 for i in range(7, 12)])  # Set y-axis ticks for voltage

        plt.tight_layout()
        plt.show()
        HyWorksApi.stopSim()

        # current = HyWorksApi.getLastSensorValues(['LdAAA.P', 'LdAAA.Freq', 'LdAAA.Vrms'])
        # power_values.append(current[0])
        # freq_values.append(current[1])
        # volt_values.append(current[2])
        # print('Power start: {0}'.format(current[0]))
        # print('Freq start: {0}'.format(current[1]))
        # print('Volt start: {0}'.format(current[2]))
        #
        # power_values2 = ['100000000', '0', '100000000', '0', '100000000', '0', '100000000', '0']
        # for i, value in enumerate(power_values2, start=1):
        #     HyWorksApi.setComponentParameter("LdAAA", "Po", str(value))
        #     current2 = HyWorksApi.getLastSensorValues(['LdAAA.P', 'LdAAA.Freq', 'LdAAA.Vrms'])
        #     power_values.append(current2[0])
        #     freq_values.append(current2[1])
        #     volt_values.append(current2[2])
        #     print('Power: {0}'.format(current2[0]))
        #     print('Freq: {0}'.format(current2[1]))
        #     print('Volt: {0}'.format(current2[2]))
        #
        # # Generate time steps
        # time_steps = [i * 0.2 for i in range(len(power_values))]
        #
        # # Plotting
        # plt.figure(figsize=(10, 6))
        #
        # plt.subplot(3, 1, 1)
        # plt.plot(time_steps, power_values, marker='o', color='b')
        # plt.title('Power')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Power')
        #
        # plt.subplot(3, 1, 2)
        # plt.plot(time_steps, freq_values, marker='o', color='r')
        # plt.title('Frequency')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Frequency')
        #
        # plt.subplot(3, 1, 3)
        # plt.plot(time_steps, volt_values, marker='o', color='g')
        # plt.title('Voltage')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Voltage')
        #
        # plt.tight_layout()
        # plt.show()
        # # scopeViewProcess = ScopeViewApi.openScopeView()
        # # ScopeViewApi.loadTemplate("NewTemp9bus.svt")
        # # ScopeViewApi.setTimeLength(20.0)
        # # ScopeViewApi.setNumAcq(1)
        # # ScopeViewApi.setSamplingRate(2000)
        # # ScopeViewApi.setTrig(True)
        # # ScopeViewApi.setSync(True)
        # # ScopeViewApi.setCont(True)
        # # print('Scope View Loaded.')
    except Exception as err:
        if (connection):
            connection.close()
        # ScopeViewApi.close()
        HyWorksApi.stopSim()


startHypersim()
#run_acquisition()
