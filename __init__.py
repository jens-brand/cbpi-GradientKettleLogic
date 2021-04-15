import logging
#import time
from modules import cbpi
from modules.core.controller import KettleController
from modules.core.props import Property


@cbpi.controller
class GradientController(KettleController):

    # Custom Properties
       
    gradientFactor = Property.Number("gradient factor", True, 1.0, description="Sets the gradient factor, default is 1.0")
    hyteresis = Property.Number("hysteresis", True, 1.0, description="hysteresis to prevent to many on/off switches")

    def run(self):
        '''
        Each controller is exectuted in its own thread. The run method is the entry point
        :return: 
        '''

        sampleTime = 10                                # in seconds
        lastTemp = 0                                   # kettle temperature of last loop
        gradientFactor = float(self.gradientFactor)    # gradient factor from settings
        hysteresis = float(self.hyteresis)             # hysteresis to prevent to many on/off switches
        
        while self.is_running():
            
            # get current kettle temperature
            currentTemp = float(self.get_temp())
            
            # get current kettle target temperature 
            targetTemp = float(self.get_target_temp())
            
            cbpi.app.logger.info('currentTemp: {0}'.format(currentTemp))
            cbpi.app.logger.info('targetTemp: {0}'.format(targetTemp))
            cbpi.app.logger.info('lastTemp: {0}'.format(lastTemp))

            # gradient can only be calculated, if temperatur of the last loop is known
            if (lastTemp > 0):
                # calculate gradient
                gradient = ((currentTemp - lastTemp) / sampleTime) * 60 # gradient in kelvin per minute

                cbpi.app.logger.info('gradient: {0}'.format(gradient))
                
                if (currentTemp >= targetTemp - (gradient * gradientFactor)):
                    cbpi.app.logger.info('heater off')
                    self.heater_off()
                elif (currentTemp <= targetTemp - (gradient * gradientFactor) - hysteresis):
                    cbpi.app.logger.info('heater on')
                    self.heater_on(100)

            lastTemp = currentTemp
            self.sleep(sampleTime)
