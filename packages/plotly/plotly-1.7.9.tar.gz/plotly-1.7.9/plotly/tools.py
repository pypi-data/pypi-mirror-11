# -*- coding: utf-8 -*-

"""
tools
=====

Functions that USERS will possibly want access to.

"""
from __future__ import absolute_import

import os.path
import warnings

import six

import math


from plotly import utils
from plotly import exceptions
from plotly import session

from plotly.graph_objs import graph_objs
from plotly.graph_objs import Scatter, Marker


# Warning format
def warning_on_one_line(message, category, filename, lineno,
                        file=None, line=None):
    return '%s:%s: %s:\n\n%s\n\n' % (filename, lineno, category.__name__,
                                     message)
warnings.formatwarning = warning_on_one_line

try:
    from . import matplotlylib
    _matplotlylib_imported = True
except ImportError:
    _matplotlylib_imported = False

try:
    import IPython
    import IPython.core.display
    _ipython_imported = True
except ImportError:
    _ipython_imported = False

try:
    import numpy as np
    _numpy_imported = True
except ImportError:
    _numpy_imported = False

PLOTLY_DIR = os.path.join(os.path.expanduser("~"), ".plotly")
CREDENTIALS_FILE = os.path.join(PLOTLY_DIR, ".credentials")
CONFIG_FILE = os.path.join(PLOTLY_DIR, ".config")
TEST_DIR = os.path.join(os.path.expanduser("~"), ".test")
TEST_FILE = os.path.join(PLOTLY_DIR, ".permission_test")

# this sets both the DEFAULTS and the TYPES for these items
_FILE_CONTENT = {CREDENTIALS_FILE: {'username': '',
                                    'api_key': '',
                                    'proxy_username': '',
                                    'proxy_password': '',
                                    'api_key': '',
                                    'stream_ids': []},
                 CONFIG_FILE: {'plotly_domain': 'https://plot.ly',
                               'plotly_streaming_domain': 'stream.plot.ly',
                               'plotly_api_domain': 'https://api.plot.ly',
                               'plotly_ssl_verification': True,
                               'plotly_proxy_authorization': False,
                               'world_readable': True}}


try:
    os.mkdir(TEST_DIR)
    os.rmdir(TEST_DIR)
    if not os.path.exists(PLOTLY_DIR):
        os.mkdir(PLOTLY_DIR)
    f = open(TEST_FILE, 'w')
    f.write('testing\n')
    f.close()
    os.remove(TEST_FILE)
    _file_permissions = True
except:
    _file_permissions = False


def check_file_permissions():
    return _file_permissions


def ensure_local_plotly_files():
    """Ensure that filesystem is setup/filled out in a valid way"""
    if _file_permissions:
        for fn in [CREDENTIALS_FILE, CONFIG_FILE]:
            utils.ensure_file_exists(fn)
            contents = utils.load_json_dict(fn)
            for key, val in list(_FILE_CONTENT[fn].items()):
                # TODO: removed type checking below, may want to revisit
                if key not in contents:
                    contents[key] = val
            contents_keys = list(contents.keys())
            for key in contents_keys:
                if key not in _FILE_CONTENT[fn]:
                    del contents[key]
            utils.save_json_dict(fn, contents)
    else:
        warnings.warn("Looks like you don't have 'read-write' permission to "
                      "your 'home' ('~') directory or to our '~/.plotly' "
                      "directory. That means plotly's python api can't setup "
                      "local configuration files. No problem though! You'll "
                      "just have to sign-in using 'plotly.plotly.sign_in()'. "
                      "For help with that: 'help(plotly.plotly.sign_in)'."
                      "\nQuestions? support@plot.ly")


### credentials tools ###

def set_credentials_file(username=None,
                         api_key=None,
                         stream_ids=None,
                         proxy_username=None,
                         proxy_password=None):
    """Set the keyword-value pairs in `~/.plotly_credentials`.

    :param (str) username: The username you'd use to sign in to Plotly
    :param (str) api_key: The api key associated with above username
    :param (list) stream_ids: Stream tokens for above credentials
    :param (str) proxy_username: The un associated with with your Proxy
    :param (str) proxy_password: The pw associated with your Proxy un

    """
    if not _file_permissions:
        raise exceptions.PlotlyError("You don't have proper file permissions "
                                     "to run this function.")
    ensure_local_plotly_files()  # make sure what's there is OK
    credentials = get_credentials_file()
    if isinstance(username, six.string_types):
        credentials['username'] = username
    if isinstance(api_key, six.string_types):
        credentials['api_key'] = api_key
    if isinstance(proxy_username, six.string_types):
        credentials['proxy_username'] = proxy_username
    if isinstance(proxy_password, six.string_types):
        credentials['proxy_password'] = proxy_password
    if isinstance(stream_ids, (list, tuple)):
        credentials['stream_ids'] = stream_ids
    utils.save_json_dict(CREDENTIALS_FILE, credentials)
    ensure_local_plotly_files()  # make sure what we just put there is OK


def get_credentials_file(*args):
    """Return specified args from `~/.plotly_credentials`. as dict.

    Returns all if no arguments are specified.

    Example:
        get_credentials_file('username')

    """
    if _file_permissions:
        ensure_local_plotly_files()  # make sure what's there is OK
        return utils.load_json_dict(CREDENTIALS_FILE, *args)
    else:
        return _FILE_CONTENT[CREDENTIALS_FILE]


def reset_credentials_file():
    ensure_local_plotly_files()  # make sure what's there is OK
    utils.save_json_dict(CREDENTIALS_FILE, {})
    ensure_local_plotly_files()  # put the defaults back


### config tools ###

def set_config_file(plotly_domain=None,
                    plotly_streaming_domain=None,
                    plotly_api_domain=None,
                    plotly_ssl_verification=None,
                    plotly_proxy_authorization=None,
                    world_readable=None):
    """Set the keyword-value pairs in `~/.plotly/.config`.

    :param (str) plotly_domain: ex - https://plot.ly
    :param (str) plotly_streaming_domain: ex - stream.plot.ly
    :param (str) plotly_api_domain: ex - https://api.plot.ly
    :param (bool) plotly_ssl_verification: True = verify, False = don't verify
    :param (bool) plotly_proxy_authorization: True = use plotly proxy auth creds
    :param (bool) world_readable: True = public, False = private

    """
    if not _file_permissions:
        raise exceptions.PlotlyError("You don't have proper file permissions "
                                     "to run this function.")
    ensure_local_plotly_files()  # make sure what's there is OK
    settings = get_config_file()
    if isinstance(plotly_domain, six.string_types):
        settings['plotly_domain'] = plotly_domain
    elif plotly_domain is not None:
        raise TypeError('Input should be a string')
    if isinstance(plotly_streaming_domain, six.string_types):
        settings['plotly_streaming_domain'] = plotly_streaming_domain
    elif plotly_streaming_domain is not None:
        raise TypeError('Input should be a string')
    if isinstance(plotly_api_domain, six.string_types):
        settings['plotly_api_domain'] = plotly_api_domain
    elif plotly_api_domain is not None:
        raise TypeError('Input should be a string')
    if isinstance(plotly_ssl_verification, (six.string_types, bool)):
        settings['plotly_ssl_verification'] = plotly_ssl_verification
    elif plotly_ssl_verification is not None:
        raise TypeError('Input should be a boolean')
    if isinstance(plotly_proxy_authorization, (six.string_types, bool)):
        settings['plotly_proxy_authorization'] = plotly_proxy_authorization
    elif plotly_proxy_authorization is not None:
        raise TypeError('Input should be a boolean')
    if isinstance(world_readable, bool):
        settings['world_readable'] = world_readable
        kwargs = {'world_readable': world_readable}
        session.update_session_plot_options(**kwargs)
    elif world_readable is not None:
        raise TypeError('Input should be a boolean')
    utils.save_json_dict(CONFIG_FILE, settings)
    ensure_local_plotly_files()  # make sure what we just put there is OK


def get_config_file(*args):
    """Return specified args from `~/.plotly/.config`. as tuple.

    Returns all if no arguments are specified.

    Example:
        get_config_file('plotly_domain')

    """
    if _file_permissions:
        ensure_local_plotly_files()  # make sure what's there is OK
        return utils.load_json_dict(CONFIG_FILE, *args)
    else:
        return _FILE_CONTENT[CONFIG_FILE]


def reset_config_file():
    ensure_local_plotly_files()  # make sure what's there is OK
    f = open(CONFIG_FILE, 'w')
    f.close()
    ensure_local_plotly_files()  # put the defaults back


### embed tools ###

def get_embed(file_owner_or_url, file_id=None, width="100%", height=525):
    """Returns HTML code to embed figure on a webpage as an <iframe>

    Plotly uniquely identifies figures with a 'file_owner'/'file_id' pair.
    Since each file is given a corresponding unique url, you may also simply
    pass a valid plotly url as the first argument.

    Note, if you're using a file_owner string as the first argument, you MUST
    specify a `file_id` keyword argument. Else, if you're using a url string
    as the first argument, you MUST NOT specify a `file_id` keyword argument,
    or file_id must be set to Python's None value.

    Positional arguments:
    file_owner_or_url (string) -- a valid plotly username OR a valid plotly url

    Keyword arguments:
    file_id (default=None) -- an int or string that can be converted to int
                              if you're using a url, don't fill this in!
    width (default="100%") -- an int or string corresp. to width of the figure
    height (default="525") -- same as width but corresp. to the height of the
                              figure

    """
    padding = 25
    plotly_rest_url = (session.get_session_config().get('plotly_domain') or
                       get_config_file()['plotly_domain'])
    if file_id is None:  # assume we're using a url
        url = file_owner_or_url
        if url[:len(plotly_rest_url)] != plotly_rest_url:
            raise exceptions.PlotlyError(
                "Because you didn't supply a 'file_id' in the call, "
                "we're assuming you're trying to snag a figure from a url. "
                "You supplied the url, '{0}', we expected it to start with "
                "'{1}'."
                "\nRun help on this function for more information."
                "".format(url, plotly_rest_url))
        head = plotly_rest_url + "/~"
        file_owner = url.replace(head, "").split('/')[0]
        file_id = url.replace(head, "").split('/')[1]
    else:
        file_owner = file_owner_or_url
    resource = "/apigetfile/{file_owner}/{file_id}".format(file_owner=file_owner,
                                                           file_id=file_id)
    try:
        test_if_int = int(file_id)
    except ValueError:
        raise exceptions.PlotlyError(
            "The 'file_id' argument was not able to be converted into an "
            "integer number. Make sure that the positional 'file_id' argument "
            "is a number that can be converted into an integer or a string "
            "that can be converted into an integer."
        )
    if int(file_id) < 0:
        raise exceptions.PlotlyError(
            "The 'file_id' argument must be a non-negative number."
        )
    if isinstance(width, int):
        s = ("<iframe id=\"igraph\" scrolling=\"no\" style=\"border:none;\""
             "seamless=\"seamless\" "
             "src=\"{plotly_rest_url}/"
             "~{file_owner}/{file_id}.embed"
             "?width={plot_width}&height={plot_height}\" "
             "height=\"{iframe_height}\" width=\"{iframe_width}\">"
             "</iframe>").format(
            plotly_rest_url=plotly_rest_url,
            file_owner=file_owner, file_id=file_id,
            plot_width=width - padding, plot_height=height - padding,
            iframe_height=height, iframe_width=width)
    else:
        s = ("<iframe id=\"igraph\" scrolling=\"no\" style=\"border:none;\""
             "seamless=\"seamless\" "
             "src=\"{plotly_rest_url}/"
             "~{file_owner}/{file_id}.embed\" "
             "height=\"{iframe_height}\" width=\"{iframe_width}\">"
             "</iframe>").format(
            plotly_rest_url=plotly_rest_url,
            file_owner=file_owner, file_id=file_id,
            iframe_height=height, iframe_width=width)

    return s


def embed(file_owner_or_url, file_id=None, width="100%", height=525):
    """Embeds existing Plotly figure in IPython Notebook

    Plotly uniquely identifies figures with a 'file_owner'/'file_id' pair.
    Since each file is given a corresponding unique url, you may also simply
    pass a valid plotly url as the first argument.

    Note, if you're using a file_owner string as the first argument, you MUST
    specify a `file_id` keyword argument. Else, if you're using a url string
    as the first argument, you MUST NOT specify a `file_id` keyword argument, or
    file_id must be set to Python's None value.

    Positional arguments:
    file_owner_or_url (string) -- a valid plotly username OR a valid plotly url

    Keyword arguments:
    file_id (default=None) -- an int or string that can be converted to int
                              if you're using a url, don't fill this in!
    width (default="100%") -- an int or string corresp. to width of the figure
    height (default="525") -- same as width but corresp. to the height of the figure

    """
    try:
        s = get_embed(file_owner_or_url, file_id, width, height)
        # see if we are in the SageMath Cloud
        from sage_salvus import html
        return html(s, hide=False)
    except:
        pass
    if _ipython_imported:
        if file_id:
            plotly_domain = (
                session.get_session_config().get('plotly_domain') or
                get_config_file()['plotly_domain']
            )
            url = "{plotly_domain}/~{un}/{fid}".format(
                plotly_domain=plotly_domain,
                un=file_owner_or_url,
                fid=file_id)
        else:
            url = file_owner_or_url
        return PlotlyDisplay(url, width, height)
    else:
        warnings.warn(
            "Looks like you're not using IPython or Sage to embed this plot. "
            "If you just want the *embed code*, try using `get_embed()` "
            "instead."
            "\nQuestions? support@plot.ly")


### mpl-related tools ###
@utils.template_doc(**get_config_file())
def mpl_to_plotly(fig, resize=False, strip_style=False, verbose=False):
    """Convert a matplotlib figure to plotly dictionary and send.

    All available information about matplotlib visualizations are stored
    within a matplotlib.figure.Figure object. You can create a plot in python
    using matplotlib, store the figure object, and then pass this object to
    the fig_to_plotly function. In the background, mplexporter is used to
    crawl through the mpl figure object for appropriate information. This
    information is then systematically sent to the PlotlyRenderer which
    creates the JSON structure used to make plotly visualizations. Finally,
    these dictionaries are sent to plotly and your browser should open up a
    new tab for viewing! Optionally, if you're working in IPython, you can
    set notebook=True and the PlotlyRenderer will call plotly.iplot instead
    of plotly.plot to have the graph appear directly in the IPython notebook.

    Note, this function gives the user access to a simple, one-line way to
    render an mpl figure in plotly. If you need to trouble shoot, you can do
    this step manually by NOT running this fuction and entereing the following:

    ===========================================================================
    from mplexporter import Exporter
    from mplexporter.renderers import PlotlyRenderer

    # create an mpl figure and store it under a varialble 'fig'

    renderer = PlotlyRenderer()
    exporter = Exporter(renderer)
    exporter.run(fig)
    ===========================================================================

    You can then inspect the JSON structures by accessing these:

    renderer.layout -- a plotly layout dictionary
    renderer.data -- a list of plotly data dictionaries

    Positional arguments:
    fig -- a matplotlib figure object
    username -- a valid plotly username **
    api_key -- a valid api_key for the above username **
    notebook -- an option for use with an IPython notebook

    ** Don't have a username/api_key? Try looking here:
    {plotly_domain}/plot

    ** Forgot your api_key? Try signing in and looking here:
    {plotly_domain}/python/getting-started

    """
    if _matplotlylib_imported:
        renderer = matplotlylib.PlotlyRenderer()
        matplotlylib.Exporter(renderer).run(fig)
        if resize:
            renderer.resize()
        if strip_style:
            renderer.strip_style()
        if verbose:
            print(renderer.msg)
        return renderer.plotly_fig
    else:
        warnings.warn(
            "To use Plotly's matplotlylib functionality, you'll need to have "
            "matplotlib successfully installed with all of its dependencies. "
            "You're getting this error because matplotlib or one of its "
            "dependencies doesn't seem to be installed correctly.")


### graph_objs related tools ###

def get_subplots(rows=1, columns=1, print_grid=False, **kwargs):
    """Return a dictionary instance with the subplots set in 'layout'.

    Example 1:
    # stack two subplots vertically
    fig = tools.get_subplots(rows=2)
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x1', yaxis='y1')]
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x2', yaxis='y2')]

    Example 2:
    # print out string showing the subplot grid you've put in the layout
    fig = tools.get_subplots(rows=3, columns=2, print_grid=True)

    Keywords arguments with constant defaults:

    rows (kwarg, int greater than 0, default=1):
        Number of rows, evenly spaced vertically on the figure.

    columns (kwarg, int greater than 0, default=1):
        Number of columns, evenly spaced horizontally on the figure.

    horizontal_spacing (kwarg, float in [0,1], default=0.1):
        Space between subplot columns. Applied to all columns.

    vertical_spacing (kwarg, float in [0,1], default=0.05):
        Space between subplot rows. Applied to all rows.

    print_grid (kwarg, True | False, default=False):
        If True, prints a tab-delimited string representation
        of your plot grid.

    Keyword arguments with variable defaults:

    horizontal_spacing (kwarg, float in [0,1], default=0.2 / columns):
        Space between subplot columns.

    vertical_spacing (kwarg, float in [0,1], default=0.3 / rows):
        Space between subplot rows.

    """

    warnings.warn(
        "tools.get_subplots is depreciated. "
        "Please use tools.make_subplots instead."
    )

    # Throw exception for non-integer rows and columns
    if not isinstance(rows, int) or rows <= 0:
        raise Exception("Keyword argument 'rows' "
                        "must be an int greater than 0")
    if not isinstance(columns, int) or columns <= 0:
        raise Exception("Keyword argument 'columns' "
                        "must be an int greater than 0")

    # Throw exception if non-valid kwarg is sent
    VALID_KWARGS = ['horizontal_spacing', 'vertical_spacing']
    for key in kwargs.keys():
        if key not in VALID_KWARGS:
            raise Exception("Invalid keyword argument: '{0}'".format(key))

    # Set 'horizontal_spacing' / 'vertical_spacing' w.r.t. rows / columns
    try:
        horizontal_spacing = float(kwargs['horizontal_spacing'])
    except KeyError:
        horizontal_spacing = 0.2 / columns
    try:
        vertical_spacing = float(kwargs['vertical_spacing'])
    except KeyError:
        vertical_spacing = 0.3 / rows

    fig = dict(layout=graph_objs.Layout())  # will return this at the end
    plot_width = (1 - horizontal_spacing * (columns - 1)) / columns
    plot_height = (1 - vertical_spacing * (rows - 1)) / rows
    plot_num = 0
    for rrr in range(rows):
        for ccc in range(columns):
            xaxis_name = 'xaxis{0}'.format(plot_num + 1)
            x_anchor = 'y{0}'.format(plot_num + 1)
            x_start = (plot_width + horizontal_spacing) * ccc
            x_end = x_start + plot_width

            yaxis_name = 'yaxis{0}'.format(plot_num + 1)
            y_anchor = 'x{0}'.format(plot_num + 1)
            y_start = (plot_height + vertical_spacing) * rrr
            y_end = y_start + plot_height

            xaxis = graph_objs.XAxis(domain=[x_start, x_end], anchor=x_anchor)
            fig['layout'][xaxis_name] = xaxis
            yaxis = graph_objs.YAxis(domain=[y_start, y_end], anchor=y_anchor)
            fig['layout'][yaxis_name] = yaxis
            plot_num += 1

    if print_grid:
        print("This is the format of your plot grid!")
        grid_string = ""
        plot = 1
        for rrr in range(rows):
            grid_line = ""
            for ccc in range(columns):
                grid_line += "[{0}]\t".format(plot)
                plot += 1
            grid_string = grid_line + '\n' + grid_string
        print(grid_string)

    return graph_objs.Figure(fig)  # forces us to validate what we just did...


def make_subplots(rows=1, cols=1,
                  shared_xaxes=False, shared_yaxes=False,
                  start_cell='top-left', print_grid=True,
                  **kwargs):
    """Return an instance of plotly.graph_objs.Figure
    with the subplots domain set in 'layout'.

    Example 1:
    # stack two subplots vertically
    fig = tools.make_subplots(rows=2)

    This is the format of your plot grid:
    [ (1,1) x1,y1 ]
    [ (2,1) x2,y2 ]

    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2])]
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x2', yaxis='y2')]

    # or see Figure.append_trace

    Example 2:
    # subplots with shared x axes
    fig = tools.make_subplots(rows=2, shared_xaxes=True)

    This is the format of your plot grid:
    [ (1,1) x1,y1 ]
    [ (2,1) x1,y2 ]


    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2])]
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], yaxis='y2')]

    Example 3:
    # irregular subplot layout (more examples below under 'specs')
    fig = tools.make_subplots(rows=2, cols=2,
                              specs=[[{}, {}],
                                     [{'colspan': 2}, None]])

    This is the format of your plot grid!
    [ (1,1) x1,y1 ]  [ (1,2) x2,y2 ]
    [ (2,1) x3,y3           -      ]

    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2])]
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x2', yaxis='y2')]
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x3', yaxis='y3')]

    Example 4:
    # insets
    fig = tools.make_subplots(insets=[{'cell': (1,1), 'l': 0.7, 'b': 0.3}])

    This is the format of your plot grid!
    [ (1,1) x1,y1 ]

    With insets:
    [ x2,y2 ] over [ (1,1) x1,y1 ]

    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2])]
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x2', yaxis='y2')]

    Example 5:
    # include subplot titles
    fig = tools.make_subplots(rows=2, subplot_titles=('Plot 1','Plot 2'))

    This is the format of your plot grid:
    [ (1,1) x1,y1 ]
    [ (2,1) x2,y2 ]

    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2])]
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x2', yaxis='y2')]

    Example 6:
    # Include subplot title on one plot (but not all)
    fig = tools.make_subplots(insets=[{'cell': (1,1), 'l': 0.7, 'b': 0.3}],
                              subplot_titles=('','Inset'))

    This is the format of your plot grid!
    [ (1,1) x1,y1 ]

    With insets:
    [ x2,y2 ] over [ (1,1) x1,y1 ]

    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2])]
    fig['data'] += [Scatter(x=[1,2,3], y=[2,1,2], xaxis='x2', yaxis='y2')]

    Keywords arguments with constant defaults:

    rows (kwarg, int greater than 0, default=1):
        Number of rows in the subplot grid.

    cols (kwarg, int greater than 0, default=1):
        Number of columns in the subplot grid.

    shared_xaxes (kwarg, boolean or list, default=False)
        Assign shared x axes.
        If True, subplots in the same grid column have one common
        shared x-axis at the bottom of the gird.

        To assign shared x axes per subplot grid cell (see 'specs'),
        send list (or list of lists, one list per shared x axis)
        of cell index tuples.

    shared_yaxes (kwarg, boolean or list, default=False)
        Assign shared y axes.
        If True, subplots in the same grid row have one common
        shared y-axis on the left-hand side of the gird.

        To assign shared y axes per subplot grid cell (see 'specs'),
        send list (or list of lists, one list per shared y axis)
        of cell index tuples.

    start_cell (kwarg, 'bottom-left' or 'top-left', default='top-left')
        Choose the starting cell in the subplot grid used to set the
        domains of the subplots.

    print_grid (kwarg, boolean, default=True):
        If True, prints a tab-delimited string representation of
        your plot grid.

    Keyword arguments with variable defaults:

    horizontal_spacing (kwarg, float in [0,1], default=0.2 / cols):
        Space between subplot columns.
        Applies to all columns (use 'specs' subplot-dependents spacing)

    vertical_spacing (kwarg, float in [0,1], default=0.3 / rows):
        Space between subplot rows.
        Applies to all rows (use 'specs' subplot-dependents spacing)

    subplot_titles (kwarg, list of strings, default=empty list):
        Title of each subplot.
        "" can be included in the list if no subplot title is desired in
        that space so that the titles are properly indexed.

    specs (kwarg, list of lists of dictionaries):
        Subplot specifications.

        ex1: specs=[[{}, {}], [{'colspan': 2}, None]]

        ex2: specs=[[{'rowspan': 2}, {}], [None, {}]]

        - Indices of the outer list correspond to subplot grid rows
          starting from the bottom. The number of rows in 'specs'
          must be equal to 'rows'.

        - Indices of the inner lists correspond to subplot grid columns
          starting from the left. The number of columns in 'specs'
          must be equal to 'cols'.

        - Each item in the 'specs' list corresponds to one subplot
          in a subplot grid. (N.B. The subplot grid has exactly 'rows'
          times 'cols' cells.)

        - Use None for blank a subplot cell (or to move pass a col/row span).

        - Note that specs[0][0] has the specs of the 'start_cell' subplot.

        - Each item in 'specs' is a dictionary.
            The available keys are:

            * is_3d (boolean, default=False): flag for 3d scenes
            * colspan (int, default=1): number of subplot columns
                for this subplot to span.
            * rowspan (int, default=1): number of subplot rows
                for this subplot to span.
            * l (float, default=0.0): padding left of cell
            * r (float, default=0.0): padding right of cell
            * t (float, default=0.0): padding right of cell
            * b (float, default=0.0): padding bottom of cell

        - Use 'horizontal_spacing' and 'vertical_spacing' to adjust
          the spacing in between the subplots.

    insets (kwarg, list of dictionaries):
        Inset specifications.

        - Each item in 'insets' is a dictionary.
            The available keys are:

            * cell (tuple, default=(1,1)): (row, col) index of the
                subplot cell to overlay inset axes onto.
            * is_3d (boolean, default=False): flag for 3d scenes
            * l (float, default=0.0): padding left of inset
                  in fraction of cell width
            * w (float or 'to_end', default='to_end') inset width
                  in fraction of cell width ('to_end': to cell right edge)
            * b (float, default=0.0): padding bottom of inset
                  in fraction of cell height
            * h (float or 'to_end', default='to_end') inset height
                  in fraction of cell height ('to_end': to cell top edge)
    """

    # Throw exception for non-integer rows and cols
    if not isinstance(rows, int) or rows <= 0:
        raise Exception("Keyword argument 'rows' "
                        "must be an int greater than 0")
    if not isinstance(cols, int) or cols <= 0:
        raise Exception("Keyword argument 'cols' "
                        "must be an int greater than 0")

    # Dictionary of things start_cell
    START_CELL_all = {
        'bottom-left': {
            # 'natural' setup where x & y domains increase monotonically
            'col_dir': 1,
            'row_dir': 1
        },
        'top-left': {
            # 'default' setup visually matching the 'specs' list of lists
            'col_dir': 1,
            'row_dir': -1
        }
        # TODO maybe add 'bottom-right' and 'top-right'
    }

    # Throw exception for invalid 'start_cell' values
    try:
        START_CELL = START_CELL_all[start_cell]
    except KeyError:
        raise Exception("Invalid 'start_cell' value")

    # Throw exception if non-valid kwarg is sent
    VALID_KWARGS = ['horizontal_spacing', 'vertical_spacing',
                    'specs', 'insets', 'subplot_titles']
    for key in kwargs.keys():
        if key not in VALID_KWARGS:
            raise Exception("Invalid keyword argument: '{0}'".format(key))

    # Set 'subplot_titles'
    subplot_titles = kwargs.get('subplot_titles', [""] * rows * cols)

    # Set 'horizontal_spacing' / 'vertical_spacing' w.r.t. rows / cols
    try:
        horizontal_spacing = float(kwargs['horizontal_spacing'])
    except KeyError:
        horizontal_spacing = 0.2 / cols
    try:
        vertical_spacing = float(kwargs['vertical_spacing'])
    except KeyError:
        if 'subplot_titles' in kwargs:
            vertical_spacing = 0.5 / rows
        else:
            vertical_spacing = 0.3 / rows

    # Sanitize 'specs' (must be a list of lists)
    exception_msg = "Keyword argument 'specs' must be a list of lists"
    try:
        specs = kwargs['specs']
        if not isinstance(specs, list):
            raise Exception(exception_msg)
        else:
            for spec_row in specs:
                if not isinstance(spec_row, list):
                    raise Exception(exception_msg)
    except KeyError:
        specs = [[{}
                 for c in range(cols)]
                 for r in range(rows)]     # default 'specs'

    # Throw exception if specs is over or under specified
    if len(specs) != rows:
        raise Exception("The number of rows in 'specs' "
                        "must be equal to 'rows'")
    for r, spec_row in enumerate(specs):
        if len(spec_row) != cols:
            raise Exception("The number of columns in 'specs' "
                            "must be equal to 'cols'")

    # Sanitize 'insets'
    try:
        insets = kwargs['insets']
        if not isinstance(insets, list):
            raise Exception("Keyword argument 'insets' must be a list")
    except KeyError:
        insets = False

    # Throw exception if non-valid key / fill in defaults
    def _check_keys_and_fill(name, arg, defaults):
        def _checks(item, defaults):
            if item is None:
                return
            if not isinstance(item, dict):
                raise Exception("Items in keyword argument '{name}' must be "
                                "dictionaries or None".format(name=name))
            for k in item.keys():
                if k not in defaults.keys():
                    raise Exception("Invalid key '{k}' in keyword "
                                    "argument '{name}'".format(k=k, name=name))
            for k in defaults.keys():
                if k not in item.keys():
                    item[k] = defaults[k]
        for arg_i in arg:
            if isinstance(arg_i, list):
                for arg_ii in arg_i:
                    _checks(arg_ii, defaults)
            elif isinstance(arg_i, dict):
                _checks(arg_i, defaults)

    # Default spec key-values
    SPEC_defaults = dict(
        is_3d=False,
        colspan=1,
        rowspan=1,
        l=0.0,
        r=0.0,
        b=0.0,
        t=0.0
        # TODO add support for 'w' and 'h'
    )
    _check_keys_and_fill('specs', specs, SPEC_defaults)

    # Default inset key-values
    if insets:
        INSET_defaults = dict(
            cell=(1, 1),
            is_3d=False,
            l=0.0,
            w='to_end',
            b=0.0,
            h='to_end'
        )
        _check_keys_and_fill('insets', insets, INSET_defaults)

    # Set width & height of each subplot cell (excluding padding)
    width = (1. - horizontal_spacing * (cols - 1)) / cols
    height = (1. - vertical_spacing * (rows - 1)) / rows

    # Built row/col sequence using 'row_dir' and 'col_dir'
    COL_DIR = START_CELL['col_dir']
    ROW_DIR = START_CELL['row_dir']
    col_seq = range(cols)[::COL_DIR]
    row_seq = range(rows)[::ROW_DIR]

    # [grid] Build subplot grid (coord tuple of cell)
    grid = [[((width + horizontal_spacing) * c,
              (height + vertical_spacing) * r)
            for c in col_seq]
            for r in row_seq]

    # [grid_ref] Initialize the grid and insets' axis-reference lists
    grid_ref = [[None for c in range(cols)] for r in range(rows)]
    insets_ref = [None for inset in range(len(insets))] if insets else None

    layout = graph_objs.Layout()  # init layout object

    # Function handling logic around 2d axis labels
    # Returns 'x{}' | 'y{}'
    def _get_label(x_or_y, r, c, cnt, shared_axes):
        # Default label (given strictly by cnt)
        label = "{x_or_y}{cnt}".format(x_or_y=x_or_y, cnt=cnt)

        if isinstance(shared_axes, bool):
            if shared_axes:
                if x_or_y == 'x':
                    label = "{x_or_y}{c}".format(x_or_y=x_or_y, c=c + 1)
                if x_or_y == 'y':
                    label = "{x_or_y}{r}".format(x_or_y=x_or_y, r=r + 1)

        if isinstance(shared_axes, list):
            if isinstance(shared_axes[0], tuple):
                shared_axes = [shared_axes]  # TODO put this elsewhere
            for shared_axis in shared_axes:
                if (r + 1, c + 1) in shared_axis:
                    label = {
                        'x': "x{0}".format(shared_axis[0][1]),
                        'y': "y{0}".format(shared_axis[0][0])
                    }[x_or_y]

        return label

    # Row in grid of anchor row if shared_xaxes=True
    ANCHOR_ROW = 0 if ROW_DIR > 0 else rows - 1

    # Function handling logic around 2d axis anchors
    # Return 'x{}' | 'y{}' | 'free' | False
    def _get_anchors(r, c, x_cnt, y_cnt, shared_xaxes, shared_yaxes):
        # Default anchors (give strictly by cnt)
        x_anchor = "y{y_cnt}".format(y_cnt=y_cnt)
        y_anchor = "x{x_cnt}".format(x_cnt=x_cnt)

        if isinstance(shared_xaxes, bool):
            if shared_xaxes:
                if r != ANCHOR_ROW:
                    x_anchor = False
                    y_anchor = 'free'
                    if shared_yaxes and c != 0:  # TODO covers all cases?
                        y_anchor = False
                    return x_anchor, y_anchor

        elif isinstance(shared_xaxes, list):
            if isinstance(shared_xaxes[0], tuple):
                shared_xaxes = [shared_xaxes]  # TODO put this elsewhere
            for shared_xaxis in shared_xaxes:
                if (r + 1, c + 1) in shared_xaxis[1:]:
                    x_anchor = False
                    y_anchor = 'free'  # TODO covers all cases?

        if isinstance(shared_yaxes, bool):
            if shared_yaxes:
                if c != 0:
                    y_anchor = False
                    x_anchor = 'free'
                    if shared_xaxes and r != ANCHOR_ROW:  # TODO all cases?
                        x_anchor = False
                    return x_anchor, y_anchor

        elif isinstance(shared_yaxes, list):
            if isinstance(shared_yaxes[0], tuple):
                shared_yaxes = [shared_yaxes]  # TODO put this elsewhere
            for shared_yaxis in shared_yaxes:
                if (r + 1, c + 1) in shared_yaxis[1:]:
                    y_anchor = False
                    x_anchor = 'free'  # TODO covers all cases?

        return x_anchor, y_anchor

    list_of_domains = []  # added for subplot titles

    # Function pasting x/y domains in layout object (2d case)
    def _add_domain(layout, x_or_y, label, domain, anchor, position):
        name = label[0] + 'axis' + label[1:]
        graph_obj = '{X_or_Y}Axis'.format(X_or_Y=x_or_y.upper())
        axis = getattr(graph_objs, graph_obj)(domain=domain)
        if anchor:
            axis['anchor'] = anchor
        if isinstance(position, float):
            axis['position'] = position
        layout[name] = axis
        list_of_domains.append(domain)  # added for subplot titles

    # Function pasting x/y domains in layout object (3d case)
    def _add_domain_is_3d(layout, s_label, x_domain, y_domain):
        scene = graph_objs.Scene(domain={'x': x_domain, 'y': y_domain})
        layout[s_label] = scene

    x_cnt = y_cnt = s_cnt = 1  # subplot axis/scene counters

    # Loop through specs -- (r, c) <-> (row, col)
    for r, spec_row in enumerate(specs):
        for c, spec in enumerate(spec_row):

            if spec is None:  # skip over None cells
                continue

            c_spanned = c + spec['colspan'] - 1  # get spanned c
            r_spanned = r + spec['rowspan'] - 1  # get spanned r

            # Throw exception if 'colspan' | 'rowspan' is too large for grid
            if c_spanned >= cols:
                raise Exception("Some 'colspan' value is too large for "
                                "this subplot grid.")
            if r_spanned >= rows:
                raise Exception("Some 'rowspan' value is too large for "
                                "this subplot grid.")

            # Get x domain using grid and colspan
            x_s = grid[r][c][0] + spec['l']
            x_e = grid[r][c_spanned][0] + width - spec['r']
            x_domain = [x_s, x_e]

            # Get y domain (dep. on row_dir) using grid & r_spanned
            if ROW_DIR > 0:
                y_s = grid[r][c][1] + spec['b']
                y_e = grid[r_spanned][c][1] + height - spec['t']
            else:
                y_s = grid[r_spanned][c][1] + spec['b']
                y_e = grid[r][c][1] + height - spec['t']
            y_domain = [y_s, y_e]

            if spec['is_3d']:

                # Add scene to layout
                s_label = 'scene{0}'.format(s_cnt)
                _add_domain_is_3d(layout, s_label, x_domain, y_domain)
                grid_ref[r][c] = (s_label, )
                s_cnt += 1

            else:

                # Get axis label and anchor
                x_label = _get_label('x', r, c, x_cnt, shared_xaxes)
                y_label = _get_label('y', r, c, y_cnt, shared_yaxes)
                x_anchor, y_anchor = _get_anchors(r, c,
                                                  x_cnt, y_cnt,
                                                  shared_xaxes,
                                                  shared_yaxes)

                # Add a xaxis to layout (N.B anchor == False -> no axis)
                if x_anchor:
                    if x_anchor == 'free':
                        x_position = y_domain[0]
                    else:
                        x_position = False
                    _add_domain(layout, 'x', x_label, x_domain,
                                x_anchor, x_position)
                    x_cnt += 1

                # Add a yaxis to layout (N.B anchor == False -> no axis)
                if y_anchor:
                    if y_anchor == 'free':
                        y_position = x_domain[0]
                    else:
                        y_position = False
                    _add_domain(layout, 'y', y_label, y_domain,
                                y_anchor, y_position)
                    y_cnt += 1

                grid_ref[r][c] = (x_label, y_label)  # fill in ref

    # Loop through insets
    if insets:
        for i_inset, inset in enumerate(insets):

            r = inset['cell'][0] - 1
            c = inset['cell'][1] - 1

            # Throw exception if r | c is out of range
            if not (0 <= r < rows):
                raise Exception("Some 'cell' row value is out of range. "
                                "Note: the starting cell is (1, 1)")
            if not (0 <= c < cols):
                raise Exception("Some 'cell' col value is out of range. "
                                "Note: the starting cell is (1, 1)")

            # Get inset x domain using grid
            x_s = grid[r][c][0] + inset['l'] * width
            if inset['w'] == 'to_end':
                x_e = grid[r][c][0] + width
            else:
                x_e = x_s + inset['w'] * width
            x_domain = [x_s, x_e]

            # Get inset y domain using grid
            y_s = grid[r][c][1] + inset['b'] * height
            if inset['h'] == 'to_end':
                y_e = grid[r][c][1] + height
            else:
                y_e = y_s + inset['h'] * height
            y_domain = [y_s, y_e]

            if inset['is_3d']:

                # Add scene to layout
                s_label = 'scene{0}'.format(s_cnt)
                _add_domain_is_3d(layout, s_label, x_domain, y_domain)
                insets_ref[i_inset] = (s_label, )
                s_cnt += 1

            else:

                # Get axis label and anchor
                x_label = _get_label('x', False, False, x_cnt, False)
                y_label = _get_label('y', False, False, y_cnt, False)
                x_anchor, y_anchor = _get_anchors(r, c,
                                                  x_cnt, y_cnt,
                                                  False, False)

                # Add a xaxis to layout (N.B insets always have anchors)
                _add_domain(layout, 'x', x_label, x_domain, x_anchor, False)
                x_cnt += 1

                # Add a yayis to layout (N.B insets always have anchors)
                _add_domain(layout, 'y', y_label, y_domain, y_anchor, False)
                y_cnt += 1

                insets_ref[i_inset] = (x_label, y_label)  # fill in ref

    # [grid_str] Set the grid's string representation
    sp = "  "            # space between cell
    s_str = "[ "         # cell start string
    e_str = " ]"         # cell end string
    colspan_str = '       -'     # colspan string
    rowspan_str = '       |'     # rowspan string
    empty_str = '    (empty) '   # empty cell string

    # Init grid_str with intro message
    grid_str = "This is the format of your plot grid:\n"

    # Init tmp list of lists of strings (sorta like 'grid_ref' but w/ strings)
    _tmp = [['' for c in range(cols)] for r in range(rows)]

    # Define cell string as function of (r, c) and grid_ref
    def _get_cell_str(r, c, ref):
        return '({r},{c}) {ref}'.format(r=r + 1, c=c + 1, ref=','.join(ref))

    # Find max len of _cell_str, add define a padding function
    cell_len = max([len(_get_cell_str(r, c, ref))
                    for r, row_ref in enumerate(grid_ref)
                    for c, ref in enumerate(row_ref)
                    if ref]) + len(s_str) + len(e_str)

    def _pad(s, cell_len=cell_len):
        return ' ' * (cell_len - len(s))

    # Loop through specs, fill in _tmp
    for r, spec_row in enumerate(specs):
        for c, spec in enumerate(spec_row):

            ref = grid_ref[r][c]
            if ref is None:
                if _tmp[r][c] == '':
                    _tmp[r][c] = empty_str + _pad(empty_str)
                continue

            cell_str = s_str + _get_cell_str(r, c, ref)

            if spec['colspan'] > 1:
                for cc in range(1, spec['colspan'] - 1):
                    _tmp[r][c + cc] = colspan_str + _pad(colspan_str)
                _tmp[r][c + spec['colspan'] - 1] = (
                    colspan_str + _pad(colspan_str + e_str)) + e_str
            else:
                cell_str += e_str

            if spec['rowspan'] > 1:
                for rr in range(1, spec['rowspan'] - 1):
                    _tmp[r + rr][c] = rowspan_str + _pad(rowspan_str)
                for cc in range(spec['colspan']):
                    _tmp[r + spec['rowspan'] - 1][c + cc] = (
                        rowspan_str + _pad(rowspan_str))

            _tmp[r][c] = cell_str + _pad(cell_str)

    # Append grid_str using data from _tmp in the correct order
    for r in row_seq[::-1]:
        grid_str += sp.join(_tmp[r]) + '\n'

    # Append grid_str to include insets info
    if insets:
        grid_str += "\nWith insets:\n"
        for i_inset, inset in enumerate(insets):

            r = inset['cell'][0] - 1
            c = inset['cell'][1] - 1
            ref = grid_ref[r][c]

            grid_str += (
                s_str + ','.join(insets_ref[i_inset]) + e_str +
                ' over ' +
                s_str + _get_cell_str(r, c, ref) + e_str + '\n'
            )

    # Add subplot titles

    # If shared_axes is False (default) use list_of_domains
    # This is used for insets and irregular layouts
    if not shared_xaxes and not shared_yaxes:
        x_dom = list_of_domains[::2]
        y_dom = list_of_domains[1::2]
        subtitle_pos_x = []
        subtitle_pos_y = []
        for x_domains in x_dom:
            subtitle_pos_x.append(sum(x_domains) / 2)
        for y_domains in y_dom:
            subtitle_pos_y.append(y_domains[1])
    # If shared_axes is True the domin of each subplot is not returned so the
    # title position must be calculated for each subplot
    else:
        subtitle_pos_x = [None] * cols
        subtitle_pos_y = [None] * rows
        delt_x = (x_e - x_s)
        for index in range(cols):
            subtitle_pos_x[index] = ((delt_x / 2) +
                                     ((delt_x + horizontal_spacing) * index))
        subtitle_pos_x *= rows
        for index in range(rows):
            subtitle_pos_y[index] = (1 - ((y_e + vertical_spacing) * index))
        subtitle_pos_y *= cols
        subtitle_pos_y = sorted(subtitle_pos_y, reverse=True)

    plot_titles = []
    for index in range(len(subplot_titles)):
        if not subplot_titles[index]:
            pass
        else:
            plot_titles.append({'y': subtitle_pos_y[index],
                                'xref': 'paper',
                                'x': subtitle_pos_x[index],
                                'yref': 'paper',
                                'text': subplot_titles[index],
                                'showarrow': False,
                                'font': graph_objs.Font(size=16),
                                'xanchor': 'center',
                                'yanchor': 'bottom'
                                })

            layout['annotations'] = plot_titles

    if print_grid:
        print(grid_str)

    fig = graph_objs.Figure(layout=layout)

    fig._grid_ref = grid_ref
    fig._grid_str = grid_str

    return fig


def get_valid_graph_obj(obj, obj_type=None):
    """Returns a new graph object that is guaranteed to pass validate().

    CAREFUL: this will *silently* strip out invalid pieces of the object.

    """
    try:
        new_obj = graph_objs.get_class_instance_by_name(
            obj.__class__.__name__)
    except KeyError:
        try:
            new_obj = graph_objs.get_class_instance_by_name(obj_type)
        except KeyError:
            raise exceptions.PlotlyError(
                "'{0}' nor '{1}' are recognizable graph_objs.".
                format(obj.__class__.__name__, obj_type))
    if isinstance(new_obj, list):
        new_obj += obj
    else:
        for key, val in list(obj.items()):
            new_obj[key] = val
    new_obj.force_clean()
    return new_obj


def validate(obj, obj_type):
    """Validate a dictionary, list, or graph object as 'obj_type'.

    This will not alter the 'obj' referenced in the call signature. It will
    raise an error if the 'obj' reference could not be instantiated as a
    valid 'obj_type' graph object.

    """
    try:
        obj_type = graph_objs.KEY_TO_NAME[obj_type]
    except KeyError:
        pass
    try:
        test_obj = graph_objs.get_class_instance_by_name(obj_type, obj)
    except KeyError:
        raise exceptions.PlotlyError(
            "'{0}' is not a recognizable graph_obj.".
            format(obj_type))


def validate_stream(obj, obj_type):
    """Validate a data dictionary (only) for use with streaming.

    An error is raised if a key within (or nested within) is not streamable.

    """
    try:
        obj_type = graph_objs.KEY_TO_NAME[obj_type]
    except KeyError:
        pass
    info = graph_objs.INFO[graph_objs.NAME_TO_KEY[obj_type]]
    for key, val in list(obj.items()):
        if key == 'type':
            continue
        if 'streamable' in info['keymeta'][key].keys():
            if not info['keymeta'][key]['streamable']:
                raise exceptions.PlotlyError(
                    "The '{0}' key is not streamable in the '{1}' "
                    "object".format(
                        key, obj_type
                    )
                )
        else:
            raise exceptions.PlotlyError(
                "The '{0}' key is not streamable in the '{1}' object".format(
                    key, obj_type
                )
            )
        try:
            sub_obj_type = graph_objs.KEY_TO_NAME[key]
            validate_stream(val, sub_obj_type)
        except KeyError:
            pass


def _replace_newline(obj):
    """Replaces '\n' with '<br>' for all strings in a collection."""
    if isinstance(obj, dict):
        d = dict()
        for key, val in list(obj.items()):
            d[key] = _replace_newline(val)
        return d
    elif isinstance(obj, list):
        l = list()
        for index, entry in enumerate(obj):
            l += [_replace_newline(entry)]
        return l
    elif isinstance(obj, six.string_types):
        s = obj.replace('\n', '<br>')
        if s != obj:
            warnings.warn("Looks like you used a newline character: '\\n'.\n\n"
                          "Plotly uses a subset of HTML escape characters\n"
                          "to do things like newline (<br>), bold (<b></b>),\n"
                          "italics (<i></i>), etc. Your newline characters \n"
                          "have been converted to '<br>' so they will show \n"
                          "up right on your Plotly figure!")
        return s
    else:
        return obj  # we return the actual reference... but DON'T mutate.


if _ipython_imported:
    class PlotlyDisplay(IPython.core.display.HTML):
        """An IPython display object for use with plotly urls

        PlotlyDisplay objects should be instantiated with a url for a plot.
        IPython will *choose* the proper display representation from any
        Python object, and using provided methods if they exist. By defining
        the following, if an HTML display is unusable, the PlotlyDisplay
        object can provide alternate representations.

        """
        def __init__(self, url, width, height):
            self.resource = url
            self.embed_code = get_embed(url, width=width, height=height)
            super(PlotlyDisplay, self).__init__(data=self.embed_code)

        def _repr_html_(self):
            return self.embed_code


def return_figure_from_figure_or_data(figure_or_data, validate_figure):
    if isinstance(figure_or_data, dict):
        figure = figure_or_data
    elif isinstance(figure_or_data, list):
        figure = {'data': figure_or_data}
    else:
        raise exceptions.PlotlyError("The `figure_or_data` positional "
                                     "argument must be either "
                                     "`dict`-like or `list`-like.")
    if validate_figure:
        try:
            validate(figure, obj_type='Figure')
        except exceptions.PlotlyError as err:
            raise exceptions.PlotlyError("Invalid 'figure_or_data' argument. "
                                         "Plotly will not be able to properly "
                                         "parse the resulting JSON. If you "
                                         "want to send this 'figure_or_data' "
                                         "to Plotly anyway (not recommended), "
                                         "you can set 'validate=False' as a "
                                         "plot option.\nHere's why you're "
                                         "seeing this error:\n\n{0}"
                                         "".format(err))
        if not figure['data']:
            raise exceptions.PlotlyEmptyDataError(
                "Empty data list found. Make sure that you populated the "
                "list of data objects you're sending and try again.\n"
                "Questions? support@plot.ly"
            )

    return figure


class TraceFactory(object):

    @staticmethod
    def validate_equal_length(*args):
        """
        Validates that data lists or ndarrays are the same length.

        :raises: (PlotlyError) If any data lists are not the same length.
        """
        length = len(args[0])
        if any(len(lst) != length for lst in args):
            raise exceptions.PlotlyError("Oops! Your data lists or ndarrays "
                                         "should be the same length.")

    @staticmethod
    def validate_positive_scalars(**kwargs):
        """
        Validates that all values given in key/val pairs are positive.

        Accepts kwargs to improve Exception messages.

        :raises: (PlotlyError) If any value is < 0 or raises.
        """
        for key, val in kwargs.items():
            try:
                if val <= 0:
                    raise ValueError('{} must be > 0, got {}'.format(key, val))
            except TypeError:
                raise exceptions.PlotlyError('{} must be a number, got {}'
                                             .format(key, val))

    @staticmethod
    def validate_streamline(x, y):
        """
        streamline specific validations

        Specifically, this checks that x and y are both evenly spaced,
        and that the package numpy is available.

        See TraceFactory.create_streamline() for params

        :raises: (ImportError) If numpy is not available.
        :raises: (PlotlyError) If x is not evenly spaced.
        :raises: (PlotlyError) If y is not evenly spaced.
        """
        if _numpy_imported is False:
            raise ImportError("TraceFactory.create_streamline requires numpy.")
        for index in range(len(x) - 1):
            if ((x[index + 1] - x[index]) - (x[1] - x[0])) > .0001:
                raise exceptions.PlotlyError("x must be a 1 dimensional, "
                                             "evenly spaced array")
        for index in range(len(y) - 1):
            if ((y[index + 1] - y[index]) -
               (y[1] - y[0])) > .0001:
                raise exceptions.PlotlyError("y must be a 1 dimensional, "
                                             "evenly spaced array")

    @staticmethod
    def flatten(array):
        """
        Uses list comprehension to flatten array

        :param (array): An iterable to flatten
        :raises (PlotlyError): If iterable is not nested.
        :rtype (list): The flattened list.
        """
        try:
            return [item for sublist in array for item in sublist]
        except TypeError:
            raise exceptions.PlotlyError("Your data array could not be "
                                         "flattened! Make sure your data is "
                                         "entered as lists or ndarrays!")

    @staticmethod
    def create_quiver(x, y, u, v, scale=.1, arrow_scale=.3,
                      angle=math.pi / 9, **kwargs):
        """
        Returns data for a quiver plot.

        :param (list|ndarray) x: x coordinates of the arrow locations
        :param (list|ndarray) y: y coordinates of the arrow locations
        :param (list|ndarray) u: x components of the arrow vectors
        :param (list|ndarray) v: y components of the arrow vectors
        :param (float in [0,1]) scale: scales size of the arrows(ideally to
            avoid overlap). Default = .1
        :param (float in [0,1]) arrow_scale: value multiplied to length of barb
            to get length of arrowhead. Default = .3
        :param (angle in radians) angle: angle of arrowhead. Default = pi/9
        :param kwargs: kwargs passed through plotly.graph_objs.Scatter
            for more information on valid kwargs call
            help(plotly.graph_objs.Scatter)

        :rtype (trace): returns quiver trace

        Example 1: Trivial Quiver
        ```
        # 1 Arrow from (0,0) to (1,1)

        import math

        quiver = TraceFactory.create_quiver(x=[0], y=[0],
                                            u=[1], v=[1],
                                            scale=1)

        # Plot
        fig=Figure()
        fig['data'].append(quiver)
        py.iplot(fig, filename='quiver')
        ```

        Example 2: Quiver plot using meshgrid
        ```
        import numpy as np
        import math

        # Add data
        x,y = np.meshgrid(np.arange(0, 2, .2), np.arange(0, 2, .2))
        u = np.cos(x)*y
        v = np.sin(x)*y

        #Create quiver
        quiver = TraceFactory.create_quiver(x, y, u, v)

        # Plot
        fig=Figure()
        fig['data'].append(quiver)
        py.iplot(fig, filename='quiver')
        ```

        Example 3: Styling the quiver plot
        ```
        import numpy as np
        import math

        # Add data
        x, y = np.meshgrid(np.arange(-np.pi, math.pi, .5),
                           np.arange(-math.pi, math.pi, .5))
        u = np.cos(x)*y
        v = np.sin(x)*y

        # Create quiver
        quiver = TraceFactory.create_quiver(x, y, u, v, scale=.2,
                                            arrow_scale=.3, angle=math.pi/6,
                                            name='Wind Velocity',
                                            line=Line(width=1))

        # Plot
        fig=Figure()
        fig['data'].append(quiver)
        py.iplot(fig, filename='quiver')
        ```
        """
        TraceFactory.validate_equal_length(x, y, u, v)
        TraceFactory.validate_positive_scalars(arrow_scale=arrow_scale,
                                               scale=scale)

        barb_x, barb_y = _Quiver(x, y, u, v, scale,
                                 arrow_scale, angle).get_barbs()
        arrow_x, arrow_y = _Quiver(x, y, u, v, scale,
                                   arrow_scale, angle).get_quiver_arrows()
        quiver = Scatter(x=barb_x + arrow_x,
                         y=barb_y + arrow_y,
                         mode='lines', **kwargs)
        return quiver

    @staticmethod
    def create_streamline(x, y, u, v,
                          density=1, angle=math.pi / 9,
                          arrow_scale=.09, **kwargs):
        """
        Returns data for a streamline plot.

        :param (list|ndarray) x: 1 dimensional, evenly spaced list or array
        :param (list|ndarray) y: 1 dimensional, evenly spaced list or array
        :param (ndarray) u: 2 dimensional array
        :param (ndarray) v: 2 dimensional array
        :param (float|int) density: controls the density of streamlines in
            plot. This is multiplied by 30 to scale similiarly to other
            available streamline functions such as matplotlib.
            Default = 1
        :param (angle in radians) angle: angle of arrowhead. Default = pi/9
        :param (float in [0,1]) arrow_scale: value to scale length of arrowhead
            Default = .09
        :param kwargs: kwargs passed through plotly.graph_objs.Scatter
            for more information on valid kwargs call
            help(plotly.graph_objs.Scatter)

        :rtype (trace): returns streamline data

        Example 1: Plot simple streamline and increase arrow size
        ```
        import numpy as np
        import math

        # Add data
        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        Y, X = np.meshgrid(x, y)
        u = -1 - X**2 + Y
        v = 1 + X - Y**2
        u = u.T  # Transpose
        v = v.T  # Transpose

        # Create streamline
        streamline = TraceFactory.create_streamline(x, y, u, v, arrow_scale=.1)

        # Plot
        fig=Figure()
        fig['data'].append(streamline)
        py.iplot(fig, filename='streamline')
        ```

        Example 2: from nbviewer.ipython.org/github/barbagroup/AeroPython
        ```
        import numpy as np
        import math

        # Add data
        N = 50
        x_start, x_end = -2.0, 2.0
        y_start, y_end = -1.0, 1.0
        x = np.linspace(x_start, x_end, N)
        y = np.linspace(y_start, y_end, N)
        X, Y = np.meshgrid(x, y)
        ss = 5.0
        x_s, y_s = -1.0, 0.0

        # Compute the velocity field on the mesh grid
        u_s = ss/(2*np.pi) * (X-x_s)/((X-x_s)**2 + (Y-y_s)**2)
        v_s = ss/(2*np.pi) * (Y-y_s)/((X-x_s)**2 + (Y-y_s)**2)

        # Create streamline
        streamline = TraceFactory.create_streamline(x, y, u_s, v_s, density=2,
                                                    name='streamline')

        # Add source point
        point = Scatter(x=[x_s], y=[y_s], mode='markers',
                        marker=Marker(size=14), name='source point')

        # Plot
        fig=Figure()
        fig['data'].append(streamline)
        fig['data'].append(point)
        py.iplot(fig, filename='streamline')
        ```
        """
        TraceFactory.validate_equal_length(x, y)
        TraceFactory.validate_equal_length(u, v)
        TraceFactory.validate_streamline(x, y)
        TraceFactory.validate_positive_scalars(density=density,
                                               arrow_scale=arrow_scale)

        streamline_x, streamline_y = _Streamline(x, y, u, v,
                                                 density, angle,
                                                 arrow_scale).sum_streamlines()
        arrow_x, arrow_y = _Streamline(x, y, u, v,
                                       density, angle,
                                       arrow_scale).get_streamline_arrows()

        streamline = Scatter(x=streamline_x + arrow_x,
                             y=streamline_y + arrow_y,
                             mode='lines', **kwargs)
        return streamline


class _Quiver(TraceFactory):
    """
    Refer to TraceFactory.create_quiver() for docstring
    """
    def __init__(self, x, y, u, v,
                 scale, arrow_scale, angle, **kwargs):
        try:
            x = TraceFactory.flatten(x)
        except exceptions.PlotlyError:
            pass

        try:
            y = TraceFactory.flatten(y)
        except exceptions.PlotlyError:
            pass

        try:
            u = TraceFactory.flatten(u)
        except exceptions.PlotlyError:
            pass

        try:
            v = TraceFactory.flatten(v)
        except exceptions.PlotlyError:
            pass

        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.scale = scale
        self.arrow_scale = arrow_scale
        self.angle = angle
        self.end_x = []
        self.end_y = []
        self.scale_uv()
        barb_x, barb_y = self.get_barbs()
        arrow_x, arrow_y = self.get_quiver_arrows()

    def scale_uv(self):
        """
        Scales u and v to avoid overlap of the arrows.

        u and v are added to x and y to get the
        endpoints of the arrows so a smaller scale value will
        result in less overlap of arrows.
        """
        self.u = [i * self.scale for i in self.u]
        self.v = [i * self.scale for i in self.v]

    def get_barbs(self):
        """
        Creates x and y startpoint and endpoint pairs

        After finding the endpoint of each barb this zips startpoint and
        endpoint pairs to create 2 lists: x_values for barbs and y values
        for barbs

        :rtype: (list, list) barb_x, barb_y: list of startpoint and endpoint
            x_value pairs separated by a None to create the barb of the arrow,
            and list of startpoint and endpoint y_value pairs separated by a
            None to create the barb of the arrow.
        """
        self.end_x = [i + j for i, j in zip(self.x, self.u)]
        self.end_y = [i + j for i, j in zip(self.y, self.v)]
        empty = [None] * len(self.x)
        barb_x = self.flatten(zip(self.x, self.end_x, empty))
        barb_y = self.flatten(zip(self.y, self.end_y, empty))
        return barb_x, barb_y

    def get_quiver_arrows(self):
        """
        Creates lists of x and y values to plot the arrows

        Gets length of each barb then calculates the length of each side of
        the arrow. Gets angle of barb and applies angle to each side of the
        arrowhead. Next uses arrow_scale to scale the length of arrowhead and
        creates x and y values for arrowhead point1 and point2. Finally x and y
        values for point1, endpoint and point2s for each arrowhead are
        separated by a None and zipped to create lists of x and y values for
        the arrows.

        :rtype: (list, list) arrow_x, arrow_y: list of point1, endpoint, point2
            x_values separated by a None to create the arrowhead and list of
            point1, endpoint, point2 y_values separated by a None to create
            the barb of the arrow.
        """
        dif_x = [i - j for i, j in zip(self.end_x, self.x)]
        dif_y = [i - j for i, j in zip(self.end_y, self.y)]

        # Get barb lengths(default arrow length = 30% barb length)
        barb_len = [None] * len(self.x)
        for index in range(len(barb_len)):
            barb_len[index] = math.hypot(dif_x[index], dif_y[index])

        # Make arrow lengths
        arrow_len = [None] * len(self.x)
        arrow_len = [i * self.arrow_scale for i in barb_len]

        # Get barb angles
        barb_ang = [None] * len(self.x)
        for index in range(len(barb_ang)):
            barb_ang[index] = math.atan2(dif_y[index], dif_x[index])

        # Set angles to create arrow
        ang1 = [i + self.angle for i in barb_ang]
        ang2 = [i - self.angle for i in barb_ang]

        cos_ang1 = [None] * len(ang1)
        for index in range(len(ang1)):
            cos_ang1[index] = math.cos(ang1[index])
        seg1_x = [i * j for i, j in zip(arrow_len, cos_ang1)]

        sin_ang1 = [None] * len(ang1)
        for index in range(len(ang1)):
            sin_ang1[index] = math.sin(ang1[index])
        seg1_y = [i * j for i, j in zip(arrow_len, sin_ang1)]

        cos_ang2 = [None] * len(ang2)
        for index in range(len(ang2)):
            cos_ang2[index] = math.cos(ang2[index])
        seg2_x = [i * j for i, j in zip(arrow_len, cos_ang2)]

        sin_ang2 = [None] * len(ang2)
        for index in range(len(ang2)):
            sin_ang2[index] = math.sin(ang2[index])
        seg2_y = [i * j for i, j in zip(arrow_len, sin_ang2)]

        # Set coordinates to create arrow
        for index in range(len(self.end_x)):
            point1_x = [i - j for i, j in zip(self.end_x, seg1_x)]
            point1_y = [i - j for i, j in zip(self.end_y, seg1_y)]
            point2_x = [i - j for i, j in zip(self.end_x, seg2_x)]
            point2_y = [i - j for i, j in zip(self.end_y, seg2_y)]

        # Combine lists to create arrow
        empty = [None] * len(self.end_x)
        arrow_x = self.flatten(zip(point1_x, self.end_x, point2_x, empty))
        arrow_y = self.flatten(zip(point1_y, self.end_y, point2_y, empty))
        return arrow_x, arrow_y


class _Streamline(TraceFactory):
    """
    Refer to TraceFactory.create_streamline() for docstring
    """
    def __init__(self, x, y, u, v,
                 density, angle,
                 arrow_scale, **kwargs):
        self.x = np.array(x)
        self.y = np.array(y)
        self.u = np.array(u)
        self.v = np.array(v)
        self.angle = angle
        self.arrow_scale = arrow_scale
        self.density = int(30 * density)  # Scale similarly to other functions
        self.delta_x = self.x[1] - self.x[0]
        self.delta_y = self.y[1] - self.y[0]
        self.val_x = self.x
        self.val_y = self.y

        # Set up spacing
        self.blank = np.zeros((self.density, self.density))
        self.spacing_x = len(self.x) / float(self.density - 1)
        self.spacing_y = len(self.y) / float(self.density - 1)
        self.trajectories = []

        # Rescale speed onto axes-coordinates
        self.u = self.u / (self.x[-1] - self.x[0])
        self.v = self.v / (self.y[-1] - self.y[0])
        self.speed = np.sqrt(self.u ** 2 + self.v ** 2)

        # Rescale u and v for integrations.
        self.u *= len(self.x)
        self.v *= len(self.y)
        self.st_x = []
        self.st_y = []
        self.get_streamlines()
        streamline_x, streamline_y = self.sum_streamlines()
        arrows_x, arrows_y = self.get_streamline_arrows()

    def blank_pos(self, xi, yi):
        """
        Set up positions for trajectories to be used with rk4 function.
        """
        return (int((xi / self.spacing_x) + 0.5),
                int((yi / self.spacing_y) + 0.5))

    def value_at(self, a, xi, yi):
        """
        Set up for RK4 function, based on Bokeh's streamline code
        """
        if isinstance(xi, np.ndarray):
            self.x = xi.astype(np.int)
            self.y = yi.astype(np.int)
        else:
            self.val_x = np.int(xi)
            self.val_y = np.int(yi)
        a00 = a[self.val_y, self.val_x]
        a01 = a[self.val_y, self.val_x + 1]
        a10 = a[self.val_y + 1, self.val_x]
        a11 = a[self.val_y + 1, self.val_x + 1]
        xt = xi - self.val_x
        yt = yi - self.val_y
        a0 = a00 * (1 - xt) + a01 * xt
        a1 = a10 * (1 - xt) + a11 * xt
        return a0 * (1 - yt) + a1 * yt

    def rk4_integrate(self, x0, y0):
        """
        RK4 forward and back trajectories from the initial conditions.

        Adapted from Bokeh's streamline -uses Runge-Kutta method to fill
        x and y trajectories then checks length of traj (s in units of axes)
        """
        def f(xi, yi):
            dt_ds = 1. / self.value_at(self.speed, xi, yi)
            ui = self.value_at(self.u, xi, yi)
            vi = self.value_at(self.v, xi, yi)
            return ui * dt_ds, vi * dt_ds

        def g(xi, yi):
            dt_ds = 1. / self.value_at(self.speed, xi, yi)
            ui = self.value_at(self.u, xi, yi)
            vi = self.value_at(self.v, xi, yi)
            return -ui * dt_ds, -vi * dt_ds

        check = lambda xi, yi: (0 <= xi < len(self.x) - 1 and
                                0 <= yi < len(self.y) - 1)
        xb_changes = []
        yb_changes = []

        def rk4(x0, y0, f):
            ds = 0.01
            stotal = 0
            xi = x0
            yi = y0
            xb, yb = self.blank_pos(xi, yi)
            xf_traj = []
            yf_traj = []
            while check(xi, yi):
                xf_traj.append(xi)
                yf_traj.append(yi)
                try:
                    k1x, k1y = f(xi, yi)
                    k2x, k2y = f(xi + .5 * ds * k1x, yi + .5 * ds * k1y)
                    k3x, k3y = f(xi + .5 * ds * k2x, yi + .5 * ds * k2y)
                    k4x, k4y = f(xi + ds * k3x, yi + ds * k3y)
                except IndexError:
                    break
                xi += ds * (k1x + 2 * k2x + 2 * k3x + k4x) / 6.
                yi += ds * (k1y + 2 * k2y + 2 * k3y + k4y) / 6.
                if not check(xi, yi):
                    break
                stotal += ds
                new_xb, new_yb = self.blank_pos(xi, yi)
                if new_xb != xb or new_yb != yb:
                    if self.blank[new_yb, new_xb] == 0:
                        self.blank[new_yb, new_xb] = 1
                        xb_changes.append(new_xb)
                        yb_changes.append(new_yb)
                        xb = new_xb
                        yb = new_yb
                    else:
                        break
                if stotal > 2:
                    break
            return stotal, xf_traj, yf_traj

        sf, xf_traj, yf_traj = rk4(x0, y0, f)
        sb, xb_traj, yb_traj = rk4(x0, y0, g)
        stotal = sf + sb
        x_traj = xb_traj[::-1] + xf_traj[1:]
        y_traj = yb_traj[::-1] + yf_traj[1:]

        if len(x_traj) < 1:
            return None
        if stotal > .2:
            initxb, inityb = self.blank_pos(x0, y0)
            self.blank[inityb, initxb] = 1
            return x_traj, y_traj
        else:
            for xb, yb in zip(xb_changes, yb_changes):
                self.blank[yb, xb] = 0
            return None

    def traj(self, xb, yb):
        """

        Integrate trajectories

        :param (int) xb: results of passing xi through self.blank_pos
        :param (int) xy: results of passing yi through self.blank_pos

        Calculate each trajectory based on rk4 integrate method.
        """

        if xb < 0 or xb >= self.density or yb < 0 or yb >= self.density:
            return
        if self.blank[yb, xb] == 0:
            t = self.rk4_integrate(xb * self.spacing_x, yb * self.spacing_y)
            if t is not None:
                self.trajectories.append(t)

    def get_streamlines(self):
        """
        Get streamlines by building trajectory set.

        """
        for indent in range(self.density // 2):
            for xi in range(self.density - 2 * indent):
                self.traj(xi + indent, indent)
                self.traj(xi + indent, self.density - 1 - indent)
                self.traj(indent, xi + indent)
                self.traj(self.density - 1 - indent, xi + indent)

        self.st_x = [np.array(t[0]) * self.delta_x + self.x[0] for t in
                     self.trajectories]
        self.st_y = [np.array(t[1]) * self.delta_y + self.y[0] for t in
                     self.trajectories]

        for index in range(len(self.st_x)):
            self.st_x[index] = self.st_x[index].tolist()
            self.st_x[index].append(np.nan)

        for index in range(len(self.st_y)):
            self.st_y[index] = self.st_y[index].tolist()
            self.st_y[index].append(np.nan)

    def get_streamline_arrows(self):
        """
        Makes an arrow for each streamline.

        Gets angle of streamline at 1/3 mark and creates arrow coordinates
        based off of user defined angle and arrow_scale.

        :param (array) st_x: x-values for all streamlines
        :param (array) st_y: y-values for all streamlines
        :param (angle in radians) angle: angle of arrowhead. Default = pi/9
        :param (float in [0,1]) arrow_scale: value to scale length of arrowhead
            Default = .09
        :rtype (list, list) arrows_x: x-values to create arrowhead and
            arrows_y: y-values to create arrowhead
        """
        arrow_end_x = np.empty((len(self.st_x)))
        arrow_end_y = np.empty((len(self.st_y)))
        arrow_start_x = np.empty((len(self.st_x)))
        arrow_start_y = np.empty((len(self.st_y)))
        for index in range(len(self.st_x)):
            arrow_end_x[index] = (self.st_x[index]
                                  [int(len(self.st_x[index]) / 3)])
            arrow_start_x[index] = (self.st_x[index]
                                    [(int(len(self.st_x[index]) / 3)) - 1])
            arrow_end_y[index] = (self.st_y[index]
                                  [int(len(self.st_y[index]) / 3)])
            arrow_start_y[index] = (self.st_y[index]
                                    [(int(len(self.st_y[index]) / 3)) - 1])

        dif_x = arrow_end_x - arrow_start_x
        dif_y = arrow_end_y - arrow_start_y

        streamline_ang = np.arctan(dif_y / dif_x)

        ang1 = streamline_ang + (self.angle)
        ang2 = streamline_ang - (self.angle)

        seg1_x = np.cos(ang1) * self.arrow_scale
        seg1_y = np.sin(ang1) * self.arrow_scale
        seg2_x = np.cos(ang2) * self.arrow_scale
        seg2_y = np.sin(ang2) * self.arrow_scale

        point1_x = np.empty((len(dif_x)))
        point1_y = np.empty((len(dif_y)))
        point2_x = np.empty((len(dif_x)))
        point2_y = np.empty((len(dif_y)))

        for index in range(len(dif_x)):
            if dif_x[index] >= 0:
                point1_x[index] = arrow_end_x[index] - seg1_x[index]
                point1_y[index] = arrow_end_y[index] - seg1_y[index]
                point2_x[index] = arrow_end_x[index] - seg2_x[index]
                point2_y[index] = arrow_end_y[index] - seg2_y[index]
            else:
                point1_x[index] = arrow_end_x[index] + seg1_x[index]
                point1_y[index] = arrow_end_y[index] + seg1_y[index]
                point2_x[index] = arrow_end_x[index] + seg2_x[index]
                point2_y[index] = arrow_end_y[index] + seg2_y[index]

        space = np.empty((len(point1_x)))
        space[:] = np.nan

        # Combine arrays into matrix
        arrows_x = np.matrix([point1_x, arrow_end_x, point2_x, space])
        arrows_x = np.array(arrows_x)
        arrows_x = arrows_x.flatten('F')
        arrows_x = arrows_x.tolist()

        # Combine arrays into matrix
        arrows_y = np.matrix([point1_y, arrow_end_y, point2_y, space])
        arrows_y = np.array(arrows_y)
        arrows_y = arrows_y.flatten('F')
        arrows_y = arrows_y.tolist()

        return arrows_x, arrows_y

    def sum_streamlines(self):
        """
        Makes all streamlines readable as a single trace.

        :rtype (list, list): streamline_x: all x values for each streamline
            combined into single list and streamline_y: all y values for each
            streamline combined into single list
        """
        streamline_x = sum(self.st_x, [])
        streamline_y = sum(self.st_y, [])
        return streamline_x, streamline_y


_DEFAULT_INCREASING_COLOR = '#3D9970'  # http://clrs.cc
_DEFAULT_DECREASING_COLOR = '#FF4136'


class FigureFactory(object):
    """
    BETA functions to create specific chart types.

    See FigureFactory.create_ohlc for more infomation and examples of open high
    low close charts or FigureFactory.create_candlestick for more information
    and examples of candlestick charts.

    """

    @staticmethod
    def validate_ohlc(open, high, low, close, direction, **kwargs):
        """
        ohlc and candlestick specific validations

        Specifically, this checks that the high value is the greatest value and
        the low value is the lowest value in each unit.

        See FigureFactory.create_ohlc() or FigureFactory.create_candlestick()
        for params

        :raises: (PlotlyError) If the high value is not the greatest value in
            each unit.
        :raises: (PlotlyError) If the low value is not the lowest value in each
            unit.
        :raises: (PlotlyError) If direction is not 'increasing' or 'decreasing'
        """
        for lst in [open, low, close]:
            for index in range(len(high)):
                if high[index] < lst[index]:
                    raise exceptions.PlotlyError("Oops! Looks like some of "
                                                 "your high values are less "
                                                 "the corresponding open, "
                                                 "low, or close values. "
                                                 "Double check that your data "
                                                 "is entered in O-H-L-C order")

        for lst in [open, high, close]:
            for index in range(len(low)):
                if low[index] > lst[index]:
                    raise exceptions.PlotlyError("Oops! Looks like some of "
                                                 "your low values are greater "
                                                 "than the corresponding high"
                                                 ", open, or close values. "
                                                 "Double check that your data "
                                                 "is entered in O-H-L-C order")

        direction_opts = ('increasing', 'decreasing', 'both')
        if direction not in direction_opts:
            raise exceptions.PlotlyError("direction must be defined as "
                                         "'increasing', 'decreasing', or "
                                         "'both'")

    @staticmethod
    def _make_increasing_ohlc(open, high, low, close, dates, **kwargs):
        """
        Makes increasing ohlc sticks

        _make_increasing_ohlc() and _make_decreasing_ohlc separate the
        increasing trace from the decreasing trace so kwargs (such as
        color) can be passed separately to increasing or decreasing traces
        when direction is set to 'increasing' or 'decreasing' in
        FigureFactory.create_candlestick()

        :param (list) open: opening values
        :param (list) high: high values
        :param (list) low: low values
        :param (list) close: closing values
        :param (list) dates: list of datetime objects. Default: None
        :param kwargs: kwargs to be passed to increasing trace via
            plotly.graph_objs.Scatter.

        :rtype (trace) ohlc_incr_data: Scatter trace of all increasing ohlc
            sticks.
        """
        (flat_increase_x,
         flat_increase_y,
         text_increase) = _OHLC(open, high, low, close, dates).get_increase()

        if 'name' in kwargs:
            showlegend = True
        else:
            kwargs.setdefault('name', 'Increasing')
            showlegend = False

        kwargs.setdefault('line', dict(color=_DEFAULT_INCREASING_COLOR,
                                       width=1))
        kwargs.setdefault('text', text_increase)

        ohlc_incr = dict(type='scatter',
                         x=flat_increase_x,
                         y=flat_increase_y,
                         mode='lines',
                         showlegend=showlegend,
                         **kwargs)
        return ohlc_incr

    @staticmethod
    def _make_decreasing_ohlc(open, high, low, close, dates, **kwargs):
        """
        Makes decreasing ohlc sticks

        :param (list) open: opening values
        :param (list) high: high values
        :param (list) low: low values
        :param (list) close: closing values
        :param (list) dates: list of datetime objects. Default: None
        :param kwargs: kwargs to be passed to increasing trace via
            plotly.graph_objs.Scatter.

        :rtype (trace) ohlc_decr_data: Scatter trace of all decreasing ohlc
            sticks.
        """
        (flat_decrease_x,
         flat_decrease_y,
         text_decrease) = _OHLC(open, high, low, close, dates).get_decrease()

        kwargs.setdefault('line', dict(color=_DEFAULT_DECREASING_COLOR,
                                       width=1))
        kwargs.setdefault('text', text_decrease)
        kwargs.setdefault('showlegend', False)
        kwargs.setdefault('name', 'Decreasing')

        ohlc_decr = dict(type='scatter',
                         x=flat_decrease_x,
                         y=flat_decrease_y,
                         mode='lines',
                         **kwargs)
        return ohlc_decr

    @staticmethod
    def create_ohlc(open, high, low, close,
                    dates=None, direction='both',
                    **kwargs):
        """
        BETA function that creates an ohlc chart

        :param (list) open: opening values
        :param (list) high: high values
        :param (list) low: low values
        :param (list) close: closing
        :param (list) dates: list of datetime objects. Default: None
        :param (string) direction: direction can be 'increasing', 'decreasing',
            or 'both'. When the direction is 'increasing', the returned figure
            consists of all units where the close value is greater than the
            corresponding open value, and when the direction is 'decreasing',
            the returned figure consists of all units where the close value is
            less than or equal to the corresponding open value. When the
            direction is 'both', both increasing and decreasing units are
            returned. Default: 'both'
        :param kwargs: kwargs passed through plotly.graph_objs.Scatter.
            These kwargs describe other attributes about the ohlc Scatter trace
            such as the color or the legend name. For more information on valid
            kwargs call help(plotly.graph_objs.Scatter)

        :rtype (dict): returns a representation of an ohlc chart figure.

        Example 1: Simple OHLC chart from a Pandas DataFrame
        ```
        import plotly.plotly as py
        from plotly.tools import FigureFactory as FF
        from datetime import datetime

        import pandas.io.data as web

        df = web.DataReader("aapl", 'yahoo', datetime(2008, 8, 15), datetime(2008, 10, 15))
        fig = FF.create_ohlc(df.Open, df.High, df.Low, df.Close, dates=df.index)

        py.plot(fig, filename='finance/aapl-ohlc')
        ```

        Example 2: Add text and annotations to the OHLC chart
        ```
        import plotly.plotly as py
        from plotly.tools import FigureFactory as FF
        from datetime import datetime

        import pandas.io.data as web

        df = web.DataReader("aapl", 'yahoo', datetime(2008, 8, 15), datetime(2008, 10, 15))
        fig = FF.create_ohlc(df.Open, df.High, df.Low, df.Close, dates=df.index)

        # Update the fig - all options here: https://plot.ly/python/reference/#Layout
        fig['layout'].update({
            'title': 'The Great Recession',
            'yaxis': {'title': 'AAPL Stock'},
            'shapes': [{
                'x0': '2008-09-15', 'x1': '2008-09-15', 'type': 'line',
                'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper',
                'line': {'color': 'rgb(40,40,40)', 'width': 0.5}
            }],
            'annotations': [{
                'text': "the fall of Lehman Brothers",
                'x': '2008-09-15', 'y': 1.02,
                'xref': 'x', 'yref': 'paper',
                'showarrow': False, 'xanchor': 'left'
            }]
        })

        py.plot(fig, filename='finance/aapl-recession-ohlc', validate=False)
        ```

        Example 3: Customize the OHLC colors
        ```
        import plotly.plotly as py
        from plotly.tools import FigureFactory as FF
        from plotly.graph_objs import Line, Marker
        from datetime import datetime

        import pandas.io.data as web

        df = web.DataReader("aapl", 'yahoo', datetime(2008, 1, 1), datetime(2009, 4, 1))

        # Make increasing ohlc sticks and customize their color and name
        fig_increasing = FF.create_ohlc(df.Open, df.High, df.Low, df.Close, dates=df.index,
            direction='increasing', name='AAPL',
            line=Line(color='rgb(150, 200, 250)'))

        # Make decreasing ohlc sticks and customize their color and name
        fig_decreasing = FF.create_ohlc(df.Open, df.High, df.Low, df.Close, dates=df.index,
            direction='decreasing',
            line=Line(color='rgb(128, 128, 128)'))

        # Initialize the figure
        fig = fig_increasing

        # Add decreasing data with .extend()
        fig['data'].extend(fig_decreasing['data'])

        py.iplot(fig, filename='finance/aapl-ohlc-colors', validate=False)
        ```

        Example 4: OHLC chart with datetime objects
        ```
        import plotly.plotly as py
        from plotly.tools import FigureFactory as FF

        from datetime import datetime

        # Add data
        open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
        high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
        low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
        close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
        dates = [datetime(year=2013, month=10, day=10),
                 datetime(year=2013, month=11, day=10),
                 datetime(year=2013, month=12, day=10),
                 datetime(year=2014, month=1, day=10),
                 datetime(year=2014, month=2, day=10)]

        # Create ohlc
        fig = FF.create_ohlc(open_data, high_data,
            low_data, close_data, dates=dates)

        py.iplot(fig, filename='finance/simple-ohlc', validate=False)
        ```
        """
        if dates is not None:
            TraceFactory.validate_equal_length(open, high, low, close, dates)
        else:
            TraceFactory.validate_equal_length(open, high, low, close)
        FigureFactory.validate_ohlc(open, high, low, close, direction,
                                    **kwargs)

        if direction is 'increasing':
            ohlc_incr = FigureFactory._make_increasing_ohlc(open, high,
                                                            low, close,
                                                            dates, **kwargs)
            data = [ohlc_incr]
        elif direction is 'decreasing':
            ohlc_decr = FigureFactory._make_decreasing_ohlc(open, high,
                                                            low, close,
                                                            dates, **kwargs)
            data = [ohlc_decr]
        else:
            ohlc_incr = FigureFactory._make_increasing_ohlc(open, high,
                                                            low, close,
                                                            dates, **kwargs)
            ohlc_decr = FigureFactory._make_decreasing_ohlc(open, high,
                                                            low, close,
                                                            dates, **kwargs)
            data = [ohlc_incr, ohlc_decr]

        layout = graph_objs.Layout(xaxis=dict(zeroline=False),
                                   hovermode='closest')

        return dict(data=data, layout=layout)

    @staticmethod
    def _make_increasing_candle(open, high, low, close, dates, **kwargs):
        """
        Makes stacked bar and vertical line for increasing candlesticks

        _make_increasing_candle() and _make_decreasing_candle separate the
        increasing traces from the decreasing traces so kwargs (such as
        color) can be passed separately to increasing or decreasing traces
        when direction is set to 'increasing' or 'decreasing' in
        FigureFactory.create_candlestick()

        :param (list) open: opening values
        :param (list) high: high values
        :param (list) low: low values
        :param (list) close: closing values
        :param (list) dates: list of datetime objects. Default: None
        :param kwargs: kwargs to be passed to increasing trace via
            plotly.graph_objs.Scatter.

        :rtype (list) candle_incr_data: list of three traces: hidden_bar_incr,
            candle_bar_incr, candle_line_incr: returns the first (invisible)
            stacked bar, second (visible) stacked bar, and trace composed of
            vertical lines for each increasing candlestick.
        """
        (increase_x,
         increase_open,
         increase_dif,
         stick_increase_y,
         stick_increase_x) = (_Candlestick(open, high, low, close, dates,
                                           **kwargs).get_candle_increase())

        if 'name' in kwargs:
            showlegend = True
        else:
            kwargs.setdefault('name', 'Increasing')
            showlegend = False

        kwargs.setdefault('marker', dict(color=_DEFAULT_INCREASING_COLOR))
        kwargs.setdefault('line', dict(color=_DEFAULT_INCREASING_COLOR))

        hidden_bar_incr = dict(type='bar',
                               x=increase_x,
                               y=increase_open,
                               marker=Marker(color='rgba(0, 0, 0, 0)'),
                               legendgroup='Increasing',
                               showlegend=False,
                               hoverinfo='none')
        candle_bar_incr = dict(type='bar',
                               x=increase_x,
                               y=increase_dif,
                               legendgroup='Increasing',
                               showlegend=False,
                               hoverinfo='none',
                               **kwargs)
        candle_line_incr = dict(type='scatter',
                                x=stick_increase_x,
                                y=stick_increase_y,
                                mode='lines',
                                legendgroup='Increasing',
                                text=('Low', 'Open', 'Close',
                                      'High', '') * len(increase_x),
                                showlegend=showlegend,
                                **kwargs)
        candle_incr_data = [hidden_bar_incr, candle_bar_incr, candle_line_incr]
        return candle_incr_data

    @staticmethod
    def _make_decreasing_candle(open, high, low, close, dates, **kwargs):
        """
        Makes stacked bar and vertical line for decreasing candlesticks

        :param (list) open: opening values
        :param (list) high: high values
        :param (list) low: low values
        :param (list) close: closing values
        :param (list) dates: list of datetime objects. Default: None
        :param kwargs: kwargs to be passed to decreasing trace via
            plotly.graph_objs.Scatter.

        :rtype (list) candle_decr_data: list of three traces: hidden_bar_decr,
            candle_bar_decr, candle_line_decr: returns the first (invisible)
            stacked bar, second (visible) stacked bar, and trace composed of
            vertical lines for each decreasing candlestick.
        """

        (decrease_x,
         decrease_close,
         decrease_dif,
         stick_decrease_y,
         stick_decrease_x) = (_Candlestick(open, high, low, close, dates,
                                           **kwargs).get_candle_decrease())

        kwargs.setdefault('marker', dict(color=_DEFAULT_DECREASING_COLOR))
        kwargs.setdefault('line', dict(color=_DEFAULT_DECREASING_COLOR))
        kwargs.setdefault('name', 'Decreasing')

        hidden_bar_decr = dict(type='bar',
                               x=decrease_x,
                               y=decrease_close,
                               marker=Marker(color='rgba(0, 0, 0, 0)'),
                               legendgroup='Decreasing',
                               showlegend=False,
                               hoverinfo='none')
        candle_bar_decr = dict(type='bar',
                               x=decrease_x,
                               y=decrease_dif,
                               legendgroup='Decreasing',
                               showlegend=False,
                               hoverinfo='none',
                               **kwargs)
        candle_line_decr = dict(type='scatter',
                                x=stick_decrease_x,
                                y=stick_decrease_y,
                                mode='lines',
                                legendgroup='Decreasing',
                                showlegend=False,
                                text=('Low', 'Close', 'Open',
                                      'High', '') * len(decrease_x),
                                **kwargs)
        candle_decr_data = [hidden_bar_decr, candle_bar_decr, candle_line_decr]
        return candle_decr_data

    @staticmethod
    def create_candlestick(open, high, low, close,
                           dates=None, direction='both', **kwargs):
        """
        BETA function that creates a candlestick chart

        :param (list) open: opening values
        :param (list) high: high values
        :param (list) low: low values
        :param (list) close: closing values
        :param (list) dates: list of datetime objects. Default: None
        :param (string) direction: direction can be 'increasing', 'decreasing',
            or 'both'. When the direction is 'increasing', the returned figure
            consists of all candlesticks where the close value is greater than
            the corresponding open value, and when the direction is
            'decreasing', the returned figure consists of all candlesticks
            where the close value is less than or equal to the corresponding
            open value. When the direction is 'both', both increasing and
            decreasing candlesticks are returned. Default: 'both'
        :param kwargs: kwargs passed through plotly.graph_objs.Scatter.
            These kwargs describe other attributes about the ohlc Scatter trace
            such as the color or the legend name. For more information on valid
            kwargs call help(plotly.graph_objs.Scatter)

        :rtype (dict): returns a representation of candlestick chart figure.

        Example 1: Simple candlestick chart from a Pandas DataFrame
        ```
        import plotly.plotly as py
        from plotly.tools import FigureFactory as FF
        from datetime import datetime

        import pandas.io.data as web

        df = web.DataReader("aapl", 'yahoo', datetime(2007, 10, 1), datetime(2009, 4, 1))
        fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)
        py.plot(fig, filename='finance/aapl-candlestick', validate=False)
        ```

        Example 2: Add text and annotations to the candlestick chart
        ```
        fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)
        # Update the fig - all options here: https://plot.ly/python/reference/#Layout
        fig['layout'].update({
            'title': 'The Great Recession',
            'yaxis': {'title': 'AAPL Stock'},
            'shapes': [{
                'x0': '2007-12-01', 'x1': '2007-12-01',
                'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper',
                'line': {'color': 'rgb(30,30,30)', 'width': 1}
            }],
            'annotations': [{
                'x': '2007-12-01', 'y': 0.05, 'xref': 'x', 'yref': 'paper',
                'showarrow': False, 'xanchor': 'left',
                'text': 'Official start of the recession'
            }]
        })
        py.plot(fig, filename='finance/aapl-recession-candlestick', validate=False)
        ```

        Example 3: Customize the candlestick colors
        ```
        import plotly.plotly as py
        from plotly.tools import FigureFactory as FF
        from plotly.graph_objs import Line, Marker
        from datetime import datetime

        import pandas.io.data as web

        df = web.DataReader("aapl", 'yahoo', datetime(2008, 1, 1), datetime(2009, 4, 1))
        fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)

        # Make increasing ohlc sticks and customize their color and name
        fig_increasing = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index,
            direction='increasing', name='AAPL',
            marker=Marker(color='rgb(150, 200, 250)'),
            line=Line(color='rgb(150, 200, 250)'))

        # Make decreasing ohlc sticks and customize their color and name
        fig_decreasing = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index,
            direction='decreasing',
            marker=Marker(color='rgb(128, 128, 128)'),
            line=Line(color='rgb(128, 128, 128)'))

        # Initialize the figure
        fig = fig_increasing

        # Add decreasing data with .extend()
        fig['data'].extend(fig_decreasing['data'])

        py.iplot(fig, filename='finance/aapl-candlestick-custom', validate=False)
        ```

        Example 4: Candlestick chart with datetime objects
        ```
        import plotly.plotly as py
        from plotly.tools import FigureFactory as FF

        from datetime import datetime

        # Add data
        open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
        high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
        low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
        close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
        dates = [datetime(year=2013, month=10, day=10),
                 datetime(year=2013, month=11, day=10),
                 datetime(year=2013, month=12, day=10),
                 datetime(year=2014, month=1, day=10),
                 datetime(year=2014, month=2, day=10)]

        # Create ohlc
        fig = FF.create_candlestick(open_data, high_data,
            low_data, close_data, dates=dates)

        py.iplot(fig, filename='finance/simple-candlestick', validate=False)
        ```
        """
        if dates is not None:
            TraceFactory.validate_equal_length(open, high, low, close, dates)
        else:
            TraceFactory.validate_equal_length(open, high, low, close)
        FigureFactory.validate_ohlc(open, high, low, close, direction,
                                    **kwargs)

        if direction is 'increasing':
            candle_incr_data = FigureFactory._make_increasing_candle(open,
                                                                     high,
                                                                     low,
                                                                     close,
                                                                     dates,
                                                                     **kwargs)
            data = candle_incr_data
        elif direction is 'decreasing':
            candle_decr_data = FigureFactory._make_decreasing_candle(open,
                                                                     high,
                                                                     low,
                                                                     close,
                                                                     dates,
                                                                     **kwargs)
            data = candle_decr_data
        else:
            candle_incr_data = FigureFactory._make_increasing_candle(open,
                                                                     high,
                                                                     low,
                                                                     close,
                                                                     dates,
                                                                     **kwargs)
            candle_decr_data = FigureFactory._make_decreasing_candle(open,
                                                                     high,
                                                                     low,
                                                                     close,
                                                                     dates,
                                                                     **kwargs)
            data = candle_incr_data + candle_decr_data

        layout = graph_objs.Layout(barmode='stack',
                                   bargroupgap=0.2,
                                   yaxis=dict(range=[(min(low) -
                                                     ((max(high) - min(low)) *
                                                      .1)),
                                                     (max(high) + ((max(high) -
                                                                    min(low)) *
                                                      .1))]))
        layout['yaxis']['fixedrange'] = True

        return dict(data=data, layout=layout)


class _OHLC(FigureFactory):
    """
    Refer to FigureFactory.create_ohlc_increase() for docstring.
    """
    def __init__(self, open, high, low, close, dates, **kwargs):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.empty = [None] * len(open)
        self.dates = dates

        self.all_x = []
        self.all_y = []
        self.increase_x = []
        self.increase_y = []
        self.decrease_x = []
        self.decrease_y = []
        self.get_all_xy()
        self.separate_increase_decrease()

    def get_all_xy(self):
        """
        Zip data to create OHLC shape

        OHLC shape: low to high vertical bar with
        horizontal branches for open and close values.
        If dates were added, the smallest date difference is calculated and
        multiplied by .2 to get the length of the open and close branches.
        If no date data was provided, the x-axis is a list of integers and the
        length of the open and close branches is .2.
        """
        self.all_y = list(zip(self.open, self.open, self.high,
                              self.low, self.close, self.close, self.empty))
        if self.dates is not None:
            date_dif = []
            for i in range(len(self.dates) - 1):
                date_dif.append(self.dates[i + 1] - self.dates[i])
            date_dif_min = (min(date_dif)) / 5
            self.all_x = [[x - date_dif_min, x, x, x, x, x +
                           date_dif_min, None] for x in self.dates]
        else:
            self.all_x = [[x - .2, x, x, x, x, x + .2, None]
                          for x in range(len(self.open))]

    def separate_increase_decrease(self):
        """
        Separate data into two groups: increase and decrease

        (1) Increase, where close > open and
        (2) Decrease, where close <= open
        """

        for index in range(len(self.open)):
            if self.close[index] is None:
                pass
            elif self.close[index] > self.open[index]:
                self.increase_x.append(self.all_x[index])
                self.increase_y.append(self.all_y[index])
            else:
                self.decrease_x.append(self.all_x[index])
                self.decrease_y.append(self.all_y[index])

    def get_increase(self):
        """
        Flatten increase data and get increase text

        :rtype (list, list, list): flat_increase_x: x-values for the increasing
            trace, flat_increase_y: y=values for the increasing trace and
            text_increase: hovertext for the increasing trace
        """
        flat_increase_x = TraceFactory.flatten(self.increase_x)
        flat_increase_y = TraceFactory.flatten(self.increase_y)
        text_increase = (("Open", "Open", "High",
                          "Low", "Close", "Close", '')
                         * (len(self.increase_x)))

        return flat_increase_x, flat_increase_y, text_increase

    def get_decrease(self):
        """
        Flatten decrease data and get decrease text

        :rtype (list, list, list): flat_decrease_x: x-values for the decreasing
            trace, flat_decrease_y: y=values for the decreasing trace and
            text_decrease: hovertext for the decreasing trace
        """
        flat_decrease_x = TraceFactory.flatten(self.decrease_x)
        flat_decrease_y = TraceFactory.flatten(self.decrease_y)
        text_decrease = (("Open", "Open", "High",
                          "Low", "Close", "Close", '')
                         * (len(self.decrease_x)))

        return flat_decrease_x, flat_decrease_y, text_decrease


class _Candlestick(FigureFactory):
    """
    Refer to FigureFactory.create_candlestick() for docstring.
    """
    def __init__(self, open, high, low, close, dates, **kwargs):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        if dates is not None:
            self.x = dates
        else:
            self.x = [x for x in range(len(self.open))]
        self.get_candle_increase()

    def get_candle_increase(self):
        """
        Separate increasing data from decreasing data.

        The data is increasing when close value > open value
        and decreasing when the close value <= open value.
        """
        increase_open = []
        increase_high = []
        increase_low = []
        increase_close = []
        increase_x = []
        for index in range(len(self.open)):
            if self.close[index] > self.open[index]:
                increase_open.append(self.open[index])
                increase_high.append(self.high[index])
                increase_low.append(self.low[index])
                increase_close.append(self.close[index])
                increase_x.append(self.x[index])

        increase_dif = [cl - op for (cl, op)
                        in zip(increase_close, increase_open)]

        increase_empty = [None] * len(increase_open)
        stick_increase_y = list(zip(increase_low, increase_open,
                                    increase_close, increase_high,
                                    increase_empty))
        stick_increase_x = [[x, x, x, x, None] for x in increase_x]
        stick_increase_y = TraceFactory.flatten(stick_increase_y)
        stick_increase_x = TraceFactory.flatten(stick_increase_x)

        return (increase_x, increase_open, increase_dif,
                stick_increase_y, stick_increase_x)

    def get_candle_decrease(self):
        """
        Separate increasing data from decreasing data.

        The data is increasing when close value > open value
        and decreasing when the close value <= open value.
        """
        decrease_open = []
        decrease_high = []
        decrease_low = []
        decrease_close = []
        decrease_x = []

        for index in range(len(self.open)):
            if self.close[index] <= self.open[index]:
                decrease_open.append(self.open[index])
                decrease_high.append(self.high[index])
                decrease_low.append(self.low[index])
                decrease_close.append(self.close[index])
                decrease_x.append(self.x[index])

        decrease_dif = [op - cl for (op, cl)
                        in zip(decrease_open, decrease_close)]

        decrease_empty = [None] * len(decrease_open)
        stick_decrease_y = list(zip(decrease_low, decrease_close,
                                    decrease_open, decrease_high,
                                    decrease_empty))
        stick_decrease_x = [[x, x, x, x, None] for x in decrease_x]

        stick_decrease_y = TraceFactory.flatten(stick_decrease_y)
        stick_decrease_x = TraceFactory.flatten(stick_decrease_x)

        return (decrease_x, decrease_close, decrease_dif,
                stick_decrease_y, stick_decrease_x)

