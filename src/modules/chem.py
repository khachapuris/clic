"""Module with chemical functions"""

from token import Token
from decimal import Decimal


def mass(cp):
    """Find molar mass of compound"""
    import re

    def f(st):
        if st.isalpha():
            if st not in table:
                raise ValueError('incorrect compound name')
            return table[st]
        else:
            if len(st) < 2:
                raise ValueError('incorrect compound name')
            elif st[-2].isdigit():
                st, n = st[:-2], st[-2:]
            else:
                st, n = st[:-1], st[-1:]
            if st not in table:
                raise ValueError('incorrect compound name')
            return table[st] * int(n)

    table = {
        'H': 1, 'Li': 7, 'Na': 23, 'K': 39, 'Rb': 85, 'Cs': 133, 'Fr': 223,
        'Be': 9, 'Mg': 24, 'Ca': 40, 'Sr': 88, 'Ba': 137, 'Ra': 226,
        'Sc': 45, 'Y': 89, 'La': 139, 'Ac': 227,
        'Ti': 48, 'Zr': 91, 'Hf': 178, 'Rf': 265,
        'V': 51, 'Nb': 93, 'Ta': 181, 'Db': 268,
        'Cr': 52, 'Mo': 96, 'W': 184, 'Sg': 271,
        'Mn': 55, 'Tc': 98, 'Re': 186, 'Bh': 272,
        'Fe': 56, 'Ru': 101, 'Os': 190, 'Hs': 270,
        'Co': 59, 'Rh': 103, 'Ir': 192, 'Mt': 276,
        'Ni': 59, 'Pd': 106, 'Pt': 195, 'Ds': 281,
        'Cu': 64, 'Ag': 108, 'Au': 197, 'Rg': 280,
        'Zn': 65, 'Cd': 112, 'Hg': 201, 'Cn': 285,
        'B': 11, 'Al': 27, 'Ga': 70, 'In': 115, 'Tl': 204, 'Nh': 284,
        'C': 12, 'Si': 28, 'Ge': 73, 'Sn': 119, 'Pb': 207, 'Fl': 289,
        'N': 14, 'P': 31, 'As': 75, 'Sb': 122, 'Bi': 209, 'Mc': 288,
        'O': 16, 'S': 32, 'Se': 79, 'Te': 128, 'Po': 209, 'Lv': 293,
        'F': 19, 'Cl': 35.5, 'Br': 80, 'I': 127, 'At': 210, 'Ts': 294,
        'He': 4, 'Ne': 20, 'Ar': 40, 'Kr': 84, 'Xe': 131, 'Rn': 222, 'Og': 294,
        'Ce': 140, 'Pr': 141, 'Nd': 144, 'Pm': 145, 'Sm': 150, 'Eu': 152, 'Gd': 157,
        'Tb': 159, 'Dy': 162, 'Ho': 165, 'Er': 167, 'Tm': 169, 'Yb': 173, 'Lu': 175,
        'Th': 232, 'Pa': 231, 'U': 238, 'Np': 237, 'Pu': 244, 'Am': 243, 'Cm': 247,
        'Bk': 247, 'Cf': 251, 'Es': 252, 'Fm': 257, 'Md': 258, 'No': 259, 'Lr': 262
    }

    cp = re.sub(r'([A-Z()\[\]*])', r' \1', cp)[1:]
    ls = cp.split()
    m = [0, 0, 0, 0]
    level = 1
    for el in ls:
        if el in ('(', '['):
            level += 1
        elif ')' in el or ']' in el:
            n = 1
            if len(el) > 1:
                n = int(el[1:])
            m[level - 1] += m[level] * n
            m[level] = 0
            level -= 1
        elif el == '*':
            m[0] += m[1]
            m[1] = 0
        else:
            m[level] += f(el)
    m[0] += m[1]
    m[1] = 0
    if m[1] + m[2] + m[3] != 0:
        raise ValueError('incorrect compound name')
    return Decimal(m[0])


exporttokens = [
    Token('M', mass, 'normal', 'func', 'Molar mass of compound'),
]
