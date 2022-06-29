from time import sleep
from helpers import log
from hardware.hardware import HARDWARE
from so.handlers.abstract_interruption_handler import AbstractInterruptionHandler

class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        scheduler = self.kernel.scheduler

        log.logger.info("Current process finished by IRQ #KILL. Killing current process.")
        scheduler.kill_current_process()

        if scheduler.has_next_process():
            log.logger.info("There are still processes to run. Loading next process...")
            scheduler.load_next_process(HARDWARE.cpu)
        else:
            log.logger.info("No more processes to run. Shutting down the hardware...")
            HARDWARE.switchOff()

