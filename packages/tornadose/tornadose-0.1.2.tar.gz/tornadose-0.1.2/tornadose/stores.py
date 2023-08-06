"""Data storage for dynamic updates to clients."""

from uuid import uuid4


class DataStore(object):
    """Generic object for producing data to feed to clients.

    Notes
    -----
    To use this, simply instantiate and update the ``data`` property
    whenever new data is available. When creating a new
    :class:`EventSource` handler, specify the :class:`DataStore`
    instance so that the :class:`EventSource` can listen for
    updates.

    When data is updated, a unique id is generated. This is in order
    to enable the publisher to update any new data, even if the value
    is the same as the previous data.

    """
    def __init__(self, initial_data=None):
        self.set_data(initial_data)

    def set_data(self, new_data):
        """Update the store with new data."""
        self._data = new_data
        self.id = uuid4()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self.set_data(new_data)


class StoreContainer(object):
    """Class for holding multiple stores."""
    def __init__(self, stores=None):
        """Create the container with a list of stores."""
        assert isinstance(stores, (list, tuple)) or stores is None
        if stores is not None:
            assert [isinstance(store, DataStore) for store in stores]
            self._stores = stores
        else:
            self._stores = []

    def __len__(self):
        return len(self._stores)

    def __getitem__(self, i):
        return self._stores[i]

    def add(self, store):
        """Add a store to the container."""
        assert isinstance(store, DataStore)
        self._stores.append(store)

    def add_stores(self, stores):
        """Add several stores to the container at once."""
        assert isinstance(stores, (list, tuple))
        [self.add(store) for store in stores]
