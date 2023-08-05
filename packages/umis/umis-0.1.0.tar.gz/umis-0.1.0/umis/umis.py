#!/usr/bin/env python

import itertools
import collections
import re
import json
import gzip
import sys

import click


def stream_fastq(file_handler):
    ''' Generator which gives all four lines if a fastq read as one string
    '''
    next_element = ''
    for i, line in enumerate(file_handler):
        next_element += line
        if i % 4 == 3:
            yield next_element
            next_element =''


@click.command()
@click.argument('transform', required=True)
@click.argument('fastq1', required=True)
@click.argument('fastq2', default=None, required=False)
@click.option('--demuxed_cb', default=None)
def fastqtransform(transform, fastq1, fastq2, demuxed_cb):
    ''' Transform input reads to the tagcounts compatible read layout using regular expressions
    as defined in a transform file. Outputs new format to stdout.
    '''
    read_template = '{name}:CELL_{CB}:UMI_{MB}\n{seq}\n+\n{qual}\n'

    transform = json.load(open(transform))
    read1_regex = re.compile(transform['read1'])
    read2_regex = re.compile(transform['read2']) if fastq2 else None

    fastq1_fh = open(fastq1)
    if fastq1.endswith('gz'):
        fastq1_fh = gzip.GzipFile(fileobj=fastq1_fh)

    fastq_file1 = stream_fastq(fastq1_fh)

    if fastq2:
        fastq2_fh = open(fastq2)
        if fastq2.endswith('gz'):
            fastq2_fh = gzip.GzipFile(fileobj=fastq2_fh)

        fastq_file2 = stream_fastq(fastq2_fh)

    else:
        fastq_file2 = itertools.cycle((None,))

    for read1, read2 in itertools.izip(fastq_file1, fastq_file2):
        # Parse the reads with the regexes
        read1_match = read1_regex.search(read1)
        if not read1_match:
            continue

        read1_dict = read1_match.groupdict()

        if fastq2:
            read2_match = read2_regex.search(read2)
            if not read2_match:
                continue

            read2_dict = read2_match.groupdict()

        else:
            read2_dict = dict()

        read1_dict.update(read2_dict)

        if demuxed_cb:
            read1_dict['CB'] = demuxed_cb

        # Output the restrutured read
        sys.stdout.write(read_template.format(**read1_dict))


@click.command()
@click.argument('genemap', required=False)
@click.argument('sam', type=click.File('r'))
@click.argument('out')
@click.option('--output_evidence_table', default=None)
@click.option('--positional', default=False)
def tagcount(genemap, sam, out, output_evidence_table, positional):
    ''' Count up evidence for tagged molecules
    '''
    from simplesam import Reader
    from cStringIO import StringIO
    import pandas as pd

    gene_map = None
    if genemap:
        with open(genemap) as fh:
            gene_map = dict(p.strip().split() for p in fh)

    sam_file = Reader(sam)

    parser_re = re.compile('(.*):CELL_(?P<CB>.*):UMI_(?P<MB>.*)')

    evidence = collections.defaultdict(int)

    for i, aln in enumerate(sam_file):
        if aln.mapped:
            match = parser_re.search(aln.qname).groupdict()
            CB = match['CB']
            MB = match['MB']

            if gene_map:
                target_name = gene_map[aln.rname]
            else:
                target_name = aln.rname

            if positional:
                e_tuple = (CB, target_name, aln.pos, MB)
            else:
                e_tuple = (CB, target_name, MB)
            
            # TODO: Parsing NH should be more robust.
            nh = float(aln._tags[-1].split('NH:i:')[-1])  # Number of hits per read
            evidence[e_tuple] += 1. / nh

    buf = StringIO()
    for key in evidence:
        line = ','.join(map(str, key)) + ',' + str(evidence[key]) + '\n'
        buf.write(line)

    buf.seek(0)
    evidence_table = pd.read_csv(buf)
    evidence_table.columns=['cell', 'gene', 'umi', 'evidence']

    # TODO: Make required amount of evidence for a tagged molecule a parameter
    # TODO: How to use positional information?
    collapsed = evidence_table.query('evidence > 1').groupby(['cell', 'gene'])['umi'].size()
    expanded = collapsed.unstack().T

    genes = pd.Series(index=set(gene_map.values()))
    genes = genes.sort_index()
    genes = expanded.ix[genes.index]
    genes.replace(pd.np.nan, 0, inplace=True)

    if output_evidence_table:
        import shutil
        buf.seek(0)
        with open(output_evidence_table, 'w') as etab_fh:
            shutil.copyfileobj(buf, etab_fh)

    genes.to_csv(out)


@click.group()
def umis():
    pass

umis.add_command(fastqtransform)
umis.add_command(tagcount)
