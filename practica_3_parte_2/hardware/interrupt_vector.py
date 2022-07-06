from helpers import log

## Emula el vector de interrupciones.
class InterruptVector():

    def __init__(self):
        self._handlers = {}

    def register(self, interruptionType, interruptionHandler):
        self._handlers[interruptionType] = interruptionHandler

    def handle(self, irq):
        log.logger.info("\nHandling {type} irq with parameters = {parameters}\n".format(type=irq.type, parameters=irq.parameters ))
        self._handlers[irq.type].execute(irq)
