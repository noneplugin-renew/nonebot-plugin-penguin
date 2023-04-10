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
                if not matrix.end and matrix.quantity > request.ignore_threshold
            ]
        case "only_close":
            return [
                matrix
                for matrix in matrixs
                if matrix.end and matrix.quantity > request.ignore_threshold
            ]


def matrix_export(
    matrixs: list[Matrix], request: Request
) -> list[RenderByItem | RenderByStage]:
    trimed_matrixs = matrix_filter(matrixs, request)
    trimed_matrixs = matrix_sort(matrixs, request)

    return list(
        map(
            lambda x: x.export(lang=request.lang, mode=request.type),
            trimed_matrixs,
        )
    )
