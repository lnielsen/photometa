"""Dirty script to parse filenames and fix creation date of photos."""

import os
import click
from libxmp import XMPFiles, consts
import re
from datetime import datetime
from fnmatch import fnmatch
import calendar

pattern = re.compile("^(\d{4}) (\d{2}) (\d{2})")


@click.group()
def cli():
    pass


@cli.command()
@click.argument('directory')
def run(directory):
    """Run command."""
    if not os.path.isdir(directory):
        click.ClickException("Not a directory: %s" % directory)

    for f in iter_files(directory, "*.jpg"):
        date = parse_filename(os.path.basename(f))
        if date:
            if embed_xmp(f, date):
                click.echo(os.path.basename(f))
            else:
                click.echo("Warning: Could not write date into: %s" % f)


def iter_files(ds, pat):
    """Iterate over files matching pattern."""
    for d in os.listdir(ds):
        if fnmatch(d, pat):
            yield os.path.join(ds, d)


def parse_filename(name):
    """Parse date from filename."""
    m = pattern.match(name)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def embed_xmp(filename, dt):
    t = calendar.timegm(dt.timetuple())
    os.utime(filename, (t, t))
    os.system('SetFile -d "%s" "%s"' % (
        dt.strftime("%m/%d/%Y 00:00:00"),
        filename.encode('utf-8'),
    ))

    xmpfile = XMPFiles(file_path=filename, open_forupdate=True)
    xmp = xmpfile.get_xmp()

    xmp.set_property(
        consts.XMP_NS_XMP,
        "CreateDate",
        dt.isoformat()
    )

    if xmpfile.can_put_xmp(xmp):
        xmpfile.put_xmp(xmp)
        xmpfile.close_file()
        return True
    else:
        xmpfile.close()
        return False

if __name__ == "__main__":
    cli()
