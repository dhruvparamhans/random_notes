#!/usr/bin/env python

# Backtracking SAT-solver with watched literals (dennis(a)yurichev.com)

# I've written it to be sure I understood watched literals well

# other implementations:
# https://www-cs-faculty.stanford.edu/~knuth/programs/sat0w.w
# http://sahandsaba.com/understanding-sat-by-implementing-a-simple-sat-solver-in-python.html

# my previous backtracking SAT-solver written in Python: https://yurichev.com/blog/SAT_backtrack/

import sys, copy

def read_text_file (fname):
    with open(fname) as f:
        content = f.readlines()
    return [x.strip() for x in content] 

def read_DIMACS (fname):
    content=read_text_file(fname)

    header=content[0].split(" ")

    assert header[0]=="p" and header[1]=="cnf"
    variables_total, clauses_total = int(header[2]), int(header[3])

    # array idx=number (of line) of clause
    # val=list of terms
    # term can be negative signed integer
    clauses=[]
    for c in content[1:]:
        clause=[]
        for var_s in c.split(" "):
            var=int(var_s)
            if var!=0:
                clause.append(var)
        clauses.append(clause)

    # key=literal
    # val=list of numbers of clause
    literals_idx={}
    for i in range(len(clauses)):
        for literal in clauses[i]:
            literals_idx.setdefault(literal, []).append(i)

    return clauses, literals_idx

clauses, literals_idx = read_DIMACS(sys.argv[1])
clauses_t=len(clauses)
literals_t=len(literals_idx)
vars_t=literals_t/2

# for each clause
# idx=clause#
# 0th is default
current_watchees=[0]*clauses_t

# k=literal
# v=list tuples: (clause#, idx)
WL={}

# initial WL:
for l in literals_idx.keys():
    WL[l]=literals_idx[l]

def find_true_or_unknown_literals_for_partial_assignment (assignment, clause):
    rt=[]
    for c in clause:
        try:
            if c>0:
                rt.append(assignment[c-1])
            if c<0:
                rt.append(not assignment[abs(c)-1])
        except IndexError:
            rt.append(True)

    #print "find_true_literals_for_partial_assignment", assignment, clause, rt
    assert len(clause)==len(rt)
    return rt

def swap_watchee_in_clause_for_literal (assignment, clause_n, literal):
    global current_watchees, WL

    # set watchee to any literal which is TRUE under current partial assignment
    possible_watchees=find_true_or_unknown_literals_for_partial_assignment(assignment, clauses[clause_n])
    if True not in possible_watchees:
        #print "can't find new watchee for clause# ", clause_n
        return False, None
    # new watchee (pick first available):
    #print "possible watches:", possible_watchees
    idx=possible_watchees.index(True)
    #print "new watchee for clause# ", clause_n, " is ", idx, " (was ", current_watchees[clause_n], ")"
    current_watchees[clause_n]=idx
    new_literal=clauses[clause_n][idx]
    return True, new_literal

def swap_watchees_for_literal (assignment, literal, clauses_to_swap):
    global WL, current_watchees

    #print "swap_watchees_for_literal(). clauses_to_swap=", clauses_to_swap
    c=0
    for clause in clauses_to_swap:
        #print "(going to swap) literal", literal, "clause#", clause
        rt=swap_watchee_in_clause_for_literal (assignment, clause, literal)
        if rt[0]==False:
            return False
        else:
            clause_n=WL[literal][c]
            # new literal is in rt[1]:
            if clause_n not in WL[rt[1]]:
                WL[rt[1]].append(clause_n)
        c=c+1
    # remove all clauses from the WL for this literal (i.e., they all were swapped)
    WL[literal]=[]
    return True

def print_vals(assignment):
    # enumerate all vals[]
    # prepend "-" if vals[i] is False (i.e., negated).
    print "".join([["-",""][assignment[i]] + str(i+1) + " " for i in range(len(assignment))])+"0"

solutions=0

def loop(assignment):
    global WL, current_watchees, literals_idx, solutions

    cur_var=len(assignment)+1

    # try False, then True, for new variable:
    for new_var in [False, True]:
        new_assignment=assignment+[new_var]
        #print "loop", new_assignment
        #print "WL", WL
        if new_var==True:
            # negate var on second pass (swap literals in clauses for "other" literal):
            # i.e., if new var is False, swap literals in clauses for positive literal
            # if it's True, swap them in clauses for negative literal
            cur_var=-cur_var
        if swap_watchees_for_literal (new_assignment, cur_var, copy.deepcopy(WL[cur_var])):
            # WL updated successfully at this point
            if len(new_assignment)==vars_t:
                # we finished:
                print "SAT"
                solutions=solutions+1
                print_vals (new_assignment)
                return
            loop(new_assignment)
        # at this point we realize we can't update WL
        # try True if it was False and do it again
        # or exit otherwise (step back)

    # both False/True failed, step back
    return

loop([])
print "UNSAT"
print "solutions=", solutions

