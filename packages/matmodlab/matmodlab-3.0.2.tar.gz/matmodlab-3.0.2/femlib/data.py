import numpy as np
from collections import OrderedDict
from constants import *
from numerix import *

__all__ = ['StepRepository', 'Step', 'Frame', 'FieldOutputs', 'FieldOutput']

class StepRepository(OrderedDict):
    def Step(self, name):
        self[name] = Step(name)
        return self[name]

    def reset(self):
        for (name, step) in self.items():
            for frame in step.frames:
                frame.field_outputs = FieldOutputs()

    def get_field_output_history(self, key, elem_num, invariants=0):
        time = []
        fo_data = []
        for step in self.values():
            for frame in step.frames:
                if time and abs(time[-1] - frame.value) < 1.e-14:
                    continue
                time.append(frame.value)
                fo = frame.field_outputs[key]
                #@tjfulle _a is a hack
                keys, values = fo.get_data(element=elem_num, invariants=invariants)
                fo_data.append(values)
        time = np.asarray(time)
        return FieldOutputHistory(key, fo.type, time, fo_data,
                                  fo.component_labels, fo.valid_invariants)

class Step(object):
    def __init__(self, name):
        self.name = name
        self.frames = []

    def Frame(self, time, increment):
        self.frames.append(Frame(time, increment))
        return self.frames[-1]

class Frame:
    def __init__(self, time, increment):
        self.time = time
        self.increment = increment
        self.value = time + increment
        self.field_outputs = FieldOutputs()

    def FieldOutput(self, name, type, position, mesh, **kwargs):
        s = kwargs.pop('s', 0)
        if name in self.field_outputs:
            if s:
                return self.field_outputs[name]
            raise NameError('{0} is already a field output'.format(name))
        fo = FieldOutput(name, type, position, mesh, **kwargs)
        self.field_outputs[name] = fo
        return self.field_outputs[name]

class FieldOutputs(OrderedDict):
    def add(self, name, type, position, mesh, **kwargs):
        fo = FieldOutput(name, type, position, mesh, **kwargs)
        self[name] = fo
    def keys(self, expand=False):
        if not expand:
            return super(FieldOutputs, self).keys()
        return [key for f in self.values() for key in f.keys]

class FieldOutput:
    def __init__(self, name, type, position, mesh, description=None,
                 component_labels=None, valid_invariants=None, mode='w'):
        self.name = name

        if type not in FIELD_TYPES:
            raise ValueError('unrecognized field type'.format(type))
        self.type = type

        if position not in FIELD_POSITIONS:
            raise ValueError('unrecognized field position'.format(position))
        self.position = position

        self.mesh_instance = mesh

        if description is None:
            description = 'Field output for {0}'.format(name)
        self.description = description

        self.values = []
        self.labels = []
        self.invariants = None
        self.data = None
        self.mode = mode

        if component_labels is None:
            component_labels = COMPONENT_LABELS(type, mesh.dimension)
        elif type == SCALAR:
            raise ValueError('scalars do not have component labels')
        self.component_labels = component_labels

        self.valid_invariants = []
        if self.type == VECTOR:
            self.valid_invariants.append(MAGNITUDE)

        if valid_invariants is not None:
            valid_invariants = aslist(valid_invariants)

        if valid_invariants:
            if self.type == SCALAR:
                raise ValueError('SCALAR values have no valid invariants')
            elif self.type == VECTOR and valid_invariants != [MAGNITUDE]:
                raise ValueError('Invalid VECTOR invariant request')
            elif self.type == TENSOR_3D:
                if any([True for x in valid_invariants if x not in
                        (MISES, PRES, EQ, V)]):
                    raise ValueError('Invalid TENSOR_3D invariant request')
                self.valid_invariants.extend(valid_invariants)

        if self.component_labels is not None:
            error = 0
            n = len(self.component_labels)
            if self.type == VECTOR and n != mesh.dimension: error = 1
            elif self.type == TENSOR_3D and n != 6: error = 1
            elif self.type == TENSOR_3D_FULL and n != 9: error = 1
            if error:
                raise ValueError('inconsistent component labels')
            self.keys = ['%s.%s' % (self.name, x)
                         for x in self.component_labels]
        else:
            self.keys = [self.name]

    def add_data(self, labels, data, num_points=1):

        if np.any(np.in1d(labels, self.labels)):
            raise ValueError('attempting to add multiple data '
                             'to same label[s]')
        labels = aslist(labels)

        data = np.asarray(data)
        n, N = len(data), len(labels) * num_points
        if n != N:
            raise ValueError('expected {0} data points, got {1}'.format(N, n))

        if self.type == SCALAR:
            if len(data.shape) != 1:
                if data.shape[1] != 1:
                    raise ValueError('unexpected SCALAR shape')
            data = data.flatten()

        elif len(data.shape) != 2 and data.shape[1] != len(self.component_labels):
            raise ValueError('inconsistent data')

        if self.data is None:
            self.data = np.array(data)

        elif len(data.shape) != len(self.data.shape):
            raise ValueError('attempting to add multiple data '
                             'to same label[s]')

        else:
            self.data = np.append(self.data, data, 0)

        self.labels.extend(labels)

        if self.mode == 'r':

            if self.valid_invariants:
                invariants = []
                for row in data:
                    values = self.compute_invariants(row, self.valid_invariants)
                    invariants.append(values)
            else:
                invariants = None
            if invariants is not None:
                if self.invariants is None:
                    self.invariants = np.array(invariants)
                else:
                    self.invariants = np.append(self.invariants, invariants, 0)

            pos = FIELD_POSITIONS[self.position]
            typ = FIELD_TYPES[self.type]
            for (i, label) in enumerate(labels):
                invar = None if invariants is None else invariants[i]
                fv = FieldValue(pos, label, typ, data[i], invar)
                self.values.append(fv)

        return

    @staticmethod
    def compute_invariants(a, invariants):
        return compute_invariants(a, invariants)

    def get_value_from_label(self, label):
        return self.values[self.labels.index(label)]

    def get_data(self, sort=0, coords=0, invariants=None, element=None,
                 block=None, flatten=0):

        get_invariants = invariants is None or invariants

        data = self.data
        if flatten:
            data = data.flatten()

        if block is not None:
            elements = self.mesh_instance.blocks[block].elements
            i = [self.labels.index(e) for e in elements]
            return data[i]

        if element is not None:
            # Return values for element number element
            e = self.mesh_instance.elements.index(element)
            if self.type == SCALAR:
                return self.name, data
            keys = [x for x in self.keys]
            data = aslist(data[e])
            if get_invariants and self.valid_invariants:
                keys.extend(['%s.%s' % (self.name, INVARIANTS[x])
                             for x in self.valid_invariants])
                if self.invariants is not None:
                    a = self.invariants[e]
                else:
                    a = self.compute_invariants(data, self.valid_invariants)
                data.extend(aslist(a))
            if len(keys) != len(data):
                raise ValueError('keys and data not consistent')
            return keys, data

        if not sort:
            if invariants:
                keys = [INVARIANTS[x] for x in self.valid_invariants]
                return data, zip(keys, self.invariants)
            return data

        # sort by coordinates
        def r(x):
            return np.sqrt(np.dot(x, x))
        X = np.array([r(self.mesh_instance.get_coords(l, self.position))
                      for l in self.labels])

        i = [a[0] for a in sorted(enumerate(X), key=lambda x: x[1])]

        if not coords:
            return data[i]

        return X[i], data[i]

class FieldValue:
    def __init__(self, position, label, type, data, invariants):
        self.position = position
        self.label = label
        self.data = data
        self.invariants = invariants

class FieldOutputHistory(np.ndarray):
    def __new__(cls, name, fo_type, time, data, component_labels, valid_invariants):
        data = np.asarray(data)
        if fo_type == SCALAR:
            data = data.flatten()
        obj = np.asarray(data).view(cls)
        obj.name = name
        obj.fo_type = type
        obj.time = time
        if valid_invariants:
            a = [compute_invariants(x, valid_invariants) for x in data]
            obj.invariants = np.array(a)
        else:
            obj.invariants = None
        obj.component_labels = component_labels or []
        obj.the_invariants = [INVARIANTS[x] for x in valid_invariants or []]
        return obj

    def __getattr__(self, key):
        if key in self.component_labels:
            i = self.component_labels.index(key)
            return self[:,i]
        if key in self.the_invariants:
            i = self.the_invariants.index(key)
            return self.invariants[:, i]
        raise AttributeError('{0!r} object has no attribute '
                             '{1!r}'.format(self.__class__, key))

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.name = getattr(obj, 'name', None)
        self.fo_type = getattr(obj, 'fo_type', None)
        self.time = getattr(obj, 'time', None)
        self.the_invariants = getattr(obj, 'the_invariants', [])
        if self.the_invariants:
            self.invariants = np.array(obj.invariants)
        else:
            self.invariants = None
        self.component_labels = getattr(obj, 'component_labels', [])

def compute_invariants(a, invariants):
    values = []
    mag = lambda x: np.sqrt(np.dot(x, x))
    for (i, invariant) in enumerate(invariants):
        if invariant in INVARIANTS.values():
            invariant = INVARIANTS.keys()[INVARIANTS.values().index(invariant)]
        if invariant == MISES:
            dev = a - np.sum(a[:3]) * I6
            value = np.sqrt(3./2.) * mag(dev)
        elif invariant == PRES:
            value = -np.sum(a[:3]) / 3.
        elif invariant == EQ:
            value = np.sqrt(2./3.*(np.sum(a[:3]**2) + .5*np.sum(a[3:]**2)))
        elif invariant == V:
            value = np.sum(a[:3])
        elif invariant == MAGNITUDE:
            value = mag(a)
        else:
            raise ValueError('Unknown invariant {0!r}'.format(invariant))
        values.append(value)
    return values
