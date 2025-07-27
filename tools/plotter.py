import plotly.graph_objects as go
import plotly.express as px
import io
import base64
from typing import List, Optional, Union, Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("plotter")

@mcp.tool()
def plot_chart(
    x_values: List[Union[str, int, float]],
    y_values: List[Union[int, float]],
    chart_type: str = "line",
    title: str = "Chart",
    x_label: str = "X-axis",
    y_label: str = "Y-axis",
    color: str = "blue",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a chart using Plotly and return it as a base64-encoded PNG image.
    This is the main plotting function that takes x and y values along with labels.
    
    :param x_values: List of x-axis values (strings, integers, or floats).
    :param y_values: List of y-axis values (integers or floats).
    :param chart_type: Type of chart ('line', 'bar', 'scatter') - default: 'line'.
    :param title: Title of the chart.
    :param x_label: Label for the x-axis.
    :param y_label: Label for the y-axis.
    :param color: Color of the chart elements (default: blue).
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    fig = go.Figure()
    
    if chart_type.lower() == "line":
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines+markers',
            line=dict(color=color),
            marker=dict(color=color),
            name='Data'
        ))
    elif chart_type.lower() == "bar":
        fig.add_trace(go.Bar(
            x=x_values,
            y=y_values,
            marker_color=color,
            name='Data'
        ))
    elif chart_type.lower() == "scatter":
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='markers',
            marker=dict(color=color, size=8),
            name='Data'
        ))
    else:
        raise ValueError("chart_type must be 'line', 'bar', or 'scatter'")
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_line_chart(
    x_values: List[Union[str, int, float]],
    y_values: List[Union[int, float]],
    title: str = "Line Chart",
    x_label: str = "X-axis",
    y_label: str = "Y-axis",
    line_color: str = "blue",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a line chart using Plotly and return it as a base64-encoded PNG image.
    
    :param x_values: List of x-axis values (strings, integers, or floats).
    :param y_values: List of y-axis values (integers or floats).
    :param title: Title of the chart.
    :param x_label: Label for the x-axis.
    :param y_label: Label for the y-axis.
    :param line_color: Color of the line (default: blue).
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        line=dict(color=line_color),
        name='Data'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_bar_chart(
    x_values: List[Union[str, int, float]],
    y_values: List[Union[int, float]],
    title: str = "Bar Chart",
    x_label: str = "X-axis",
    y_label: str = "Y-axis",
    bar_color: str = "blue",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a bar chart using Plotly and return it as a base64-encoded PNG image.
    
    :param x_values: List of x-axis values (strings, integers, or floats).
    :param y_values: List of y-axis values (integers or floats).
    :param title: Title of the chart.
    :param x_label: Label for the x-axis.
    :param y_label: Label for the y-axis.
    :param bar_color: Color of the bars (default: blue).
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        marker_color=bar_color,
        name='Data'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_scatter_plot(
    x_values: List[Union[int, float]],
    y_values: List[Union[int, float]],
    title: str = "Scatter Plot",
    x_label: str = "X-axis",
    y_label: str = "Y-axis",
    marker_color: str = "blue",
    marker_size: int = 8,
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a scatter plot using Plotly and return it as a base64-encoded PNG image.
    
    :param x_values: List of x-axis values (integers or floats).
    :param y_values: List of y-axis values (integers or floats).
    :param title: Title of the chart.
    :param x_label: Label for the x-axis.
    :param y_label: Label for the y-axis.
    :param marker_color: Color of the markers (default: blue).
    :param marker_size: Size of the markers (default: 8).
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        marker=dict(color=marker_color, size=marker_size),
        name='Data'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_histogram(
    values: List[Union[int, float]],
    bins: int = 20,
    title: str = "Histogram",
    x_label: str = "Value",
    y_label: str = "Frequency",
    bar_color: str = "blue",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a histogram using Plotly and return it as a base64-encoded PNG image.
    
    :param values: List of values to create histogram from.
    :param bins: Number of bins for the histogram (default: 20).
    :param title: Title of the chart.
    :param x_label: Label for the x-axis.
    :param y_label: Label for the y-axis.
    :param bar_color: Color of the bars (default: blue).
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=values,
        nbinsx=bins,
        marker_color=bar_color,
        name='Data'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_pie_chart(
    labels: List[str],
    values: List[Union[int, float]],
    title: str = "Pie Chart",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a pie chart using Plotly and return it as a base64-encoded PNG image.
    
    :param labels: List of labels for each slice.
    :param values: List of values for each slice.
    :param title: Title of the chart.
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    if len(labels) != len(values):
        raise ValueError("labels and values must have the same length")
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        name="Data"
    ))
    
    fig.update_layout(
        title=title,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_multi_line_chart(
    x_values: List[Union[str, int, float]],
    y_series: Dict[str, List[Union[int, float]]],
    title: str = "Multi-Line Chart",
    x_label: str = "X-axis",
    y_label: str = "Y-axis",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a multi-line chart using Plotly and return it as a base64-encoded PNG image.
    
    :param x_values: List of x-axis values (strings, integers, or floats).
    :param y_series: Dictionary where keys are series names and values are lists of y-values.
    :param title: Title of the chart.
    :param x_label: Label for the x-axis.
    :param y_label: Label for the y-axis.
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    fig = go.Figure()
    
    for series_name, y_values in y_series.items():
        if len(x_values) != len(y_values):
            raise ValueError(f"x_values and y_values for series '{series_name}' must have the same length")
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines+markers',
            name=series_name
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_candlestick_chart(
    dates: List[str],
    open_prices: List[float],
    high_prices: List[float],
    low_prices: List[float],
    close_prices: List[float],
    title: str = "Candlestick Chart",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a candlestick chart using Plotly and return it as a base64-encoded PNG image.
    
    :param dates: List of date strings.
    :param open_prices: List of opening prices.
    :param high_prices: List of high prices.
    :param low_prices: List of low prices.
    :param close_prices: List of closing prices.
    :param title: Title of the chart.
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    if not all(len(dates) == len(prices) for prices in [open_prices, high_prices, low_prices, close_prices]):
        raise ValueError("All price lists must have the same length as dates")
    
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=dates,
        open=open_prices,
        high=high_prices,
        low=low_prices,
        close=close_prices,
        name="OHLC"
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        width=width,
        height=height,
        template="plotly_white",
        xaxis_rangeslider_visible=False
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_heatmap(
    z_values: List[List[Union[int, float]]],
    x_labels: Optional[List[str]] = None,
    y_labels: Optional[List[str]] = None,
    title: str = "Heatmap",
    colorscale: str = "Viridis",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a heatmap using Plotly and return it as a base64-encoded PNG image.
    
    :param z_values: 2D list of values for the heatmap.
    :param x_labels: Optional list of x-axis labels.
    :param y_labels: Optional list of y-axis labels.
    :param title: Title of the chart.
    :param colorscale: Color scale for the heatmap (default: Viridis).
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=z_values,
        x=x_labels,
        y=y_labels,
        colorscale=colorscale,
        name="Heatmap"
    ))
    
    fig.update_layout(
        title=title,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_box_plot(
    values: List[Union[int, float]],
    title: str = "Box Plot",
    y_label: str = "Values",
    box_color: str = "blue",
    width: int = 800,
    height: int = 600
) -> str:
    """
    Create a box plot using Plotly and return it as a base64-encoded PNG image.
    
    :param values: List of values for the box plot.
    :param title: Title of the chart.
    :param y_label: Label for the y-axis.
    :param box_color: Color of the box (default: blue).
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :return: Base64-encoded PNG image string.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=values,
        marker_color=box_color,
        name="Data"
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title=y_label,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64

@mcp.tool()
def create_custom_chart(
    x_values: List[Union[str, int, float]],
    y_values: List[Union[int, float]],
    chart_type: str = "line",
    title: str = "Custom Chart",
    x_label: str = "X-axis",
    y_label: str = "Y-axis",
    color: str = "blue",
    width: int = 800,
    height: int = 600,
    show_markers: bool = True,
    marker_size: int = 8
) -> str:
    """
    Create a customizable chart using Plotly and return it as a base64-encoded PNG image.
    
    :param x_values: List of x-axis values (strings, integers, or floats).
    :param y_values: List of y-axis values (integers or floats).
    :param chart_type: Type of chart ('line', 'bar', 'scatter').
    :param title: Title of the chart.
    :param x_label: Label for the x-axis.
    :param y_label: Label for the y-axis.
    :param color: Color of the chart elements.
    :param width: Width of the chart in pixels (default: 800).
    :param height: Height of the chart in pixels (default: 600).
    :param show_markers: Whether to show markers on line charts.
    :param marker_size: Size of markers.
    :return: Base64-encoded PNG image string.
    """
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    fig = go.Figure()
    
    if chart_type.lower() == "line":
        mode = 'lines+markers' if show_markers else 'lines'
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode=mode,
            line=dict(color=color),
            marker=dict(size=marker_size),
            name='Data'
        ))
    elif chart_type.lower() == "bar":
        fig.add_trace(go.Bar(
            x=x_values,
            y=y_values,
            marker_color=color,
            name='Data'
        ))
    elif chart_type.lower() == "scatter":
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='markers',
            marker=dict(color=color, size=marker_size),
            name='Data'
        ))
    else:
        raise ValueError("chart_type must be 'line', 'bar', or 'scatter'")
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=width,
        height=height,
        template="plotly_white"
    )
    
    # Convert to PNG image
    img_bytes = fig.to_image(format="png", width=width, height=height)
    
    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return img_base64
