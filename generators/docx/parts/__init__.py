"""
Part generators for Guide Book Generator.
Each module generates a specific part of the document.
"""

from .cover_page import CoverPageGenerator
from .part_a_pyq import PartAGenerator
from .part_b_concepts import PartBGenerator
from .part_c_answers import PartCGenerator
from .part_custom import CustomPartGenerator
from .part_d_practice import PartDGenerator
from .part_e_constitutional import PartEConstitutionalGenerator
from .part_e_formulas import PartEFormulasGenerator
from .part_e_grammar import PartEGrammarGenerator
from .part_e_graphs import PartEGraphsGenerator
from .part_e_lab import PartELabGenerator
from .part_e_map import PartEGenerator
from .part_f_revision import PartFGenerator
from .part_g_strategy import PartGGenerator
