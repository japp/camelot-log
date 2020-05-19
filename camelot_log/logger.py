from os.path import basename, exists, normpath
from pathlib import Path
from astropy.table import Table, vstack
from astropy.io import fits
import io
from glob import glob
import os
from datetime import datetime as dt

def set_directories(directories, config):
    """
    Set the default directories in the config file.

    Parameters
    ----------
    directory : Path
        Base directory Path.
    args : argparse.args
        args object from argparse.

    """
    
    config['directories']['default'] = directories

    with open(os.path.dirname(os.path.abspath(__file__)) + '/config.ini', 'w') as configfile: 
        config.write(configfile)


def read_directories(directory, args):
    """
    Creates an index page for a base directory index.html containing
    a list of the daily logs.

    Parameters
    ----------

    directory : Path
        Base directory Path.
    args : argparse.args
        args object from argparse.

    """

    directory_name = basename(normpath(directory))

    if args.verbose:
        print("Reading", directory_name)

    impath = Path('.') / directory
    logfile = impath / "camelot-log.html"

    if not impath.exists():
        if args.verbose:
            print("ERROR:", basename(normpath(directory)), "not found")

    if logfile.exists():
        log_table = Table.read(logfile)
        files_in_log = log_table['NAME'].data
    else:
        files_in_log = []

    if args.all:
        images = impath.glob('*.fits')
    else:
        # Read only the new images
        images = {filename.name for filename in impath.glob('*.fits')} - set(files_in_log)

    names = ['NAME', 'OBJECT', 'DATE-OBS', 'RA', 'DEC', 'INSFILTE', 'EXPTIME',
             'AIRMASS', 'HUMIDITY', 'DUST', 'TELFOCUS', 'OBSERVER', 'RMODE']       

    tabla = Table(names=names, dtype=('S16', 'S16', 'S32', 'S32', 'S32', 'S8', 'f4',
                                      'f4', 'f4', 'f4', 'i4', 'S32', 'i4'))

    tabla['AIRMASS'].format = '%.2f'
    tabla['HUMIDITY'].format = '%.1f'
    tabla['DUST'].format = '%.4f'

    for image in images:

        image = impath / image
        
        try:
            hdr = fits.getheader(image)

            # Filename
            row = [basename(image)]
          
            # Rest of keywords
            for key in names[1:]:
                try:
                    value = hdr[key]
                    row.append(value)
                except:
                    row.append(9999)

            tabla.add_row(row)
        except:  
            if args.verbose:
                print("ERROR: ", image, "failed")
            pass

    # Join with the existing table log if exists
    if logfile.exists():
        tabla = vstack([log_table, tabla])

    tabla.sort('DATE-OBS')

    if len(tabla) > 0:

        # Plain text log
        logfile_csv = impath / "camelot.log" 
        tabla.write(logfile_csv, format="ascii.fixed_width", delimiter=False, overwrite=True)

        # HMTL log
        fh = io.StringIO()
        tabla.write(fh, format="html")

        content = fh.getvalue()

        header = """
        <head>
        <meta http-equiv="refresh" content="60" />
        <link rel="stylesheet" href="http://carlota:82/sieinvens/libs/bs/css/bootstrap320.min.css">

        """

        content = content.replace('<table>', '<h2>{}</h2><table class="table table-striped">\n'.format(directory_name))
        content = content.replace('<head>', header)

        logfile.write_text(content)

    if args.verbose:
        print("{} images found\n".format(len(tabla)))


def create_index(directory):
    """
    Creates an index page for a base directory index.html containing
    a list of the daily logs.

    Parameters
    ----------

    directory : str
        Base directory where create the index file.

    """

    template = """
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
    <head>
        <link rel="stylesheet" href="http://carlota:82/sieinvens/libs/bs/css/bootstrap320.min.css">
        <meta charset="utf-8"/>
        <meta http-equiv="refresh" content="60" />
        <meta content="text/html;charset=UTF-8" http-equiv="Content-type"/>
        <style>
        h1 {{
            margin-bottom: 20px;
        }}
        li {{
            font-size: 18px;
        }}
        </style>
    </head>
    <body>
    <div class="container">
    <nav class="navbar navbar-default">
        <div class="container">
            <div class="navbar-header" style="width: 100%">
                <div class="row">
                    <div class="col-md-1">
                        <img style="margin-top:5px" src="https://www.iac.es/themes/custom/da_vinci/logo.svg" height="75"/>
                    </div>
                    <div class="col-md-8">
                        <h2>CAMELOT2 log - <code>{title}</code></h2>
                    </div>
                    <div class="col-md-2 text-right">
                        <p><strong>{datetime}</strong></p>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    {content}
    </div>
    </body>
    </html>
    """

    now = dt.now().isoformat()[:-10]
    directory_base = directory.split("/")[-1]

    subdirectories = glob(directory + '/' + '[0-9][0-9]???[0-9][0-9]')

    #title = "<h1>{}</h1>\n".format(basename(directory))

    content = "    <ul class='list-group' style='width: 40%;'>\n"
    for subdir in subdirectories:
        content += "      <li  class='list-group-item'><a href='{subdir}/camelot-log.html'>{subdir}</a></li>\n".format(subdir=basename(subdir))
    content += "    </ul>\n"
    
    index = Path(directory + "/index.html")

    index.write_text(template.format(title=directory_base, datetime=now, content=content))