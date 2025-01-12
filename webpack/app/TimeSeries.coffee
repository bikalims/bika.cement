import * as d3 from "d3"
import { Canvg } from 'canvg';

class TimeSeries 

  ###*
   * TimeSeries Field for the Listing Table
   *
   * A multi value field is identified by the column type "timeseries" in the
   * listing view, e.g.  `self.columns = {"Result": {"type": "timeseries"}, ... }`
   *
  ###
  constructor: (element) ->
  
    @container = element;
    # remember the initial value
    this.state =
      value: element.state.value

    this.props = element.props

    console.log('constructor complete')

  ###
   * Converts the string value to an array
  ###
  to_matrix: (listString, headers) ->
    # No values yet
    if listString == ""
      return ""

    # Parse the string version of the list of lists into an array
    # list = JSON.parse(listString)
    list = listString

    # Map each inner list to an object using the headers
    matrix = list.map (innerList) ->
        obj = {}
        headers.forEach (header, index) ->
            obj[header] = innerList[index]
        obj

    matrix.map (row) ->
        headers.forEach (header, index) ->
            if index = 0
              row[header] = row[header]
            else
              row[header] = parseFloat(row[header])
    matrix


  getLineConfigs = (count) ->
    configs = [
      {color: "#666666", opacity: 1.0, symbol: d3.symbolCircle, dash: ""}
      {color: "#666666", opacity: 0.8, symbol: d3.symbolCircle, dash: ""}
      {color: "#666666", opacity: 0.6, symbol: d3.symbolCircle, dash: ""}
      {color: "#666666", opacity: 0.4, symbol: d3.symbolCircle, dash: ""}
      {color: "#666666", opacity: 0.2, symbol: d3.symbolCircle, dash: ""}
    ]
    configs.slice(0, count)

  # Create symbol generator
  symbolGenerator = d3.symbol().size(24)  # Adjust size as needed

  ###
   * Inputs table builder. Generates a table of  inputs as matrix
  ###
  build_graph: ->
    console.log "TimeSeries::build_graph: entered"

    values = this.state.value

    if values == ""
      console.log "TimeSeries::build_graph: exit because no data"
      @container.current.appendChild([])
      return

    # Get datasets
    columns = this.props.item.time_series_columns
    col_types = columns.map (i) -> i.ColumnType
    headers = columns.map (i) -> i.ColumnTitle
    index = headers[0]
    data = @to_matrix(values, headers)

    # Generate the line colors (exclude index)
    line_configs = getLineConfigs(headers.length - 1)
    if col_types[col_types.length - 1] == "average"
      line_configs[line_configs.length - 1] = {
        color: "#000000",
        dash: "",
        opacity: "1.0",
        symbol: d3.symbolCircle
      }
    console.debug(line_configs)

    # Set up dimensions
    margin = {top: 40, right: 80, bottom: 50, left: 60}
    width = 700 - margin.left - margin.right
    height = 400 - margin.top - margin.bottom + 50

    # Set up scales
    x = d3.scaleLinear()
      .domain(d3.extent(data, (d) -> parseFloat(d[index])))
      .range([0, width])

    # Set up Y scale with trimmed domain
    minY = d3.min(data.flatMap((row) -> headers.slice(1).map((header) -> parseFloat(row[header]))))
    minY = minY- (minY * 0.1)
    maxY = d3.max(data.flatMap((row) -> headers.slice(1).map((header) -> parseFloat(row[header]))))
    # maxY = maxY + (maxY * 0.1)

    y = d3.scaleLinear()
      .domain([Math.floor(minY), Math.ceil(maxY)])  # Trim domain to just cover data range
      .range([height, 0])

    # Create SVG container
    svg = d3.select(@container)
      .append('svg')
      .style("height", "#{height+120}px")

    # Remove any previous SVG content
    svg.selectAll('*').remove()

    svg = svg
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr('xmlns', 'http://www.w3.org/2000/svg')
      .append("g")
      .attr("transform", "translate(#{margin.left},#{margin.top})")

    # Graph title
    svg.append("text")
      .attr("x", width / 2)
      .attr("y", -margin.top / 2)
      .attr("text-anchor", "middle")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .text(this.props.item.time_series_graph_title)

    # X-axis
    svg.append("g")
      .attr("transform", "translate(0,#{height})")
      .call(d3.axisBottom(x))

    # X-axis label
    svg.append("text")
      .attr("x", width / 2)
      .attr("y", height + margin.bottom - 10)
      .attr("text-anchor", "middle")
      .style("font-size", "12px")
      .text(this.props.item.time_series_graph_xaxis)

    # Y-axis
    svg.append("g")
      .call(d3.axisLeft(y))

    # Y-axis label
    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2)
      .attr("y", -margin.left + 15)
      .attr("text-anchor", "middle")
      .style("font-size", "12px")
      .text(this.props.item.time_series_graph_yaxis)

    # Add horizontal grid lines
    svg.append("g")
      .attr("class", "grid horizontal")
      .attr("transform", "translate(0, 0)")
      .call(
        d3.axisLeft(y)
          .tickSize(-width)  # Extend ticks across the chart width
          .tickFormat("")    # Remove tick labels
      )
      .selectAll("line")
      .style("stroke", "#999")  # Lighter gray
      # .style("stroke-dasharray", "2,2")
      .style("opacity", 0.8)       # Adjust transparency

    # Add vertical grid lines
    svg.append("g")
      .attr("class", "grid vertical")
      .attr("transform", "translate(0, #{height})")
      .call(
        d3.axisBottom(x)
          .tickSize(-height)  # Extend ticks across the chart height
          .tickFormat("")     # Remove tick labels
      )
      .selectAll("line")
      .style("stroke", "#999")  # Lighter gray
      .style("stroke-dasharray", "2,2")
      .style("opacity", 0.8)       # Adjust transparency

    # Draw axes
    svg.append("g")
      .attr("transform", "translate(0,#{height})")
      .call(d3.axisBottom(x))

    svg.append("g")
      .call(d3.axisLeft(y))

    headers.slice(1).forEach((key, i) ->
      console.debug("Main loop: " + key + "  " + i)

      # Filter data to exclude rows with null, undefined, or non-numeric values for the current key
      validData = data.filter((d) ->
        d[key]? and not isNaN(d[key]) # Ensure value exists and is numeric
      )

      # Line generator
      lineGen = d3.line()
        .x((d) ->
          x(d[index])
        )
        .y((d) ->
          y(d[key])
        )

      svg.append("path")
        .datum(validData) # Use filtered data
        .attr("fill", "none")
        .attr("stroke-width", 2)
        .attr("stroke", line_configs[i].color)
        .attr("opacity", line_configs[i].opacity)
        .attr("stroke-dasharray", line_configs[i].dash)
        .attr("d", lineGen)

      # Add data points with different symbols
      svg.selectAll(".symbol-#{i}")
        .data(validData) # Use filtered data
        .enter().append("path")
        .attr("class", "symbol symbol-#{i}")
        .attr("d", symbolGenerator.type(line_configs[i].symbol))
        .attr("transform", (d) ->
          # Ensure valid x and y before applying transform
          xVal = parseFloat(d[index])
          yVal = parseFloat(d[key])
          if not isNaN(xVal) and not isNaN(yVal)
            "translate(#{x(xVal)}, #{y(yVal)})"
          else
            null # Skip invalid points
        )
        .style("fill", line_configs[i].color)
        .style("opacity", line_configs[i].opacity)
    )

    # Add legend
    legend = svg.append("g")
      .attr("class", "legend")
      .attr("transform", "translate(50, #{height + 50})")  # Move legend below the graph

    # Add legend items
    legendItems = legend.selectAll("g")
      .data(headers.slice(1))
      .enter().append("g")
      .attr("transform", (d, i) ->
        xOffset = parseFloat((i % Math.floor(width / 100)) * 100)  # Horizontal spacing
        yOffset = parseFloat(Math.floor(i / Math.floor(width / 100)) * 20)  # Vertical spacing
        "translate(#{xOffset}, #{yOffset})"
      )


    # Add legend color squares
    legendItems.append("rect")
      .attr("x", 0)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", (d, i) -> line_configs[i].color)
      .style("opacity", (d, i) -> line_configs[i].opacity)

    # Add legend text
    legendItems.append("text")
      .attr("x", 24)
      .attr("y", 9)
      .attr("dy", "0.35em")
      .style("font-size", "12px")
      .text((d) -> d)

    console.log "TimeSeries::build_graph: svg done"

window.TimeSeries = TimeSeries
