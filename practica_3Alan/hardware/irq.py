## Emula una solicitud de interrupción.
class IRQ:

    ##  Estas son la interrupciones soportadas por nuestro Kernel
    KILL_INTERRUPTION_TYPE = "#KILL"

    @classmethod
    def KILL_INTERRUPTION(self):
        return IRQ(IRQ.KILL_INTERRUPTION_TYPE)

    def __init__(self, type, parameters = None):
        self._type = type
        self._parameters = parameters

    def  add_parameter(self, param):
        self._parameters.append(param)

    @property
    def parameters(self):
        return self._parameters

    @property
    def type(self):
        return self._type
