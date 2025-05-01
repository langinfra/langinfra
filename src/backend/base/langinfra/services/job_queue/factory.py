from langinfra.services.base import Service
from langinfra.services.factory import ServiceFactory
from langinfra.services.job_queue.service import JobQueueService


class JobQueueServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(JobQueueService)

    def create(self) -> Service:
        return JobQueueService()
