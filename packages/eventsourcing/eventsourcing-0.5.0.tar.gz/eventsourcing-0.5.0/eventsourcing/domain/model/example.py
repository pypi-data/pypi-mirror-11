from abc import ABCMeta, abstractmethod
import uuid

from eventsourcing.domain.model.entity import EventSourcedEntity
from eventsourcing.domain.model.events import publish


class Example(EventSourcedEntity):

    class Created(EventSourcedEntity.Created):

        @property
        def a(self):
            return self.__dict__['a']

        @property
        def b(self):
            return self.__dict__['b']

    def __init__(self, entity_id, a, b):
        super().__init__(entity_id=entity_id)
        self.a = a
        self.b = b


class Repository(metaclass=ABCMeta):
    
    @abstractmethod
    def __getitem__(self, item):
        pass


def register_new_example(a, b):
    """
    Factory method for example entities.
    """
    entity_id = uuid.uuid4().hex
    event = Example.Created(entity_id=entity_id, a=a, b=b)
    entity = Example.mutator(self=Example, event=event)
    publish(event=event)
    return entity
