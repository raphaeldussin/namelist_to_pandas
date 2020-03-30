import pandas as pd


def parse_namelist(nmlfile, runname):
    """parse MOM namelist and turn it into a pandas DataFrame

    Arguments:
        nmlfile {str} -- namelist to convert
        runname {str} -- name of the experiment

    Returns:
        pandas.DataFrame -- dataframe of namelist parameters
    """
    lines = get_lines(nmlfile)
    lines = exclude_commented_lines(lines)
    lines = exclude_trailing_comments(lines)
    lines = only_affectation_lines(lines)
    dict_nml = create_dict_from_lines(lines)

    dict_nml.update({'RUN': runname})
    serie = pd.Series(dict_nml)
    df = serie.to_frame()
    return df


def create_dict_from_lines(lines):
    """turn a list of X = something lines into a dictionary

    Arguments:
        lines {list} -- lines to convert

    Returns:
        dict -- namelist param = values
    """
    dict_nml = {}
    for line in lines:
        words = line.replace('=', ' ').split()
        key = words[0]
        if len(words) > 2:
            values = "".join(words[1:])
        else:
            values = words[1]
        dict_nml.update({key: values})
    return dict_nml


def get_lines(nmlfile):
    """read file

    Arguments:
        nmlfile {str} -- text file to read

    Returns:
        list -- contents
    """
    f = open(nmlfile, 'r')
    lines = f.readlines()
    f.close()
    return lines


def exclude_commented_lines(lines):
    """remove all lines starting with comment key !

    Arguments:
        lines {list} -- lines with commented lines

    Returns:
        list -- lines without commented lines
    """
    out = []
    for line in lines:
        line_no_leadspace = line.lstrip()
        if len(line_no_leadspace) == 0:
            pass  # remove empty lines
        else:
            if line_no_leadspace[0] == '!':
                pass
            else:
                out.append(line)
    return out


def exclude_trailing_comments(lines):
    """remove comments after param = value

    Arguments:
        lines {list} -- lines with trailing comments

    Returns:
        list -- lines without trailing comments
    """
    out = []
    for line in lines:
        comment_char_index = line.find('!')
        if comment_char_index != -1:
            newline = line[:comment_char_index]
        else:
            newline = line
        out.append(newline)
    return out


def only_affectation_lines(lines):
    """keep only lines with param = value

    Arguments:
        lines {list} -- lines to process

    Returns:
        list -- lines containing =
    """
    out = []
    for line in lines:
        if line.find('=') != -1:
            out.append(line)
    return out
