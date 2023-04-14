Coord = tuple[int, int]


class ItemIcon:
    size: int = 183
    dimensions: tuple = (1098, 3111)
    pic: str = "sprite.20221011514.png"
    previous_size: int = 60

    @classmethod
    def transform_coord(cls, coord: Coord) -> Coord:
        return tuple(map(lambda x: x * cls.previous_size, coord))

    @classmethod
    def style(cls, coord: Coord):
        zoom = cls.previous_size / cls.size
        real_coord = cls.transform_coord(coord)
        return f"""
        height: {cls.previous_size}px;
        width: {cls.previous_size}px;
        background-image: url(./{cls.pic});
        background-size: {round(cls.dimensions[0] * zoom)}px {round(cls.dimensions[1] * zoom)}px;
        background-position: {-real_coord[0]}px {-real_coord[1]}px;
        """  # noqa: E501
