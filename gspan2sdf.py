__author__ = 'cwestrup'

import argparse
import logging

# names of atom names in order.
ATOM_LIST = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg",
             "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr",
             "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br",
             "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd",
             "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "Hf",
             "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi",
             "Po", "At", "Rn", "Fr", "Ra", "Pt", "Ac", "La", "U", "Sm", "Ce",
             "Nd", "Eu", "Gd", "Dy", "Er", "Rh"]


def parseargs():
  """Parse command line arguments.
  """
  parser = argparse.ArgumentParser(
    description='Converts graphs from a gspan dataset into sdf files.')
  parser.add_argument(
    '-i', '--input', type=str, dest='input',
    required=True, help='path to input gspan file (e.g. mydata.gspan)')
  parser.add_argument(
    '-o', '--output', type=str, dest='output',
    required=True, help='path to directory to store output sdf files.')
  parser.add_argument(
    '-a', '--atom_shift', dest='atom_shift', action='store_true',
    help='If this flag is set all atom labels are shifted by one, meaning '
         'e.g. an atom indexed by 0 (normally "H") would now be "He"')
  parser.add_argument(
    '-b', '--bond_shift', dest='bond_shift', action='store_true',
    help='If this flag is set the atom numbers in the bonds will be '
         'increased by one (e.g. when the labeling in gspan starts '
         'at 0 it now starts with 1 which is compliant with the sdf format')
  parser.add_argument(
    '-v', '--verbose', dest='verbose', action='store_true',
    help='show verbose information')

  args = parser.parse_args()
  return args


# main function
if __name__ == '__main__':

  # parse input arguments
  args = parseargs()
  input = args.input
  output = args.output

  # get logger and set it up
  logging.basicConfig(level=logging.INFO,
                      format="%(levelname)s - %(message)s")
  logger = logging.getLogger()
  # show debug level log messages if verbose is set
  if (args.verbose):
    logger.setLevel(logging.DEBUG)

  # add folder extension for output files
  if not output.endswith('/'):
    output = output + '/'


  # read input file and convert it to a list of lines
  with open(args.input, 'r') as input_file:
    input_list = input_file.read().splitlines()

  logger.info("Converting gspan graphs to sdf files.")


  ### iteration variables
  # index of current graph
  graph_idx = 0
  # stores the temporary string with the content for the SDF file to be written
  tmp_sdf_file = ""
  # stores the vertices / atoms part for this sdf file
  tmp_vertices = ""
  num_vertices = 0
  # stores the edges / bonds part for this sdf file
  tmp_edges = ""
  num_edges = 0


  # iterate over lines and extract and write out graph information
  for line_i, line in enumerate(input_list):

    # split current line into a list of words
    words = line.split()

    # check if end of graph, then write and go to next one
    if len(words) == 0:
      # build SDF formatted file
      tmp_sdf_file += str(num_vertices).rjust(3, " ") \
                      + str(num_edges).rjust(3, " ") \
                      + "  0  0  0  0  0  0  0  0  1 V2000" + "\n" \
                      + tmp_vertices + tmp_edges \
                      + "M  END" + "\n" + "$$$$"
      # write out to sdf file
      with open(output + str(graph_idx).rjust(6, "0") + ".sdf", 'w') as file:
        file.write(tmp_sdf_file)
      # iterate graph number
      graph_idx += 1
      # reset iteration variables
      tmp_vertices = ""
      num_vertices = 0
      tmp_edges = ""
      num_edges = 0
      tmp_sdf_file = ""

    # check if a new graph starts, indicated by t
    elif words[0] == "t":
      graph_name = words[4]
      # build first lines with header info
      # for format see http://en.wikipedia.org/wiki/Chemical_table_file
      tmp_sdf_file += graph_name + "\n" \
                      + "GSPAN_2_SDF" + "\n" \
                      + "\n"

    # check if vertex
    elif words[0] == "v":
      atom_number = int(words[2])
      if args.atom_shift: atom_number += 1
      num_vertices += 1
      tmp_vertices += "    0.0000    0.0000    0.0000 " \
                      + ATOM_LIST[atom_number].ljust(4, " ") \
                      + "0  0  0  0  0  0  0  0  0  0  0  0" + "\n"

    # check if edge
    elif words[0] == "e":
      num_edges += 1
      vertex1 = int(words[1])
      vertex2 = int(words[2])
      if args.bond_shift:
        vertex1 += 1
        vertex2 += 1
      label = str(words[3])
      tmp_edges += str(vertex1).rjust(3, " ") + str(vertex2).rjust(3, " ") \
                   + label.rjust(3, " ") + "  0  0  0  0" + "\n"

  logger.info("Done. Written " + str(graph_idx) + " sdf files.")