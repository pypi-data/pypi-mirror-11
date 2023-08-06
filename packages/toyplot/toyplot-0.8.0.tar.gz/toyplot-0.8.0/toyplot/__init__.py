# Copyright 2014, Sandia Corporation. Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains certain
# rights in this software.

from __future__ import division

__version__ = "0.8.0"

from toyplot.canvas import Canvas
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def bars(
        a,
        b=None,
        c=None,
        along="x",
        baseline="stacked",
        color=None,
        opacity=1.0,
        title=None,
        style=None,
        filename=None,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
        show=True,
        xshow=True,
        yshow=True,
        label=None,
        xlabel=None,
        ylabel=None,
        xscale="linear",
        yscale="linear",
        padding=10,
        width=None,
        height=None,
        canvas_style=None):
    """Convenience function for creating a bar plot in a single call.

    See :meth:`toyplot.axes.Cartesian.bars`, :meth:`toyplot.canvas.Canvas.axes`, and :class:`toyplot.canvas.Canvas` for parameter descriptions.

    Returns
    -------
    canvas: :class:`toyplot.canvas.Canvas`
      A new canvas object.
    axes: :class:`toyplot.axes.Cartesian`
      A new set of 2D axes that fill the canvas.
    mark: :class:`toyplot.mark.BarMagnitudes` or :class:`toyplot.mark.BarBoundaries`
      The new bar mark.
    """
    canvas = Canvas(width=width, height=height, style=canvas_style)
    axes = canvas.axes(
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        show=show,
        xshow=xshow,
        yshow=yshow,
        label=label,
        xlabel=xlabel,
        ylabel=ylabel,
        xscale=xscale,
        yscale=yscale,
        padding=padding)
    mark = axes.bars(
        a=a,
        b=b,
        c=c,
        along=along,
        baseline=baseline,
        color=color,
        opacity=opacity,
        title=title,
        style=style,
        filename=filename)
    return canvas, axes, mark


def fill(
        a,
        b=None,
        c=None,
        along="x",
        baseline=None,
        color=None,
        opacity=1.0,
        title=None,
        style=None,
        filename=None,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
        show=True,
        xshow=True,
        yshow=True,
        label=None,
        xlabel=None,
        ylabel=None,
        xscale="linear",
        yscale="linear",
        padding=10,
        width=None,
        height=None,
        canvas_style=None):
    """Convenience function for creating a fill plot in a single call.

    See :meth:`toyplot.axes.Cartesian.fill`, :meth:`toyplot.canvas.Canvas.axes`, and :class:`toyplot.canvas.Canvas` for parameter descriptions.

    Returns
    -------
    canvas: :class:`toyplot.canvas.Canvas`
      A new canvas object.
    axes: :class:`toyplot.axes.Cartesian`
      A new set of 2D axes that fill the canvas.
    mark: :class:`toyplot.mark.FillBoundaries` or :class:`toyplot.mark.FillMagnitudes`
      The new bar mark.
    """
    canvas = Canvas(width=width, height=height, style=canvas_style)
    axes = canvas.axes(
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        show=show,
        xshow=xshow,
        yshow=yshow,
        label=label,
        xlabel=xlabel,
        ylabel=ylabel,
        xscale=xscale,
        yscale=yscale,
        padding=padding)
    mark = axes.fill(
        a=a,
        b=b,
        c=c,
        along=along,
        baseline=baseline,
        color=color,
        opacity=opacity,
        title=title,
        style=style,
        filename=filename)
    return canvas, axes, mark


def matrix(
        data,
        label=None,
        tlabel=None,
        llabel=None,
        rlabel=None,
        blabel=None,
        step=1,
        tshow=None,
        lshow=None,
        rshow=None,
        bshow=None,
        tlocator=None,
        llocator=None,
        rlocator=None,
        blocator=None,
        width=None,
        height=None,
        canvas_style=None):
    """Convenience function to create a matrix visualization in a single call.

    See :meth:`toyplot.canvas.Canvas.matrix`, and :class:`toyplot.canvas.Canvas` for parameter descriptions.

    Returns
    -------
    canvas: :class:`toyplot.canvas.Canvas`
      A new canvas object.
    table: :class:`toyplot.axes.Table`
      A new set of table axes that fill the canvas.
    """
    canvas = Canvas(width=width, height=height, style=canvas_style)
    table = canvas.matrix(
        data=data,
        label=label,
        tlabel=tlabel,
        llabel=llabel,
        rlabel=rlabel,
        blabel=blabel,
        step=step,
        tshow=tshow,
        lshow=lshow,
        rshow=rshow,
        bshow=bshow,
        tlocator=tlocator,
        llocator=llocator,
        rlocator=rlocator,
        blocator=blocator)
    return canvas, table


def plot(
        a,
        b=None,
        along="x",
        color=None,
        stroke_width=2.0,
        opacity=1.0,
        title=None,
        marker=None,
        size=20,
        mfill=None,
        mopacity=1.0,
        mtitle = None,
        style=None,
        mstyle=None,
        mlstyle=None,
        filename=None,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
        show=True,
        xshow=True,
        yshow=True,
        label=None,
        xlabel=None,
        ylabel=None,
        xscale="linear",
        yscale="linear",
        padding=10,
        width=None,
        height=None,
        canvas_style=None):
    """Convenience function for creating a line plot in a single call.

    See :meth:`toyplot.axes.Cartesian.plot`, :meth:`toyplot.canvas.Canvas.axes`, and :class:`toyplot.canvas.Canvas` for parameter descriptions.

    Returns
    -------
    canvas: :class:`toyplot.canvas.Canvas`
      A new canvas object.
    axes: :class:`toyplot.axes.Cartesian`
      A new set of 2D axes that fill the canvas.
    mark: :class:`toyplot.mark.Plot`
      The new plot mark.
    """
    canvas = Canvas(width=width, height=height, style=canvas_style)
    axes = canvas.axes(
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        show=show,
        xshow=xshow,
        yshow=yshow,
        label=label,
        xlabel=xlabel,
        ylabel=ylabel,
        xscale=xscale,
        yscale=yscale,
        padding=padding)
    mark = axes.plot(
        a=a,
        b=b,
        along=along,
        color=color,
        stroke_width=stroke_width,
        opacity=opacity,
        title=title,
        marker=marker,
        size=size,
        mfill=mfill,
        mopacity=mopacity,
        mtitle=mtitle,
        style=style,
        mstyle=mstyle,
        mlstyle=mlstyle,
        filename=filename)
    return canvas, axes, mark


def scatterplot(
        a,
        b=None,
        along="x",
        color=None,
        marker="o",
        size=20,
        opacity=1.0,
        title=None,
        style=None,
        mstyle=None,
        mlstyle=None,
        filename=None,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
        show=True,
        xshow=True,
        yshow=True,
        label=None,
        xlabel=None,
        ylabel=None,
        xscale="linear",
        yscale="linear",
        padding=10,
        width=None,
        height=None,
        canvas_style=None):
    """Convenience function for creating a scatter plot in a single call.

    See :meth:`toyplot.axes.Cartesian.scatterplot`, :meth:`toyplot.canvas.Canvas.axes`, and :class:`toyplot.canvas.Canvas` for parameter descriptions.

    Returns
    -------
    canvas: :class:`toyplot.canvas.Canvas`
      A new canvas object.
    axes: :class:`toyplot.axes.Cartesian`
      A new set of 2D axes that fill the canvas.
    mark: :class:`toyplot.mark.Plot`
      The new scatter plot mark.
    """
    canvas = Canvas(width=width, height=height, style=canvas_style)
    axes = canvas.axes(
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        show=show,
        xshow=xshow,
        yshow=yshow,
        label=label,
        xlabel=xlabel,
        ylabel=ylabel,
        xscale=xscale,
        yscale=yscale,
        padding=padding)
    mark = axes.scatterplot(
        a=a,
        b=b,
        along=along,
        color=color,
        marker=marker,
        size=size,
        opacity=opacity,
        title=title,
        style=style,
        mstyle=mstyle,
        mlstyle=mlstyle,
        filename=filename)
    return canvas, axes, mark


def table(
        data=None,
        rows=None,
        columns=None,
        hrows=None,
        brows=None,
        lcols=None,
        rcols=None,
        label=None,
        width=None,
        height=None,
        canvas_style=None):
    """Convenience function to create a table visualization in a single call.

    See :meth:`toyplot.canvas.Canvas.table`, and :class:`toyplot.canvas.Canvas` for parameter descriptions.

    Returns
    -------
    canvas: :class:`toyplot.canvas.Canvas`
      A new canvas object.
    table: :class:`toyplot.axes.Table`
      A new set of table axes that fill the canvas.
    """
    canvas = Canvas(width=width, height=height, style=canvas_style)
    table = canvas.table(
        data=data,
        rows=rows,
        columns=columns,
        hrows=hrows,
        brows=brows,
        lcols=lcols,
        rcols=rcols,
        label=label)
    return canvas, table
