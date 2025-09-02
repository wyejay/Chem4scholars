# services/elements_service.py
from periodictable import elements

LAN_START, LAN_END = 57, 71     # La–Lu
ACT_START, ACT_END = 89, 103    # Ac–Lr

def _series_index(Z: int) -> int:
    """0-based index within lanthanides or actinides."""
    if LAN_START <= Z <= LAN_END:
        return Z - LAN_START
    if ACT_START <= Z <= ACT_END:
        return Z - ACT_START
    return -1

def get_all_elements():
    """
    Returns all 118 elements with enough info to draw a proper periodic table grid.
    For groups/periods we rely on the library; we special-case f-block placement.
    """
    data = []
    for Z in range(1, 119):
        e = elements[Z]
        # Library has .group and .period for most; f-block needs custom row/col for the display.
        group = getattr(e, "group", None)
        period = getattr(e, "period", None)

        # Category colors: use block (s,p,d,f) as a clean, stable grouping
        block = getattr(e, "block", None)  # 's','p','d','f'

        # Visual placement:
        row, col = None, None
        if 1 <= Z <= 118:
            if LAN_START <= Z <= LAN_END:
                # Lanthanides live on their own display row (row 8), columns 4..17
                row = 8
                col = 4 + _series_index(Z)
            elif ACT_START <= Z <= ACT_END:
                # Actinides on row 9, columns 4..17
                row = 9
                col = 4 + _series_index(Z)
            else:
                # Regular placement uses real period/group
                row = period
                col = group

        data.append({
            "Z": Z,
            "symbol": e.symbol,
            "name": e.name.capitalize(),
            "atomic_mass": getattr(e, "mass", None),
            "block": block,          # s/p/d/f
            "group": group,          # 1..18 (None for some f-block)
            "period": period,        # 1..7
            "row": row,              # for CSS Grid
            "col": col,              # for CSS Grid
            # quick flags
            "is_lanth": LAN_START <= Z <= LAN_END,
            "is_act": ACT_START <= Z <= ACT_END,
        })
    return data
