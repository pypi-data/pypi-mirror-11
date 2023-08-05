# This module is part of Hypatia and is released under the
# MIT License: http://opensource.org/licenses/MIT

"""Constants, enumerations for Hypatia.

Generally, these constants and enumerations serve to replace
the usage of strings for such paramount attributes like
direction and action. The benefit of this model is:

  * enhances code clarity
  * provides type checking
  * provides constants operations, e.g.,
    `North + East = North East`.
  * class methods to convert one datatype to a constant, like
    velocity to direction

Example:
  >>> from hypatia import animations
  >>> sprite = animations.Walkabout('debug')
  >>> sprite.animations[Action.walk][Direction.east]
  <pyganim.PygAnimation object at 0x...>

See Also:
   *  :attribute:`actor.Actor.direction`
   *  :attribute:`animations.Walkabout.direction`

"""

import enum


# Intentionally not using `enum.IntEnum` because there is no reason to
# compare values of `Direction` to integers.
@enum.unique
class Direction(enum.Enum):
    """Compass direction. Specific to movement of a sprite/surface.

    Inspired by Unix numerical permissions. Only ever
    combined with one other direction max.

    See Also:
        :class:`physics.Velocity`

    Note:
        I don't see a point in having a separate class for ordinal
        and cardinal classes.

    """

    # Cardinal Directions
    #
    # The values for these directions are the powers of two because
    # that avoids potential conflicts with ordinal directions.  The
    # values for ordinal directions are the addition of their cardinal
    # components, e.g. `north_east` has the value of `north` plus
    # `east`.  Defining the cardinal directions as powers of two
    # avoids a problem by which ordinal directions could end up with
    # same values which would make equality comparisons true for
    # directions which should never be equal.
    north = 1
    east = 2
    south = 4
    west = 8

    # Ordinal Directions
    north_east = 3
    north_west = 9
    south_east = 6
    south_west = 12

    # just for fun
    north_south = 5
    east_west = 10

    @classmethod
    def cardinal(cls):
        """Return a tuple of the cardinal directions in the order:
        North, East, South, West.

        Returns:
            tuple: (north, east, south, west)

        """

        return (cls.north, cls.east, cls.south, cls.west)

    @classmethod
    def x_plus(cls):
        """Returns the direction associated
        with moving RIGHT (+x) on the X-AXIS.

        Returns:
            Direction.east

        """

        return cls.east

    @classmethod
    def x_minus(cls):
        """Returns the direction associated
        with moving LEFT (-x) on the X-AXIS.

        Returns:
            Direction.west

        """

        return cls.west

    @classmethod
    def y_plus(cls):
        """Returns the direction associated
        with moving DOWN (+y) on the Y-AXIS.

        Returns:
            Direction.south

        """

        return cls.south

    @classmethod
    def y_minus(cls):
        """Returns the direction associated
        with moving UP (-y) on the Y-AXIS.

        Returns:
            Direction.north

        """

        return cls.north

    @classmethod
    def from_velocity(cls, velocity):
        """Return a direction which corresponds
        to the current 2D velocity.

        See Also:
            :class:`constants.Direction`

        Returns:
            :class:`constants.Direction`: --

        """

        # We're going to combine the directions
        # extrapolated from each axis, then
        # combine them to make a new direction!
        collected_directions = []

        for axis in ['x', 'y']:
            # e.g., call Direction.x_plus() to get the positive
            # axis direction for 'x' (which would be East).
            plus_direction = getattr(Direction, axis + '_plus')()

            # e.g., call Direction.y_minus() to get the negative
            # axis direction for 'y' (which would be North).
            minus_direction = getattr(Direction, axis + '_minus')()

            # get the current velocity for this axis, determine
            # if it's positive (use plus_direction), negative
            # (use minus_direction) or neutral (do nothing!).
            axis_value = getattr(velocity, axis)

            if axis_value > 0:
                # the velocity for this axis is positive,
                # therefore it is the "plus direction."
                collected_directions.append(plus_direction)
            elif axis_value == 0:
                # the velocity for this axis is neutral,
                # therefore we cannot extrapolate
                # direction from velocity.
                pass
            else:
                # Deductively, the axis value is negative,
                # therefore it is the "minus_direction."
                collected_directions.append(minus_direction)

        # Cool trick, huh? North + East = North East, so forth.
        # Be sure to check out Direction.__add__.
        return collected_directions[0] + collected_directions[1]

    def __add__(cls, other_direction):
        """Combine one cardinal direction with
        another to get an ordinal direction.

        Args:
            other_direction (Direction): one of the Direction
                enumerations.

        Returns:
            :class:`Direction`: an ordinal direction.

        Example:
          >>> Direction.east + Direction.north == Direction.north_east
          True

        """

        return Direction(cls.value + other_direction.value)


@enum.unique
class Action(enum.Enum):
    """Specific to movement of a sprite/surface.

    Attributes:
        stand (int): Actor standing/normal/no-input state.
        walk (int): Actor walking/moving state. Actor
            has velocity.

    See Also:
        :class:`animations.Walkabout`

    """

    stand = 1
    walk = 2
