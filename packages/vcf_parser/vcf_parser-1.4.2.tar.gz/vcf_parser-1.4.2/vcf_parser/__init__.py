from pkg_resources import require

__version__ = require("vcf_parser")[0].version

from logging import getLogger
logger = getLogger(__name__)

from vcf_parser.header_parser import HeaderParser
from vcf_parser.log import init_log
from vcf_parser.genotype import Genotype
from vcf_parser.parser import VCFParser
