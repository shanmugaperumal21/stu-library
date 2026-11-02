# Build Full Report for StudentSphere Project
# Generates DOCX, HTML, PDF, and MD files with complete 17 sections and embedded figures

import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

WORKSPACE = r"e:\st-20261015T083357Z-1-001"

print("Starting report generation script...")
