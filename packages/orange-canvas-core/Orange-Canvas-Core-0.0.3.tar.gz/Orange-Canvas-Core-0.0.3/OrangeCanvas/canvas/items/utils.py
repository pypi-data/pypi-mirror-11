import numpy

import sip

from PyQt4.QtGui import QColor, QRadialGradient, QPainterPathStroker
from PyQt4.QtCore import QObject, QSignalMapper
from PyQt4.QtCore import pyqtSignal as Signal


def saturated(color, factor=150):
    """Return a saturated color.
    """
    h = color.hsvHueF()
    s = color.hsvSaturationF()
    v = color.valueF()
    a = color.alphaF()
    s = factor * s / 100.0
    s = max(min(1.0, s), 0.0)
    return QColor.fromHsvF(h, s, v, a).convertTo(color.spec())


def sample_path(path, num=10):
    """Sample `num` equidistant points from the `path` (`QPainterPath`).
    """
    space = numpy.linspace(0.0, 1.0, num, endpoint=True)
    return [path.pointAtPercent(float(p)) for p in space]


def radial_gradient(color, color_light=50):
    """
    radial_gradient(QColor, QColor)
    radial_gradient(QColor, int)

    Return a radial gradient. `color_light` can be a QColor or an int.
    In the later case the light color is derived from `color` using
    `saturated(color, color_light)`.

    """
    if not isinstance(color_light, QColor):
        color_light = saturated(color, color_light)
    gradient = QRadialGradient(0.5, 0.5, 0.5)
    gradient.setColorAt(0.0, color_light)
    gradient.setColorAt(0.5, color_light)
    gradient.setColorAt(1.0, color)
    gradient.setCoordinateMode(QRadialGradient.ObjectBoundingMode)
    return gradient


def toGraphicsObjectIfPossible(item):
    """Return the item as a QGraphicsObject if possible.

    This function is intended as a workaround for a problem with older
    versions of PyQt (< 4.9), where methods returning 'QGraphicsItem *'
    lose the type of the QGraphicsObject subclasses and instead return
    generic QGraphicsItem wrappers.

    """
    if item is None:
        return None

    obj = item.toGraphicsObject()
    return item if obj is None else obj


def typed_signal_mapper(pyType):
    """Create a TypedSignalMapper class supporting signal
    mapping for `pyType` (the default QSigalMapper only supports
    int, string, QObject and QWidget (but not for instance QGraphicsItem).

    """

    def unwrap(obj):
        return sip.unwrapinstance(sip.cast(obj, QObject))

    class TypedSignalMapper(QSignalMapper):
        pyMapped = Signal(pyType)

        def __init__(self, parent=None):
            QSignalMapper.__init__(self, parent)
            self.__mapping = {}

        def setPyMapping(self, sender, mapped):
            sender_id = unwrap(sender)
            self.__mapping[sender_id] = mapped
            sender.destroyed.connect(self.removePyMappings)

        def removePyMappings(self, sender):
            sender_id = unwrap(sender)
            del self.__mapping[sender_id]
            sender.destroyed.disconnect(self.removePyMappings)

        def pyMap(self, sender=None):
            if sender is None:
                sender = self.sender()

            sender_id = unwrap(sender)
            mapped = self.__mapping[sender_id]
            self.pyMapped.emit(mapped)

    return TypedSignalMapper


def linspace(count):
    """Return `count` evenly spaced points from 0..1 interval excluding
    both end points, e.g. `linspace(3) == [0.25, 0.5, 0.75]`.

    """
    return numpy.linspace(0.0, 1.0, count + 2, endpoint=True)[1:-1]


def uniform_linear_layout(points):
    """Layout the points (a list of floats in 0..1 range) in a uniform
    linear space while preserving the existing sorting order.

    """
    indices = numpy.argsort(points)
    space = numpy.asarray(linspace(len(points)))

    # invert the indices
    indices = numpy.argsort(indices)
#     indices = invert_permutation_indices(indices)
#    assert((numpy.argsort(points) == numpy.argsort(space[indices])).all())
    points = space[indices]

    return points.tolist()


def invert_permutation_indices(indices):
    """Invert the permutation giver by indices.
    """
    inverted = [0] * len(indices)
    for i, index in enumerate(indices):
        inverted[index] = i
    return inverted


def stroke_path(path, pen):
    """Create a QPainterPath stroke from the `path` drawn with `pen`.
    """
    stroker = QPainterPathStroker()
    stroker.setCapStyle(pen.capStyle())
    stroker.setJoinStyle(pen.joinStyle())
    stroker.setMiterLimit(pen.miterLimit())
    stroker.setWidth(max(pen.widthF(), 1e-9))

    return stroker.createStroke(path)
