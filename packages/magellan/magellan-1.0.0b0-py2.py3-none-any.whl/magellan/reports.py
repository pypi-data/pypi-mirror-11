#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Report code for Magellan here.
"""

# todo (aj) completely change this!

from pprint import pprint

# Logging:
import logging
maglog = logging.getLogger("magellan_logger")
maglog.info("Env imported")

def produce_pdp_package_report(
        package, piptree, piperrs, file_template="Mag_Report_{}.txt"):
    """
    Generates a report based on a specific package
    
    :param str package: name of the package to produce report for
    :param dict piptree: parsed output from pipdeptree
    :param dict piperrs: parsed error output from pipdeptree
    """
    
    search_package = package + ' '
    
    # From output:
    nodes = [x for x in piptree['nodes'] if package == x[0]]
    deps = {}
    for l in piptree['dependencies']: 
        if search_package in str(piptree['dependencies'][l]):
            dep_root = l
            deps[dep_root] = piptree['dependencies'][l]

    no_tree = False
    if not nodes and not deps:
        no_tree = True
        maglog.info("No nodes or dependencies found for {}".format(package))

    # From errs:
    e_nodes = []
    e_deps = {}
    if package in piperrs.keys():
        e_nodes = piperrs[package]
    
    for k in piperrs:
        tmp_l = [(k, x) for x in piperrs[k] if package == x[0].strip()]
        if tmp_l:
            root = tmp_l[0][0]
            pv = tmp_l[0][1]
            req = piperrs[root][pv]
            e_deps[root] = [pv, req, piperrs[root]]
        
    no_errs = False
    if not e_nodes and not e_deps:
        no_errs = True
        maglog.info("No conflict information found for {}".format(package))

    # Exit if nothing to report.
    if no_tree and no_errs:
        return None
    
    # Actually output to a file:
    write_file = file_template.format(package)
    maglog.info("Generating report for: {0} as file: {1}"
                .format(package, write_file))
    with open(write_file, 'w') as f:
        # NAME:
        f.write("Package: {}".format(package))
        f.write('\n'*2)
        
        # PIPDEPTREE TREE
        f.write("PipDepTree Output: \n")
        f.write("-"*50 + "\n")
        
        f.write("Root node:" + '\n')
        pprint(nodes, stream=f)
        f.write('\n'*2)
        f.write("Dependencies and sub-dependencies:" + '\n')
        f.write("-"*50 + "\n")
        pprint(deps, stream=f)
        
        # PIPDEPTREE ERRS
        f.write('\n'*2)
        f.write("PipDepTree Conflicts/Confusing Dependencies:" + "\n"*2)
        f.write("-"*50 + "\n")
        f.write("These depend on {0}:\n".format(package))
        for k in e_nodes:
            f.write("{0} : with {1} dependency requirements {2} \n"
                    .format(k, package, e_nodes[k]))
        f.write('\n'*2)
        
        for k in e_deps:
            f.write("These are depended on by {0}:\n".format(e_deps[k][0]))
            f.write(k + " ")
            f.write("{}\n".format(e_deps[k][1]))
            f.write("\n Full ancestor requirements list for {}:\n".format(k))
            pprint(e_deps[k][2], stream=f)
