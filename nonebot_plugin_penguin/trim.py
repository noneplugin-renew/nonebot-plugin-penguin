from typing import Any, Literal

from .model import Matrix
from .types import T_Server, lang_map

T_Sorted_Key = Literal["percentage", "apPPR"]
T_Filter_Mode = Literal["all", "only_open", "only_close"]


def matrix_sort(
    matrixs: list[Matrix], key: T_Sorted_Key, reverse: bool = False
) -> list[Matrix]:
    return sorted(matrixs, key=lambda x: getattr(x, key), reverse=reverse)


def matrix_filter(
    matrixs: list[Matrix], mode: T_Filter_Mode = "only_open", ignore_threshold: int = 0
) -> list[Matrix]:
    match mode:
        case "all":
            return [matrix for matrix in matrixs if matrix.quantity > ignore_threshold]
        case "only_open":
            return [
                matrix
                for matrix in matrixs
                if not matrix.end and matrix.quantity > ignore_threshold
            ]
        case "only_close":
            return [
                matrix
                for matrix in matrixs
                if matrix.end and matrix.quantity > ignore_threshold
            ]


def matrix_export(
    matrixs: list[Matrix],
    lang: T_Server,
    sorted_key: T_Sorted_Key,
    filted_mode: T_Filter_Mode,
    reverse: bool = False,
    ignore_threshold: int = 0,
) -> list[dict[str, Any]]:
    trimed_matrixs = matrix_filter(
        matrixs, mode=filted_mode, ignore_threshold=ignore_threshold
    )
    trimed_matrixs = matrix_sort(matrixs, key=sorted_key, reverse=reverse)
    _lang = lang_map[lang]

    return list(
        map(
            lambda x: {
                "stage_name": x.stage.code_i18n[_lang],
                "item_name": x.item.name_i18n[_lang],
                "zone_name": x.zone.zoneName_i18n[_lang],
                "sprite_coord": x.item.spriteCoord,
                "percentage": str(x.percentage) + "%",
                "apPPR": x.apPPR,
                "quantity": x.quantity,
                "time": x.times,
                "opening": True if not x.end else False,
            },
            trimed_matrixs,
        )
    )
