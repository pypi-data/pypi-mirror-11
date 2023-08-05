# -*- coding: utf-8 -*-
"""Provides target dimension object."""

from __future__ import absolute_import
import warnings
from ..errors import ClientError
from ..entity import SubEntity
from .targetvalue import TargetValue
from ..utils import PATHS

class TargetDimension(SubEntity):
    """docstring for TargetDimension."""
    collection = 'target_dimensions'
    resource = 'target_dimension'
    _relations = {
        'strategy', 'target_value',
    }

    _pull = {
        '_type': None,
        'exclude': None,
        'include': None,
    }
    _push = _pull
    def __init__(self, session, properties=None, **kwargs):
        super(TargetDimension, self).__init__(session, properties, **kwargs)
        self.environment = kwargs['environment']
        self.include, self.exclude = list(self.include), list(self.exclude)
        for index, ent_dict in enumerate(self.exclude):
            self.exclude[index] = TargetValue(self.session,
                                              properties=ent_dict,
                                              environment=self.environment)
        for index, ent_dict in enumerate(self.include):
            self.include[index] = TargetValue(self.session,
                                              properties=ent_dict,
                                              environment=self.environment)

    def save(self, data=None, **kwargs):
        """Saves the TargetDimension object.

        data: optional dict of properties
        """
        if 'obj' in kwargs:
            import warnings
            warnings.warn('The obj flag is deprecated; discontinue use.',
                          DeprecationWarning, stacklevel=2)
        if data is None:
            data = {}

        data.update({
            'exclude': [location.id if isinstance(location, TargetValue)
                        else location for location in self.exclude],
            'include': [location.id if isinstance(location, TargetValue)
                        else location for location in self.include]
        })

        return super(TargetDimension, self).save(data=data)

    def add(self, group, target):
        """Add target value by ID or instance to group"""
        url = ['target_values', 0]
        if isinstance(target, TargetValue):
            group.append(target)
        elif isinstance(target, int):
            target = [target,]
        if hasattr(target, '__iter__'):
            for child_id in target:
                url[1] = str(child_id)
                entities, _ = super(TargetDimension, self)._get(PATHS['mgmt'],
                                                                '/'.join(url))
                group.append(TargetValue(self.session,
                                         properties=next(entities),
                                         environment=self.environment))
        else:
            raise ClientError('add_to target should be an int or iterator')


    def add_to(self, group, target):
        """Alias for add to retain compatibility"""
        warnings.warn('Deprecated; use `add\' method', DeprecationWarning)
        return self.add(group, target)

    def remove(self, group, target):
        """Remove target value by ID or instance from group"""
        target_values = dict((target_value.id, target_value)
                             for target_value in group)
        if isinstance(target, list):
            for child_id in target:
                try:
                    group.remove(target_values[child_id])
                except ValueError:
                    raise ClientError('Target value with ID {} not in '
                                      'given group.'.format(child_id))
        if isinstance(target, int):
            try:
                group.remove(target_values[target])
            except ValueError:
                raise ClientError('Target value with ID {} not in '
                                  'given group.'.format(target))

    def remove_from(self, group, target):
        """Alias for remove to retain compatibility"""
        warnings.warn('Deprecated; use `remove\' method', DeprecationWarning)
        return self.remove(group, target)
