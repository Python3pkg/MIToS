from .Annotations import annotate_modification


def ncolumns(msa):
    return len(msa[0])


def coverage(sequence, reference):
    matchs = list(zip(sequence, reference))
    matchs = [residues for residues in matchs if residues[0] not in ['-', '.']]
    count = sum([residues[0].lower() == residues[1].lower() for residues in matchs])
    return count / float(len(matchs))


def filtersequences(msa, condition, annotate):
    msa.__dict__['_records'] = list(filter(condition, msa.__dict__['_records']))
    return msa


def nsequences(msa):
    return len(msa[:,0])


def columngappercentage(column):
    return (column.count('-') + column.count('.')) / float(len(column))


def filtercolumns(msa, condition, annotate):
    seqs = [s.seq for s in msa]
    valid_cols = list(filter(condition, list(zip(*seqs))))
    seqs = list(zip(*valid_cols))
    for sr, s in zip(msa, seqs):
        sr.__dict__['_seq'].__dict__['_data'] = ''.join(s)
    return msa


"""
This functions deletes/filters sequences and columns/positions on the MSA on the
following order:

 - Removes all the columns/position on the MSA with gaps on the reference
 sequence (first sequence)
 - Removes all the sequences with a coverage with respect to the number of
 columns/positions on the MSA **less** than a `coveragelimit` (default to
 `0.75`: sequences with 25% of gaps)
 - Removes all the columns/position on the MSA with **more** than a `gaplimit`
 (default to `0.5`: 50% of gaps)
"""
def gapstrip(msa, reference, annotate=True, coverage_limit=0.75, gap_limit=0.5):
    reference = [r for r in msa if r.description == reference]
    if not reference:
        raise Exception("Unknonw reference {:} inside the MSA.".format(reference))
    else:
        reference = reference[0]
    # Remove sequences with pour coverage of the reference sequence
    if ncolumns(msa) != 0:
        annotate and annotate_modification(msa, "gapstrip! : Deletes columns with "
                                           " gaps on the reference sequence.")
        msa = filtersequences(msa,
                              lambda s: coverage(s.seq, reference) >= coverage_limit,
                              annotate)
    else:
        raise Exception("There isn't columns in the MSA after the gap trimming.")
    # Remove columns with a porcentage of gap greater than gaplimit
    if nsequences(msa) != 0:
        message = ("gapstrip! : Deletes columns with more than {:} "
                   "gaps.".format(gap_limit))
        annotate and annotate_modification(msa, message)
        msa = filtercolumns(msa,
                            lambda c: columngappercentage(c) <= gap_limit,
                            annotate)
    else:
        raise Exception("There isn't sequences in the MSA after coverage filter.")
    return msa
