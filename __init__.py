import math
from modules import cbpi
from modules.core.controller import KettleController
from modules.core.props import Property


@cbpi.controller
class GradientController(KettleController):

    # Custom Properties

    gradientFactor = Property.Number("gradient factor", True, 1.0, description="Sets the gradient factor, default is 1.0")
    hyteresis = Property.Number("hysteresis", True, 1.0, description="hysteresis to prevent to many on/off switches")

    def run(self):
        sampleTime = 10                                # in seconds
        gradientFactor = float(self.gradientFactor)    # gradient factor from settings
        hysteresis = float(self.hyteresis)             # hysteresis to prevent to many on/off switches

        lastTempsSize = math.ceil(60 / sampleTime)     # how many temperatures should be used to calulate gradient
        lastTemps = []                                 # list with last measured temperatures
        
        while self.is_running():
            
            # get current kettle temperature
            currentTemp = float(self.get_temp())
            
            # get current kettle target temperature 
            targetTemp = float(self.get_target_temp())
            
            print 'currentTemp: {0}'.format(currentTemp)
            print 'targetTemp: {0}'.format(targetTemp)

            # gradient can only be calculated, if at minimum 1 last temperatur is known
            if len(lastTemps) > 0:
                
                for i in range(len(lastTemps)):
                    print 'lastTemps[{0}] : {1}'.format(i, lastTemps(i))

                if len(lastTemps) >= lastTempsSize:
                    lastTemp = lastTemps.pop(0)
                    # calculate gradient
                    gradient = currentTemp - lastTemp # gradient in kelvin per minute
                else:
                    lastTemp = lastTemps[0]
                    # calculate gradient
                    gradient = ((currentTemp - lastTemp) / (sampleTime * len(lastTemps)) * 60 # gradient in kelvin per minute

                print 'lastTemp: {0}'.format(lastTemp)
                print 'gradient: {0}'.format(gradient)
                
                if currentTemp >= targetTemp - (gradient * gradientFactor):
                    print 'heater off'
                    self.heater_off()
                elif currentTemp <= targetTemp - (gradient * gradientFactor) - hysteresis:
                    print 'heater on'
                    self.heater_on(100)

            lastTemps.append(currentTemp)

            self.sleep(sampleTime)
