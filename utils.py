def get_pagination(offset: int, limit: int, total: int):
    next_offset = offset + limit if offset + limit < total else None
    prev_offset = offset - limit if offset - limit >= 0 else None
    return {
        "next": next_offset,
        "limit": limit,
        "previous": prev_offset
    }
