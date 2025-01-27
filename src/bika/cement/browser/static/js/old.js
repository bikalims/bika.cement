console.log("TimeSeries:: loading");
class TimeSeries {
  constructor(svgElement) {
    // console.log("Constructor - svgElement:", svgElement);
    let columns = $(svgElement).attr('data-columns');
    let results = $(svgElement).attr('data-results');
    // console.log("Raw columns:", columns);
    // console.log("Raw results:", results);
    
    try {
      columns = JSON.parse(columns);
      results = JSON.parse(results);
    } catch (e) {
      console.error("JSON parsing error:", e);
    }
    
    // console.log("Parsed columns:", columns);
    // console.log("Parsed results:", results);
    
    this.svgRef = { current: svgElement };
    this.state = { results: results };
    this.props = {
      item: {
        time_series_columns: columns,
        time_series_graph_title: "Time Series Graph",
        time_series_graph_xaxis: "X-Axis",
        time_series_graph_yaxis: "Y-Axis"
      }
    };
  }

  getLineConfigs(count) {
    // console.log("Getting line configs for count:", count);
    const configs = [
      {color: "#666666", opacity: 1.0, symbol: d3.symbolCircle, dash: ""},
      {color: "#666666", opacity: 0.8, symbol: d3.symbolCircle, dash: ""},
      {color: "#666666", opacity: 0.6, symbol: d3.symbolCircle, dash: ""},
      {color: "#666666", opacity: 0.4, symbol: d3.symbolCircle, dash: ""},
      {color: "#666666", opacity: 0.2, symbol: d3.symbolCircle, dash: ""}
    ];
    return configs.slice(0, count);
  }

  toMatrix(data, headers) {
    // console.log("Converting to matrix. Data:", data, "Headers:", headers);
    if (!data || data.length === 0) {
      console.log("No data to convert");
      return "";
    }

    try {
      const matrix = data.map(innerList => {
        const obj = {};
        headers.forEach((header, index) => {
          obj[header] = index === 0 ? innerList[index] : parseFloat(innerList[index]);
        });
        return obj;
      });
      // console.log("Converted matrix:", matrix);
      return matrix;
    } catch (e) {
      console.error("Matrix conversion error:", e);
      return "";
    }
  }

  buildGraph() {
    console.log("TimeSeries::build_graph: entered");
    
    if (!this.svgRef?.current) {
      console.error("No SVG reference found");
      return;
    }

    const results = this.state.results;
    if (!results || results === "") {
      console.log("No results data");
      $(this.svgRef.current).empty();
      return;
    }

    // Get datasets
    const columns = this.props.item.time_series_columns;
    // console.log("Columns:", columns);
    
    if (!columns || !Array.isArray(columns)) {
      console.error("Invalid columns data");
      return;
    }

    const colTypes = columns.map(i => i.ColumnType);
    const headers = columns.map(i => i.ColumnTitle);
    // console.log("Column types:", colTypes);
    // console.log("Headers:", headers);
    
    const index = headers[0];
    const data = this.toMatrix(results, headers);
    // console.log("Processed data:", data);

    if (!data || data === "") {
      console.error("No valid data after matrix conversion");
      return;
    }

    // Generate the line colors (exclude index)
    const lineConfigs = this.getLineConfigs(headers.length - 1);
    if (colTypes[colTypes.length - 1] === "average") {
      lineConfigs[lineConfigs.length - 1] = {
        color: "#000000",
        dash: "",
        opacity: "1.0",
        symbol = d3.symbolCircle
      };
    }
    // console.log("Line configs:", lineConfigs);

    try {
      // Set up dimensions
      const margin = { top: 40, right: 80, bottom: 50, left: 80 };
      const width = 800 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;
      const totalHeight = height + 120;

      // console.log("Dimensions:", { margin, width, height, totalHeight });

      // Clear existing content
      d3.select(this.svgRef.current).selectAll("*").remove();

      if (!this.svgRef.current) {
        console.error("SVG container element is missing!");
        return;
      }

      // Create SVG container
      const svg = d3.select(this.svgRef.current)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", totalHeight)
        .style('fill', 'red')
        .style('padding', '20px')

      // Set up scales
      const xExtent = d3.extent(data, d => parseFloat(d[index]));
      const x = d3.scale.linear()
        .domain(xExtent)
        .range([0, width-10]);

      const yValues = data.flatMap(row => 
        headers.slice(1).map(header => row[header])
      );
      const minY = d3.min(yValues);
      const maxY = d3.max(yValues);
      const adjustedMinY = minY - (minY * 0.1);  // 10% below MinY

      // console.log("Y values:", { minY, maxY, adjustedMinY });

      const y = d3.scale.linear()
        .domain([Math.floor(adjustedMinY), Math.ceil(maxY)])
        .range([height, 0]);

      // Add title
      svg.append("text")
        .attr("class", "graph-title")
        .attr("x", width / 2)
        .attr("y", -margin.top / 2)
        .attr("text-anchor", "middle")
        .style("stroke", "black")
        .style("font-size", "16px")
        .style("font-weight", "bold")
        .text(this.props.item.time_series_graph_title);

      // Add X axis and label
      svg.append("g")
        .attr("class", "x axis")
        .attr("transform", `translate(0, ${height})`)
        .style('padding', '20px')
        .call(d3.svg.axis().scale(x).orient("bottom"))
        .attr("fill", "black")
        .style('padding', '20px');

      svg.append("text")
        .attr("x", width / 2)
        .attr("y", height + margin.bottom)
        .attr("text-anchor", "middle")
        .style("font-size", "12px")
        .style("fill", "black")
        .text(this.props.item.time_series_graph_xaxis);

      // Add Y axis and label
      svg.append("g")
        .attr("class", "y axis")
        .style('padding', '20px')
        .call(d3.svg.axis().scale(y).orient("left"));

      svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", -margin.left)
        .attr("text-anchor", "middle")
        .style("font-size", "12px")
        .text(this.props.item.time_series_graph_yaxis);

      // Add grid lines

      // Add horizontal grid lines
      svg.append("g")
        .attr("class", "grid horizontal")
        .attr("transform", "translate(0, 0)")
        .call(
          d3.svg.axis()
            .scale(y)
            .orient("left")
            .tickSize(-width)
            .tickFormat("")
        )
        .selectAll("line")
        .style("stroke", "black")
        .style("stroke-dasharray", "2,2")
        .style("opacity", 1)

      // // Add vertical grid lines
      // svg.append("g")
      //   .attr("class", "grid vertical")
      //   .attr("transform", `translate(0, ${height})`)
      //   .call(
      //     d3.svg.axis()
      //       .scale(x)
      //       .orient("bottom")
      //       .tickSize(-height)
      //       .tickFormat("")
      //   )
      //   .selectAll("line")
      //   .style("stroke-dasharray", "2,2")
      //   .style("opacity", 1)

      // Draw lines and points for each series
      headers.slice(1).forEach((key, i) => {
        // console.log(`Processing series ${key} (${i})`);
        
        const lineGenerator = d3.svg.line()
          .x(d => x(parseFloat(d[index])))
          .y(d => y(d[key]));

        // Add line
        const pathData = lineGenerator(data);
        // console.log(`Generated Line  ${pathData}`);
        svg.append("path")
          .attr("d", pathData)
          .attr("fill", "none")
          .attr("stroke", lineConfigs[i].color)
          .attr("stroke-width", 2)
          .attr("opacity", lineConfigs[i].opacity);

        // Add points
        svg.selectAll(`.point-${i}`)
          .data(data)
          .enter()
          .append("circle")
          .attr("class", `point-${i}`)
          .attr("cx", d => x(parseFloat(d[index])))
          .attr("cy", d => y(d[key]))
          .attr("r", lineConfigs[i].radius)
          .style("fill", lineConfigs[i].color)
          .style("opacity", lineConfigs[i].opacity);
      });

      // Add legend
      const legendItemWidth = 100;
      const legendItemsPerRow = Math.floor(width / legendItemWidth);
      
      const legend = svg.append("g")
        .attr("class", "legend")
        .attr("transform", `translate(50,${height + 50})`);

      const legendItems = legend.selectAll("g")
        .data(headers.slice(1))
        .enter()
        .append("g")
        .attr("transform", (d, i) => {
          const row = Math.floor(i / legendItemsPerRow);
          const col = i % legendItemsPerRow;
          return `translate(${col * legendItemWidth},${row * 20})`;
        });

      legendItems.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", (d, i) => lineConfigs[i].color)
        .style("opacity", (d, i) => lineConfigs[i].opacity);

      legendItems.append("text")
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("font-size", "12px")
        .style("fill", (d, i) => lineConfigs[i].color)
        .text(d => d);

      console.log("Graph build completed successfully");

    } catch (error) {
      console.error("Error building graph:", error);
    }
  }
}
console.log("TimeSeries:: loaded");
