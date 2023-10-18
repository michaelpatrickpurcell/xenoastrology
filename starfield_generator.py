import tikz
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist

from pylatex import Document, TikZ
from pylatex import Package, Command
from pylatex.utils import italic, bold, NoEscape
from pylatex.basic import NewLine

def generate_starfield_points(seed=None):
    alpha = 0.1
    min_dist = 5
    ngroups=25
    nppg = 6
    npoints = ngroups*nppg
    ibox_size = 10
    max_height = 90

    if seed is None:
        seed = np.random.randint(2**31)
    print('Initial seed = %i' % seed)
    np.random.seed(seed)

    while 1:
        points = ibox_size*np.random.random(size=(npoints,2)) - ibox_size/2
        iter = 0
        dist_mat = pdist(points)
        while np.min(dist_mat) < min_dist:
            updates = np.zeros(points.shape)
            for i,point in enumerate(points):
                diffs = point - points
                norms = np.linalg.norm(diffs, axis=1, keepdims=True)
                directions = np.nan_to_num(diffs/norms)
                forces = alpha * directions * np.nan_to_num(1/norms**(1))
                updates[i] = np.sum(forces, axis=0)

            points += updates
            dist_mat = pdist(points)
            iter += 1
        if np.max(points[:,1]) - np.min(points[:,1]) > max_height:
            print('reseeding')
            seed = np.random.randint(2**31)
            np.random.seed(seed)        
            print('New seed = %i' % seed)
        else:
            break

    return points, seed

def generate_starfield_tikzpicture(points):
    color_list = ['OffBlack'] * 6

    pic = tikz.Picture()
    pic.usetikzlibrary('shapes.geometric')

    pic.node(r'\phantom{1}', at=(0,0), circle=True, minimum_width='160mm')


    for point in points[:6]:
        pic.node(r'\phantom{1}', at=tuple(point/6), draw=color_list[0], circle=True, inner_sep='1.875pt', line_width='0.9mm')

    for point in points[6:12]:
        pic.node(r'\rule{7mm}{1mm}', at=tuple(point/6), text=color_list[1], rotate=45, inner_sep='0pt')
        pic.node(r'\rule{7mm}{1mm}', at=tuple(point/6), text=color_list[1], rotate=-45, inner_sep='0pt')

    for point in points[12:18]:
        pic.node(r'\phantom{1}', at=tuple(point/6), regular_polygon=True, regular_polygon_sides=3, fill=color_list[2], inner_sep='0.0pt')

    for point in points[18:24]:
        pic.node(r'\phantom{1}', at=tuple(point/6), draw=color_list[3], diamond=True, inner_sep='0.8pt', line_width='0.9mm')

    for point in points[24:30]:
        pic.node(r'\phantom{1}', at=tuple(point/6), star=True, star_points=5, star_point_ratio=2, fill=color_list[4], inner_sep='0.3pt')

    for point in points[30:36]:
        pic.node(r'\phantom{1}', at=tuple(point/6), regular_polygon=True, regular_polygon_sides=6, fill=color_list[5], inner_sep='2.2pt')

    for i in range(6,9):
        for point in points[6*i:6*(i+1)]:
            pic.node('', at=tuple(point/6), draw='white', circle=True, fill='lightgray', inner_sep='3pt')
            
    for i in range(9,13):
        for point in points[6*i:6*(i+1)]:
            pic.node('', at=tuple(point/6), draw='white', circle=True, fill='lightgray', inner_sep='2pt')

    for i in range(13,17):
        for point in points[6*i:6*(i+1)]:
            pic.node('', at=tuple(point/6), draw='white', circle=True, fill='lightgray', inner_sep='1.5pt')

    # pic.node(r'\setmainfont[Scale=1.6]{Ubuntu}\Huge X', at=(8.25, -8.25), text='lightgray!50')
    # pic.node('', at=(8.25, -8.25), draw='black', ultra_thick=True, minimum_size='10mm', rounded_corners='2mm')
    # pic.node(r'\setmainfont[Scale=1.6]{Ubuntu}\Huge X', at=(8.25, -7.0), text='lightgray!50')
    # pic.node('', at=(8.25, -7.0), draw='black', ultra_thick=True, minimum_size='10mm', rounded_corners='2mm')
    # pic.node(r'\setmainfont[Scale=1.6]{Ubuntu}\Huge X', at=(8.25, -5.75), text='lightgray!50')
    # pic.node('', at=(8.25, -5.75), draw='black', ultra_thick=True, minimum_size='10mm', rounded_corners='2mm')

    tikzpicture = pic.code()

    return tikzpicture

def save_starfield_tikzpicture(tikzpicture, filename):
    f = open('filename', 'w')
    f.write(tikzpicture)
    f.close()

def generate_latex_doc(tikzpicture, seed):
    geometry_options = {'margin': '10mm'}
    doc = Document(documentclass = 'scrartcl',
                document_options = ["paper=a4","parskip=half"],
                fontenc=None,
                inputenc=None,
                lmodern=False,
                textcomp=False,
                page_numbers=False,
                geometry_options=geometry_options)

    doc.packages.append(Package('tikz'))
    doc.packages.append(Package('fontspec'))
    doc.packages.append(Package('enumitem'))
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('booktabs'))
    doc.packages.append(Package('epsdice'))
    doc.packages.append(Package('astrollogy'))

    doc.preamble.append(Command('usetikzlibrary', 'shapes.geometric'))
    doc.preamble.append(Command('setkomafont', NoEscape(r'section}{\setmainfont{Century Gothic}\LARGE\bfseries\center')))
    doc.preamble.append(Command('RedeclareSectionCommand', 'section', ([r'runin=false', NoEscape(r'afterskip=0.0\baselineskip'), NoEscape(r'beforeskip=1.0\baselineskip')])))
    doc.change_length("\columnsep", "10mm")

    doc.append(Command(NoEscape(r'begin{center}')))
    doc.append(NoEscape(tikzpicture))
    doc.append(Command(NoEscape(r'end{center}')))

    doc.append(Command(r'vspace{-8.5mm}'))

    doc.append(NoEscape(r'\begin{center}\includegraphics[width=155mm]{Images/ASTROLLOGY_Logo.eps}\end{center}'))

    doc.append(Command(r'vspace{-1mm}'))
    doc.append(Command(NoEscape(r'setmainfont[Scale=0.95]{Century Gothic}')))
    doc.append(Command(NoEscape(r'raggedright')))

    doc.append(Command(r'begin{multicols}{2}'))
    f = open('astrollogy_rules_text.tex')
    rules_text = f.read()
    f.close()
    doc.append(NoEscape(rules_text))
    doc.append(Command(r'vfill'))
    doc.append(NoEscape(r"\textbf{Random Seed:} %i\\\textbf{Design:} Michael~Purcell, Kyle~``KYNG''~Jarratt\vfill\null" % seed))
    doc.append(Command(r'end{multicols}'))

    doc.append(Command(r'vspace{-7.5mm}'))

    doc.append(NoEscape(r'{\Huge \dieone{} = \tikz{\pic {onestar}} \hfill \dietwo{} = \tikz{\pic {twostar}} \hfill \diethree{} = \tikz{\pic {threestar}} \hfill \diefour{} = \tikz{\pic {fourstar}} \hfill \diefive{} = \tikz{\pic {fivestar}} \hfill \diesix{} = \tikz{\pic {sixstar}}}'))

    return doc

def save_latex_doc(latex_doc, seed):
    latex_doc.generate_pdf('astrollogy_starfield_%i' % seed, compiler='xelatex')

if __name__ == '__main__':
    # seed = 1839123614
    # seed = 643267061
    seed = None
    points, seed = generate_starfield_points(seed=seed)
    print(seed)
    tikzpicture = generate_starfield_tikzpicture(points=points)
    # save_starfield_tikzpicture(tikzpicture=tikzpicture, filename='starfield_diagram_minimal.pdf')
    latex_doc = generate_latex_doc(tikzpicture, seed)
    save_latex_doc(latex_doc, seed)