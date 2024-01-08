import numpy as np
import math as math

timestep = int(input(f" Please insert the timestep [0 included]: "))

timeT = np.zeros((timestep,1))
incT = np.zeros((timestep,1))
cumT = np.zeros((timestep-1,1))
intensT = np.zeros((timestep-1,1))
cum = 0
for i in range(timestep-1):
    time = float(input(f" Please insert the time ({i + 2}) [minute] : "))
    timeT[i+1, 0] = time
for i in range(timestep-1):
    inc = float(input(f" Please insert the increment rainfall ({i+2}) [cm] :"))
    incT[i+1,0] = inc
for i in range(timestep-1):
    cum += incT[i+1,0]
    cumT[i,0] = cum

intensT[0, 0] = float(incT[1,0]) / ((float(timeT[1,0]/60.0)))

for i in range(1,timestep-1):
    intensT[i,0] = float(incT[i+1,0]) / ((float(timeT[i+1,0] - timeT[i,0])/60.0))

porosity = float(input(" Please insert the porosity value : "))
effporosity = float(input(" Please insert the effective porosity value : "))
head = float(input(" Please insert the wetting front soil suction head value [cm] : "))
conduct = float(input(" Please insert the hydraulic conductivity value [cm/h] : "))
se = float(input(" Please insert the effective saturation value [0 - 1]: "))

deltateta = float((1-se)*effporosity)

infrateT = np.zeros((timestep-1,1))

kt = float(conduct*timeT[1, 0] / 60.0)

for i in range(timestep-1):
    deltateta = float((1 - se) * effporosity)
    infrate = float(conduct * (head*deltateta/cumT[i,0]+1.0))
    infrateT[i,0] = infrate

for i in range(timestep - 1):
    if infrateT[i,0] < intensT[i,0]:
        print(f" Ponding not occurs between timestep (0) and timestep ({i+1}).")
        break

cuminfrateT = np.zeros((timestep-1-i,1))
result = kt - cumT[i-1, 0] - (deltateta * head * (math.log(((kt + deltateta * head) / (cumT[i-1, 0] + deltateta * head))))) - kt
print(result)
dt = 0
max_iterations = 100000
iteration = 0
tolerance =1e-3
newcum = np.zeros((timestep-i-1,1))
while iteration < max_iterations:
    dt = dt + 0.01
    result = (conduct * dt) - cumT[i - 1, 0] - (deltateta * head * (math.log(((conduct * dt + deltateta * head) / (cumT[i - 1, 0] + deltateta * head))))) - kt
    if abs(result) < tolerance:
        print(f"New cum value is ({conduct * dt}).")
        newcum[0, 0] = conduct * dt
    else:
        iteration += 1

dt = 0
max_iterations = 100000
iteration = 0
tolerance =1e-3
while iteration < max_iterations:
    dt = dt + 0.01
    result = (conduct * dt) - newcum[0, 0] - (deltateta * head * (math.log(((conduct * dt + deltateta * head) / (newcum[0, 0] + deltateta * head))))) - kt
    if abs(result) < tolerance:
        print(f"New cum value is ({conduct * dt}).")
        newcum[1, 0] = conduct * dt
    else:
        iteration += 1

print(newcum)






    # while iteration < max_iterations:
    #
    #     result = (kt) - cumT[t,0] - deltateta * head * (math.log((kt+deltateta * head)/(cumT[t,0]+deltateta * head),math.e))-kt

#         if abs(result) < tolerance:
#             break
#         iteration += 1
#     cuminfrateT[p, 0] = result
#     p += 1
#
# print(infrateT)
# print(cuminfrateT)

