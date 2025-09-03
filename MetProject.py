import numpy as np
from metpy.units import units
import metpy.calc as mcalc
from metpy.plots import SkewT, Hodograph
import matplotlib.pyplot as plt

allData = []

with open("C:/Users/jwmoo/OneDrive/Desktop/sampleData.txt") as data:
    firstLine = data.readline()
    splitFirstLine = firstLine.split()
    location = splitFirstLine[0:3]
    dateAndTime = splitFirstLine[5:9]

    for m in range(4):
        data.readline()

    for line in data:
        DataGaps = []
        line = line.strip('\n')
        x = 0
        for c in range(11):
            x += 7
            column = line[x - 1:x]
            if not column.isnumeric():
                DataGaps.append(x)
        line = line.split(" ")

        for d in range(line.count("")):  # removes spaces
            line.remove("")

        for entry in DataGaps:  # Replaces the gaps in the data with "N/A"
            line.insert(int((entry / 7) - 1), "N/A")
        # print(line)
        allData.append(line)

# ----------------------------------------------
# print(allData[2][4])
row = 1

windSpeedList = []
windDirectionList = []
pressureList = []
temperatureList = []
dewpointList = []


for line in allData:
    if line.count("N/A") == 0:
        pressureList.append(float(line[0]))
        temperatureList.append(float(line[2]))
        dewpointList.append(float(line[3]))
        windSpeedList.append(int(line[7]))
        windDirectionList.append(int(line[6]))

speed = np.array(windSpeedList) * units.knots
direction = np.array(windDirectionList) * units.degrees
u, v = mcalc.wind_components(speed, direction)

pressure = np.array(pressureList) * units.hPa
temperature = np.array(temperatureList) * units.degC
dewpoint = np.array(dewpointList) * units.degC
u_wind = np.array(u) * units.knots
v_wind = np.array(v) * units.knots

# Create a figure with skew-T log-P plot
fig = plt.figure(figsize=(10, 10))
skew = SkewT(fig, rotation=45)

# Plot temperature and dewpoint
skew.plot(pressure, temperature, 'r', label="Temperature")
skew.plot(pressure, dewpoint, 'g', label="Dewpoint")
skew.plot(pressure, temperature, 'ro')
skew.plot(pressure, dewpoint, 'go')

# Plot wind barbs
skew.plot_barbs(pressure, u_wind, v_wind)

# Add dry adiabats, moist adiabats, and mixing ratio lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

plt.legend()
plt.title("Skew-T Log-P Diagram (Sounding)")

# Create a hodograph figure
fig, ax = plt.subplots(figsize=(6, 6))
hodograph = Hodograph(ax)
hodograph.add_grid(increment=10)
hodograph.plot(u_wind, v_wind, linewidth=2, label="Hodograph")

plt.legend()
plt.title("Hodograph")
plt.show()