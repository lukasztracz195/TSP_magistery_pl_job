import abc
from typing import Dict, List, Iterable, Any, Mapping


class CsvAbstractRow(abc.ABC):

    @abc.abstractmethod
    def exist_column_name(self, column_name) -> bool:
        pass

    @abc.abstractmethod
    def column_names(self) -> Iterable[Any]:
        pass

    @abc.abstractmethod
    def record_dict(self) -> Mapping[str, Any]:
        pass

    @abc.abstractmethod
    def set_value(self, column_name, value):
        pass

    @abc.abstractmethod
    def set_values_from_dict(self, dictionary_with_data):
        pass

    @abc.abstractmethod
    def not_set_fields(self) -> Iterable[Any]:
        pass
