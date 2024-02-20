import sys
import pandas as pd
import click


CONTEXT_SETTINGS = dict(help_option_names=['-?', '-h', '--help'])


def read_peps_as_df(infile):
    records = []
    with open(infile) as f:
        for line in f:
            linelist = line.strip().split('\t')
            pid, sequences = linelist
            record = [pid] + list(sequences)
            records.append(record)

    df = pd.DataFrame(records, columns=['ID'] + list(range(1, len(records[0]))))
    
    # removing columns with identical bases
    df_cleaned = df.loc[:, ~df.apply(lambda x: x.nunique() == 1, axis=0)]
    return df_cleaned


@click.command(
    help=click.style('compare bases by columns', italic=True, fg='cyan', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
@click.option('-i', '--infile', help='the input file', type=click.Path(exists=True))
@click.option('-o', '--outfile', help='the output file', type=click.Path())
def main(infile, outfile):
    out = open(outfile, 'w') if outfile else sys.stdout
    df = read_peps_as_df(infile)
    df.to_csv(out, index=False, sep='\t')
    if outfile:
        click.secho(f'>>> save file: {outfile}', err=True, fg='green')


if __name__ == '__main__':
    main()
