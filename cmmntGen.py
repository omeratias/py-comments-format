#!/usr/bin/python
import sys, getopt

def get_footer(size):
    return '*' * (size -1) + '/'

def get_header(func_name, size):
    header = '/'
    one_side_len = (int)((size - len(func_name) - 4) / 2)
    header += '*' * one_side_len + ' ' + func_name + ' ' + '*' * (one_side_len + 1)

    return header


def gen_cmmt(func_name, lines, size):
    header = get_header(func_name, size)
    footer = get_footer(size)
    cmt = header + '\n'

    for l in lines:
        cmt += '*' + ' ' * 3 + l + ' ' * (size - len(l) - 5) + '*\n'
    cmt += footer +'\n'
    return cmt


def get_max_line(cmt):
    return max([len(i) for i in cmt])


def gen_comments(lines, outputfile):
    in_cmt = False
    cur_commnt = []
    max_line = 0
    func_name = ''
    commnents = []

    for line in lines:
        if line.find('#') != -1:
            if in_cmt:
                in_cmt = False
                commnents.append(gen_cmmt(func_name, cur_commnt, max(get_max_line(cur_commnt) + 8, 40)))
                cur_commnt = []
                func_name = ''
                
            else:
                in_cmt = True
                func_name = line.split(' ')[1]
                func_name = func_name[:len(func_name) - 1]
        else:
            cur_len = len(line) - 1
            if cur_len > max_line:
                max_line = cur_len
            cur_commnt.append(line[:cur_len])
    return commnents


def main(argv):
    input_file = ''
    output_file = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ['ifile=', 'ofile='])
        if len(opts) == 0:
            raise getopt.GetoptError('missing')
    except getopt.GetoptError:
        print 'cmmntGen.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == 'h':
            print 'cmmntGen.py -i <inputfile_path> -o <outputfile_path>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    try:
        cmmntFile = open(input_file, 'r')
    except:
        print 'the path is wrong'
        sys.exit(2)
    cmmntlines = cmmntFile.readlines()
    cmnts = gen_comments(cmmntlines, output_file)
    if len(cmnts) > 0:
        outputfile = open(output_file, 'w')
        for c in cmnts: outputfile.write(c)
        outputfile.close()

    cmmntFile.close()

if __name__ == "__main__":
    main(sys.argv[1:])
