"""Module with chemical functions."""

from token import Token
from decimal import Decimal

D = Decimal

TABLE = {
    'H': D('1.00794'),
    # Alkali metals
    'Li': D('6.941'),
    'Na': D('22.9898'),
    'K': D('39.0983'),
    'Rb': D('85.4678'),
    'Cs': D('132.905'),
    'Fr': D('223'),
    # Alkaline Earth metals
    'Be': D('9.01218'),
    'Mg': D('24.305'),
    'Ca': D('40.078'),
    'Sr': D('87.62'),
    'Ba': D('137.327'),
    'Ra': D('226'),
    # Group III B
    'Sc': D('44.9559'),
    'Y': D('88.9059'),
    'La': D('138.905'),
    'Ac': D('227'),
    # Group IV B
    'Ti': D('47.867'),
    'Zr': D('91.224'),
    'Hf': D('178.49'),
    'Rf': D('265'),
    # Group V B
    'V': D('50.9415'),
    'Nb': D('92.9064'),
    'Ta': D('180.948'),
    'Db': D('268'),
    # Group VI B
    'Cr': D('51.9961'),
    'Mo': D('95.96'),
    'W': D('183.84'),
    'Sg': D('271'),
    # Group VII B
    'Mn': D('54.938'),
    'Tc': D('98'),
    'Re': D('186.207'),
    'Bh': D('272'),
    # Group VIII
    'Fe': D('55.845'),
    'Ru': D('101.07'),
    'Os': D('190.23'),
    'Hs': D('270'),
    'Co': D('58.9332'),
    'Rh': D('102.906'),
    'Ir': D('192.217'),
    'Mt': D('276'),
    'Ni': D('58.6934'),
    'Pd': D('106.42'),
    'Pt': D('195.084'),
    'Ds': D('281'),
    # Group I B
    'Cu': D('63.546'),
    'Ag': D('107.868'),
    'Au': D('196.967'),
    'Rg': D('280'),
    # Group II B
    'Zn': D('65.38'),
    'Cd': D('112.411'),
    'Hg': D('200.59'),
    'Cn': D('285'),
    # Group III A
    'B': D('10.811'),
    'Al': D('26.9815'),
    'Ga': D('69.723'),
    'In': D('114.818'),
    'Tl': D('204.383'),
    'Nh': D('284'),
    # Group IV A
    'C': D('12.0107'),
    'Si': D('28.0855'),
    'Ge': D('72.64'),
    'Sn': D('118.71'),
    'Pb': D('207.2'),
    'Fl': D('289'),
    # Group V A
    'N': D('14.0067'),
    'P': D('30.9738'),
    'As': D('74.9216'),
    'Sb': D('121.76'),
    'Bi': D('208.98'),
    'Mc': D('288'),
    # Group VI A
    'O': D('15.9994'),
    'S': D('32.065'),
    'Se': D('78.96'),
    'Te': D('127.6'),
    'Po': D('209'),
    'Lv': D('293'),
    # Group VII A
    'F': D('18.998'),
    'Cl': D('35.453'),
    'Br': D('79.904'),
    'I': D('126.904'),
    'At': D('210'),
    'Ts': D('294'),
    # Group VIII A
    'He': D('4.0026'),
    'Ne': D('20.1797'),
    'Ar': D('39.948'),
    'Kr': D('83.798'),
    'Xe': D('131.293'),
    'Rn': D('222'),
    'Og': D('294'),
    # Lanthanides
    'Ce': D('140.116'),
    'Pr': D('140.908'),
    'Nd': D('144.242'),
    'Pm': D('145'),
    'Sm': D('150.36'),
    'Eu': D('151.964'),
    'Gd': D('157.25'),
    'Tb': D('158.925'),
    'Dy': D('162.5'),
    'Ho': D('164.93'),
    'Er': D('167.259'),
    'Tm': D('168.934'),
    'Yb': D('173.054'),
    'Lu': D('174.967'),
    # Actinides
    'Th': D('232.038'),
    'Pa': D('231.036'),
    'U': D('238.029'),
    'Np': D('237'),
    'Pu': D('244'),
    'Am': D('243'),
    'Cm': D('247'),
    'Bk': D('247'),
    'Cf': D('251'),
    'Es': D('252'),
    'Fm': D('257'),
    'Md': D('258'),
    'No': D('259'),
    'Lr': D('262'),
}


def mass_precision(precision=None):
    """Find molar mass of compound to the given precision.

    Returns a function that takes the compound name & returns its molar mass.
    """

    def get_table_data(st):
        if st == 'Cl' and precision == 0:
            return D('35.5')
        if precision is None:
            return TABLE[st]
        return round(TABLE[st], precision)

    def f(st):
        if st.isalpha():
            if st not in TABLE:
                raise ValueError('incorrect compound name')
            return get_table_data(st)
        else:
            if len(st) < 2:
                raise ValueError('incorrect compound name')
            elif st[-2].isdigit():
                st, n = st[:-2], st[-2:]
            else:
                st, n = st[:-1], st[-1:]
            if st not in TABLE:
                raise ValueError('incorrect compound name')
            return get_table_data(st) * int(n)

    def wrapper(compound):
        import re
        compound = re.sub(r'([A-Z()\[\]*])', r' \1', compound)[1:]
        m = [0, 0, 0, 0]
        level = 1
        for el in compound.split():
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
        return m[0]

    return wrapper


exporttokens = [
    Token('M', mass_precision(2), 'normal', 'func', 'Molar mass of compound'),
    Token.wrap(Decimal('6.02214076e23'), name='NA', ht="Avogadro's constant"),
    Token.wrap(Decimal('22.4'), name='Vm', ht='Molar volume at STP'),
]
