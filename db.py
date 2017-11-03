from btree import BTree
import requests
from lxml import html
import string
import sys

DEPTS = ['AANB', 'ACAM', 'ADHE', 'AFST', 'AGEC', 'ANAT', 'ANSC', 'ANTH',
         'APBI', 'APPP', 'APSC', 'ARBC', 'ARC', 'ARCH', 'ARCL', 'ARST',
         'ARTH', 'ARTS', 'ASIA', 'ASIC', 'ASLA', 'ASTR', 'ASTU', 'ATSC',
         'AUDI', 'BA', 'BAAC', 'BABS', 'BAEN', 'BAFI', 'BAHC', 'BAHR',
         'BAIM', 'BAIT', 'BALA', 'BAMA', 'BAMS', 'BAPA', 'BASC', 'BASD',
         'BASM', 'BATL', 'BAUL', 'BIOC', 'BIOF', 'BIOL', 'BIOT', 'BMEG',
         'BOTA', 'BRDG', 'BUSI', 'CAPS', 'CCFI', 'CCST', 'CDST', 'CEEN',
         'CELL', 'CENS', 'CHBE', 'CHEM', 'CHIL', 'CHIN', 'CICS', 'CIVL',
         'CLCH', 'CLST', 'CNPS', 'CNRS', 'CNTO', 'COEC', 'COGS', 'COHR',
         'COMM', 'COMR', 'CONS', 'CPEN', 'CPSC', 'CRWR', 'CSIS', 'CSPW',
         'CTLN', 'DANI', 'DENT', 'DERM', 'DES', 'DHYG', 'DMED', 'DSCI',
         'ECED', 'ECON', 'ECPS', 'EDCP', 'EDST', 'EDUC', 'EECE', 'ELEC',
         'ELI', 'EMBA', 'ENDS', 'ENGL', 'ENPH', 'ENPP', 'ENVR', 'EOSC',
         'EPSE', 'ETEC', 'EXCH', 'EXGR', 'FACT', 'FEBC', 'FHIS', 'FIPR',
         'FISH', 'FIST', 'FMPR', 'FMST', 'FNEL', 'FNH', 'FNIS', 'FOOD',
         'FOPR', 'FRE', 'FREN', 'FRSI', 'FRST', 'FSCT', 'GBPR', 'GEM',
         'GENE', 'GEOB', 'GEOG', 'GERM', 'GPP', 'GREK', 'GRS', 'GRSJ',
         'GSAT', 'HEBR', 'HESO', 'HGSE', 'HINU', 'HIST', 'HPB', 'HUNU',
         'IAR', 'IEST', 'IGEN', 'INDE', 'INDO', 'INDS', 'INFO', 'ISCI',
         'ITAL', 'ITST', 'IWME', 'JAPN', 'JRNL', 'KIN', 'KORN', 'LAIS',
         'LARC', 'LASO', 'LAST', 'LATN', 'LAW', 'LFS', 'LIBE', 'LIBR',
         'LING', 'LLED', 'LWS', 'MATH', 'MDVL', 'MECH', 'MEDD', 'MEDG',
         'MEDI', 'MGMT', 'MICB', 'MIDW', 'MINE', 'MRNE', 'MTRL', 'MUSC',
         'NAME', 'NEST', 'NEUR', 'NRSC', 'NURS', 'OBMS', 'OBST', 'OHS',
         'ONCO', 'OPTH', 'ORNT', 'ORPA', 'OSOT', 'PAED', 'PATH', 'PCTH',
         'PERS', 'PHAR', 'PHIL', 'PHRM', 'PHTH', 'PHYL', 'PHYS', 'PLAN',
         'PLNT', 'POLI', 'POLS', 'PORT', 'PSYC', 'PSYT', 'PUNJ', 'RADI',
         'RELG', 'RES', 'RGLA', 'RHSC', 'RMST', 'RSOT', 'RUSS', 'SANS',
         'SCAN', 'SCIE', 'SEAL', 'SGES', 'SLAV', 'SOAL', 'SOCI', 'SOIL',
         'SOWK', 'SPAN', 'SPHA', 'SPPH', 'STAT', 'STS', 'SURG', 'SWED',
         'TEST', 'THTR', 'TIBT', 'TRSC', 'UDES', 'UFOR', 'UKRN', 'URO',
         'URST', 'URSY', 'VANT', 'VGRD', 'VISA', 'VRHC', 'VURS', 'WOOD',
         'WRDS', 'WRIT', 'ZOOL']

def find_dept_and_number(name):
    return (name.split(" ")[0], name.split(" ")[1])

class Course(object):
    def __init__(self, name, title, description, prereqs, coreqs):
        self.name = name
        self.title = title
        self.description = description
        self.prereqs = prereqs or ""
        self.coreqs = coreqs or ""
    def __str__(self):
        myStr = "%s\n\tDsc: %s\n\tPr: %s\n\tCo: %s\n" % (self.title, self.description, self.prereqs, self.coreqs)
        return "".join(s for s in myStr if s in string.printable)

def build_db(btree):
    for dept in DEPTS:
        page = requests.get("https://courses.students.ubc.ca/cs/main?pname=subjarea&req=1&dept=%s" % dept)
        tree = html.fromstring(page.content)
        tdd = tree.xpath("//td")
        postreqs = []
        for td in tdd:
            if td.text_content().startswith(dept):
                name = td.text_content() #.replace(" ", "")
                course_page = requests.get("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=3&dept=%s&course=%s" % find_dept_and_number(name))
                course_tree = html.fromstring(course_page.content)
                pp = course_tree.xpath('//p')
                prereqs, coreqs = "", ""
                for p in pp:
                    if p.text_content().startswith("Pre-reqs:"):
                    	prereqs = p.text_content().strip("Pre-reqs:").strip()
                    if p.text_content().startswith("Co-reqs:"):
                    	coreqs = p.text_content().strip("Co-reqs:").strip()
                try:
                    description = pp[0].text_content().split("Please")[0].strip().split("Consult ")[0].strip("(") #TODO: possibly change this to raw description from site.
                    title = course_tree.xpath('//h4/text()')[0]
                except IndexError:
                    description = ""
                    title = ""
                btree.insert(Course(name, title, description, prereqs, coreqs))
                print '\r' + name,
                sys.stdout.flush()
    print '\r' + " "*8 + '\r',
    return btree

if __name__ == "__main__":
    Courses = build_db(BTree(15))
    print Courses
