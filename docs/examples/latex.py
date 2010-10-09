import os
from simplepyged import *

def name(person):
    if person is None:
        return ""
    return str(person.surname()) + ", " + str(person.given_name())

def name_link_html(person, prefix=""):
    return "<a href=\"#" + prefix + str(person.pointer()) + "\">" + name(person) + "</a> "

def name_link_latex(person, prefix=""):
    return name(person) + ' (str. \pageref{' + prefix + str(person.pointer()) + '})'

def link_latex(element, prefix=""):
    if element == None:
        return ""
    return '$^{\pageref{' + prefix + str(element.pointer()) + '}}$ '

def link_latex_index(element, prefix=""):
    if element == None:
        return ""
    return '\pageref{' + prefix + str(element.pointer()) + '}'

def anchor(person):
    return "[" + str(person.pointer()) + "] "

def anchor_html(person, prefix=""):
    if person == None:
        return "__________"
    return "<a name=\"" + prefix + str(person.pointer()) + "\"></a> "

def anchor_latex(person, prefix=""):
    return '\label{' + prefix + str(person.pointer()) + '}'

def text(family):
    retval = ""
    retval += anchor(family.husband()) + "Husband: " + name(family.husband()) + "\n"
    retval += anchor(family.wife()) + "Wife: " + name(family.wife()) + "\n"
    for c in family.children():
        retval += anchor(c) + "Child: " + name(c) + "\n"
    retval += "\n"
    retval += "\n"

    return retval

def start_latex():
    retval = ''
    retval += '\documentstyle[12pt]{article}\\begin{document}' + "\n"
    return retval

def latex(family):
    retval = ''
    retval += anchor_latex(family) + "\n"
    retval += '\\begin{tabular*}{0.9\\textwidth}{ | l | l | }' + "\n"
#    retval += '\\begin{tabular}{ l r }' + "\n"
    retval += 'Husband '
    retval += ' & '
    retval += 'Wife '
    retval += ' \\\\ ' + "\n"
    if family.husband() is not None:
        retval += name(family.husband()) + link_latex(family.husband().parent_family())
    retval += ' & '
    if family.wife() is not None:
        retval += name(family.wife()) + link_latex(family.wife().parent_family())
    retval += ' \\\\ ' + "\n"
    if family.husband() is not None:
        retval += str(family.husband().birth()[0])
    retval += ' & '
    if family.wife() is not None:
        retval += str(family.wife().birth()[0])
    retval += ' \\\\ ' + "\n"
    if family.husband() is not None:
        retval += str(family.husband().birth()[1])
    retval += ' & '
    if family.wife() is not None:
        retval += str(family.wife().birth()[1])
    retval += ' \\\\ ' + "\n"
    retval += ' \\\\ ' + "\n"
    if family.husband() is not None:
        retval += str(family.husband().death()[0])
    retval += ' & '
    if family.wife() is not None:
        retval += str(family.wife().death()[0])
    retval += ' \\\\ ' + "\n"
    if family.husband() is not None:
        retval += str(family.husband().death()[1])
    retval += ' & '
    if family.wife() is not None:
        retval += str(family.wife().death()[1])
    retval += ' \\\\ ' + "\n"
    retval += '\end{tabular*}' + "\n\n"

    retval += '\\paragraph{}' + "\n"
    retval += 'Married: ' + '' + "\n\n"

    retval += '\\paragraph{}' + "\n\n"
    retval += '\\begin{center}Children\end{center}' + '' + "\n\n"
    for i in range(1, len(family.children()) + 1):
        c = family.children()[i - 1]
        retval += '\\paragraph{}' + "\n"
        retval += str(i) + '. ' + name(c)
        for f in c.families():
            retval += link_latex(f)
        retval += "\n\n"
        if c.birth() != ('',''):
            retval += "\tBorn: " + str(c.birth()) + "\n\n"
        if c.death() != ('',''):
            retval += "\tDied: " + str(c.death()) + "\n\n"
        if len(c.children()) > 0:
            retval += "\tChildren: " + str(len(c.children())) + "\n\n"
        retval += "\n\n"

    retval += '\\newpage' + "\n\n"
    return retval

def end_latex():
    retval = ''
    retval += '\end{document}'
    return retval

def print_stack(fn, stack):
    retval = ""
    for family in stack:
        retval += fn(family)

    return retval

def push(stack, item):
    if item == None:
        return stack

    if item in stack:
        return stack

    stack.append(item)
    return stack

def construct_stack(stack, depth):
    if depth == 0:
        return []
    if stack == []:
        return []

    for family in stack:
        if family == None:
            continue
        addendum = []
        for p in family.parents():
            addendum = push(addendum, p.parent_family())
        for c in family.children():
            for f in c.families():
                addendum = push(addendum, f)

    expanded_family = construct_stack(addendum, depth - 1)

    for e in expanded_family:
        stack = push(stack, e)

    return stack

def latex_index(stack):
    individuals = []
    for family in stack:
        for p in family.parents():
            individuals = push(individuals, p)
        for c in family.children():
            individuals = push(individuals, c)

    individuals = sorted(individuals, key=name)

    retval = ""
    for i in individuals:
        if i.given_name() == '' and i.surname() == '':
            continue
        retval += '\\begin{tabular*}{0.9\\textwidth}{  l  r  }' + "\n"
        retval += name(i) + " "
        retval += ' & '
        pages = []
        if i.parent_family() is not None:
            pages = push(pages, link_latex_index(i.parent_family()))
        for f in i.families():
            if f is not None:
                pages = push(pages, link_latex_index(f))

        retval += ', '.join(pages)
        retval += ' \\\\ ' + "\n"

        retval += '\end{tabular*}' + "\n\n"

    return retval

#g = Gedcom(os.path.abspath('mcintyre.ged'))
g = Gedcom(os.path.abspath('moje.ged'))
#fam = g.get_family('@F5@')
#stack = [fam]
#stack = construct_stack(stack, 6)

stack = g.family_list()

print start_latex()
print print_stack(latex, stack)
print latex_index(stack)
print end_latex()
