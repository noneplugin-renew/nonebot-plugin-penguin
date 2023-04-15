from ..types import Coord


class ItemIcon:
    size: int = 183
    dimensions: tuple = (1098, 3111)
    pic: str = "sprite.202210111514.png"
    previous_size: int = 60

    @classmethod
    def transform_coord(cls, coord: Coord, size: int | None = None) -> Coord:
        size = size or cls.previous_size
        return tuple(map(lambda x: x * size, coord))

    @classmethod
    def style(cls, coord: Coord, size: int | None = None):
        size = size or cls.previous_size
        zoom = size / cls.size
        real_coord = cls.transform_coord(coord, size)
        return f"""
        height: {size}px;
        width: {size}px;
        background-image: url(./{cls.pic});
        background-size: {round(cls.dimensions[0] * zoom)}px {round(cls.dimensions[1] * zoom)}px;
        background-position: {-real_coord[0]}px {-real_coord[1]}px;
        """  # noqa: E501
