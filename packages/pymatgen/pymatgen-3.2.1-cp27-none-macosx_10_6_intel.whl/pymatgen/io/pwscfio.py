# coding: utf-8

from __future__ import division, unicode_literals

"""
This module implements input and output processing from PWSCF.
"""

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Virtual Lab"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "ongsp@ucsd.edu"
__date__ = "3/27/15"


import six


class PWInput(object):
    """
    Base input file class. Right now, only supports no symmetry and is
    very basic.
    """

    def __init__(self, structure, pseudo, control=None, system=None,
                 electrons=None, ions=None, cell=None, kpoints_mode="automatic",
                 kpoints_grid=(1, 1, 1),kpoints_shift=(0, 0, 0)):
        """
        Initializes a PWSCF input file.

        Args:
            structure (Structure): Input structure
            pseudo (dict): A dict of the pseudopotentials to use.
            control (dict): Control parameters. Refer to official PWSCF doc
                on supported parameters. Default to {"calculation": "scf"}
            system (dict): System parameters. Refer to official PWSCF doc
                on supported parameters. Default to None, which means {}.
            electrons (dict): Electron parameters. Refer to official PWSCF doc
                on supported parameters. Default to None, which means {}.
            ions (dict): Ions parameters. Refer to official PWSCF doc
                on supported parameters. Default to None, which means {}.
            cell (dict): Cell parameters. Refer to official PWSCF doc
                on supported parameters. Default to None, which means {}.
            kpoints_mode (str): Kpoints generation mode. Default to automatic.
            kpoints_grid (sequence): The kpoint grid. Default to (1, 1, 1).
            kpoints_shift (sequence): The shift for the kpoints. Defaults to
                (0, 0, 0).
        """
        self.structure = structure
        sections = {}
        sections["control"] = control or {"calculation": "scf"}
        sections["system"] = system or {}
        sections["electrons"] = electrons or {}
        sections["ions"] = ions or {}
        sections["cell"] = cell or {}
        for species in self.structure.composition.keys():
            if species.symbol not in pseudo:
                raise PWInputError("Missing %s in pseudo specification!")
        self.pseudo = pseudo
        self.sections = sections
        self.kpoints_mode = kpoints_mode
        self.kpoints_grid = kpoints_grid
        self.kpoints_shift = kpoints_shift

    def __str__(self):
        out = []
        def to_str(v):
            if isinstance(v, six.string_types):
                return "'%s'" % v
            return v
        for k1 in ["control", "system", "electrons", "ions", "cell"]:
            v1 = self.sections[k1]
            out.append("&%s" % k1.upper())
            sub = []
            for k2 in sorted(v1.keys()):
                sub.append("  %s = %s" % (k2, to_str(v1[k2])))
            if k1 == "system":
                sub.append("  ibrav = 0")
                sub.append("  nat = %d" % len(self.structure))
                sub.append("  ntyp = %d" % len(self.structure.composition))
            sub.append("/")
            out.append(",\n".join(sub))

        out.append("ATOMIC_SPECIES")
        for k, v in self.structure.composition.items():
            out.append("  %s %.4f %s" % (k.symbol, k.atomic_mass,
                                         self.pseudo[k.symbol]))
        out.append("ATOMIC_POSITIONS crystal")
        for site in self.structure:
            out.append("  %s %.6f %.6f %.6f" % (site.specie.symbol, site.a,
                                                site.b, site.c))
        out.append("K_POINTS %s" % self.kpoints_mode)
        kpt_str = ["%s" % i for i in self.kpoints_grid]
        kpt_str.extend(["%s" % i for i in self.kpoints_shift])
        out.append("  %s" % " ".join(kpt_str))
        out.append("CELL_PARAMETERS angstrom")
        for vec in self.structure.lattice.matrix:
            out.append("  %f %f %f" % (vec[0], vec[1], vec[2]))
        return "\n".join(out)

    def write_file(self, filename):
        """
        Write the PWSCF input file.

        Args:
            filename (str): The string filename to output to.
        """
        with open(filename, "w") as f:
            f.write(self.__str__())


class PWInputError(BaseException):
    pass


if __name__ == "__main__":
    from pymatgen.core.structure import Structure
    coords = []
    coords.append([0, 0, 0])
    coords.append([0.75, 0.5, 0.75])
    lattice = [[3.8401979337, 0.00, 0.00],
               [1.9200989668, 3.3257101909, 0.00],
               [0.00, -2.2171384943, 3.1355090603]]
    structure = Structure(lattice, ["Si", "Si"], coords)
    pw = PWInput(structure,
                    control={"calculation": "scf", "pseudo_dir": './'},
                    pseudo={"Si": "Si.pbe-n-kjpaw_psl.0.1.UPF"},
                    system={"ecutwfc": 50})
    pw.write_file("Si.pw.in")