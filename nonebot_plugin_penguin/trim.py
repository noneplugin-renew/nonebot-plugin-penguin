from .types import Matrix, Request, RenderByItem, RenderByStage

def matrix_sort(matrixs: list[Matrix], request: Request) -> list[Matrix]:
    return sorted(
        matrixs, key=lambda x: getattr(x, request.sort_by), reverse=request.reverse
    )


def matrix_filter(matrixs: list[Matrix], request: Request) -> list[Matrix]:
    match request.filter_by:
        case "all":
            return [
                matrix
                for matrix in matrixs
                if matrix.quantity > request.ignore_threshold
            ]
        case "only_open":
            return [
                matrix
                for matrix in matrixs
<<<<<<< HEAD
                if not matrix.end and matrix.quantity > request.ignore_threshold
=======
                if not matrix.end and matrix.quantity > ignore_threshold
>>>>>>> 4311f3d (:construction: 初步完成matrix export)
            ]
        case "only_close":
            return [
                matrix
                for matrix in matrixs
<<<<<<< HEAD
                if matrix.end and matrix.quantity > request.ignore_threshold
=======
                if matrix.end and matrix.quantity > ignore_threshold
>>>>>>> 4311f3d (:construction: 初步完成matrix export)
            ]


def matrix_export(
<<<<<<< HEAD
    matrixs: list[Matrix], request: Request
) -> list[RenderByItem | RenderByStage]:
    trimed_matrixs = matrix_filter(matrixs, request)
    trimed_matrixs = matrix_sort(matrixs, request)

    return list(
        map(
            lambda x: x.export(lang=request.lang, mode=request.type),
=======
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
            },
>>>>>>> 4311f3d (:construction: 初步完成matrix export)
            trimed_matrixs,
        )
    )
