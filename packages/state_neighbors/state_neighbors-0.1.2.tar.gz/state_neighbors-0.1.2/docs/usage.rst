========
Usage
========

To use State Neighbors in a project::

    import state_neighbors

Example::
    
    >>> import state_neighbors
    >>> state_neighbors.neighboring("AZ")
    ['CA', 'CO', 'NM', 'NV', 'UT']
    >>> sn = state_neighbors.StateNeighbor(contigous=True, allow_blank=True)
    >>> sn.neighbors("AK")
    []
    >>> sn.STATES
    OrderedDict([('AK', []), ('AL', ['FL', 'GA', 'MS', 'TN']), ('AR',... 
