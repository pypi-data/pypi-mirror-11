from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import object


class Scene(object):
    """
    Class to store the details of a single scene to be displayed.  This is
    made up of a set of :py:obj:`.Effect` objects.  See the documentation for
    Effect to understand the interaction between the two classes.
    """

    def __init__(self, effects, duration=0, clear=True):
        """
        :param effects: The list of effects to apply to this scene.
        :param duration: The number of frames in this Scene.  A value of 0
                         means that the Scene should query the Effects to find
                         the duration.  A value of -1 means don't stop.
        :param clear: Whether to clear the Screen at the start of the Scene.
        """
        self._effects = effects
        self._duration = duration
        if duration == 0:
            self._duration = max([x.stop_frame for x in effects])
        self._clear = clear

    def reset(self):
        """
        Reset the scene ready for playing.
        """
        for effect in self._effects:
            effect.reset()

    def process_key(self, key):
        """
        Process a new keypress.

        :param key: The key that has been pressed.
        :returns: None if the Scene processed the key, else the original key.
        """
        for effect in self._effects:
            key = effect.process_key(key)
            if key is None:
                break
        return key

    @property
    def effects(self):
        """
        :return: The list of Effects in this Scene.
        """
        return self._effects

    @property
    def duration(self):
        """
        :return: The length of the scene in frames.
        """
        return self._duration

    @property
    def clear(self):
        """
        :return: Whether the Scene should clear at the start.
        """
        return self._clear
