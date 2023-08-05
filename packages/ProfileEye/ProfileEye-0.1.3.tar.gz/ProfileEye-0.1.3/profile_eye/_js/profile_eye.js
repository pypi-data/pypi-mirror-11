var profileEye = function(selection, fontSize) {

    console.log(fontSize);

    var nodes = selection.datum()["nodes"],
        links = selection.datum()["links"];

    var width = parseInt(selection.style("width")),
        height = parseInt(selection.style("height")),
        maxWidth = width / 5;

    var fisheyeScaler = function() {
        var fishOn = false,
            distortion = 1;

        var xFishScale = d3
            .fisheye
            .scale(d3.scale.linear)
            .domain([0, width])
            .range([0, width])
            .focus(width / 2); 
        var xNoFishScale = d3
            .scale
            .linear()
            .domain([0, width])
            .range([0, width]);
        var yFishScale = d3
            .fisheye
            .scale(d3.scale.linear)
            .domain([0, height])
            .range([0, height])
            .focus(height / 2); 
        var yNoFishScale = d3
            .scale
            .linear()
            .domain([0, height])
            .range([0, height]);

        var updateMouse = function(x, y) {
            xFishScale
                .distortion(distortion)
                .focus(x); 
            yFishScale
                .distortion(distortion)
                .focus(y); 
        }

        var on = function(on_) { 
            if (arguments.length == 0)
                return fishOn; 
            fishOn = on_; 
        };

        var getXScale = function() {
            return fishOn? xFishScale: xNoFishScale;
        }
        var getYScale = function() {
            return fishOn? yFishScale: yNoFishScale;
        }

        return {
            "getXScale": getXScale,
            "getYScale": getYScale,
            "on": on,
            "updateMouse": updateMouse,
        };
    }
    theScaler = fisheyeScaler();

    var theLayout;

    var callsColorer = function() {
        var maxCalls = d3.max(
            nodes,
            function(node) {
                return node.dummy? 0: node.times_called;
            });
        var hScale = d3
            .scale
            .linear()
            .domain([0, maxCalls])
            .range([250, 0]);

        var color = function(calls) {
            return d3.hsl(hScale(calls), 1, 0.5)
        } 

        return {
            "getColor": color
        };
    }
    var theCallsColorer = callsColorer();

    var baseItemHeight = 20;

    var svg = selection
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    var buildNodesAndEdges = function() {
        var getTextWidth = function(text) {
            var canvas = document.createElement("canvas");
            var context = canvas.getContext("2d");
            var metrics = context.measureText(text);
            return 1.6 * metrics.width;
        };

        var maxTextWidth = d3
            .max(nodes, function(node) { return getTextWidth(node.label); });

        var widthScale = d3
            .scale
            .linear()
            .domain([0, 100])
            .range([0, maxWidth]);

        var maxX = d3
            .max(nodes, function(node) {
                return node.dummy? 0: node.x;
            });
        var xScale = d3
            .scale
            .linear()
            .domain([0, maxX])
            .range([maxTextWidth / 2, width - maxTextWidth / 2]);

        var maxY = d3
            .max(nodes, function(node) {
                return node.dummy? 0: node.y;
            });
        var yScale = d3
            .scale
            .linear()
            .domain([0, maxY])
            .range([height - baseItemHeight, baseItemHeight]);

        nodes
            .forEach(function(node) {
                node.x = xScale(node.x);
                node.y = yScale(node.y);
                node.fixed = true;
                node.textWidth = getTextWidth(node.label);
                node.internalWidth = widthScale(node.internal);
                node.totalWidth = widthScale(node.total);
            });

        var link = svg
            .selectAll("path")
            .data(links)
            .enter()
            .append("path")
            .classed("link", true)
            .classed("backlink", function(e) {
                return e.back;
            })
            .attr("stroke", function(d) { 
                return theCallsColorer.getColor(d.times_called); 
            })

        var minOutgoingFrac = d3
            .min(
                links, 
                function(l) {
                    return l.outgoingFrac;
                });
        var maxOutgoingFrac = d3
            .max(
                links, 
                function(l) {
                    return l.outgoingFrac;
                });
        var linkOpacityScale = d3
            .scale
            .linear()
            .domain([minOutgoingFrac, maxOutgoingFrac])
            .range([0.3, 1]);
        link
            .attr("stroke-opacity", function(e) {
                e.normalOpacity = linkOpacityScale(e.outgoingFrac);
                e.nonselectedOpacity = 0.1;
                return e.normalOpacity;
            });

        links
            .forEach(function(edge) {
                edge.points = edge
                    .points
                    .map(function(p) {
                        return [xScale(p[0]), yScale(p[1])];
                    });
            });

        var node = svg
            .selectAll(".node")
            .data(nodes)
            .enter()
            .append("g")
            .attr("class", "node");

        return {
            "node": node,
            "link": link,
        }
    }
    var nodeLinks = buildNodesAndEdges();
    var node = nodeLinks["node"],
        link = nodeLinks["link"];

    var tooltipManager = function() {   
        var tooltip = undefined;

        var createTooltipIfNeeded = function(d) {
            if (tooltip === undefined) {
                var html = "";
                if (d.file != "" || d.line != -1)
                    html = "<p>" + d.file + ":" + String(d.line) + "</p>";
                html +=
                    '<p>' + String(d.times_called) + (d.times_called == 1? ' call': ' calls') + '</p>' +
                    '<p>' + String(d.internal) + '% of internal time</p>' +
                    '<p>' + String(d.total) + '% of total time</p>';
                tooltip = selection
                    .append("div")
                    .classed("tooltip", true)
                    .style("position", "absolute")
                    .style("z-index", "10")
                    .style("visibility", "hidden")
                    .html(html);

                tooltip
                    .style("visibility", "visible");
            }
            return tooltip;
        }    

        var moveTooltip = function(that) {
            return tooltip.style("top", (d3.mouse(that)[1]-10)+"px").style("left",(d3.mouse(that)[0]+10)+"px");
        }

        var removeTooltipIfNeeded = function() {
            d3.selectAll(".tooltip")
                .remove();
            tooltip = undefined;
        }

        return {
            "createTooltipIfNeeded": createTooltipIfNeeded,
            "moveTooltip": moveTooltip,
            "removeTooltipIfNeeded": removeTooltipIfNeeded,
        };
    }
    var theTooltipManager = tooltipManager();

    var radius = width / 20;
    var makeAngleScales = function() {
        var internalAngleScale = d3
            .scale
            .linear()
            .domain([0, 100])
            .range([0, 2 * Math.PI]);

        var sumTotal = 0;
        nodes
            .forEach(function(node) {
                if (!node.dummy)
                    sumTotal += node.total;
            });
        var totalAngleScale = d3
            .scale
            .linear()
            .domain([0, sumTotal])
            .range([0, 2 * Math.PI]);

        return {
            "internalAngleScale": internalAngleScale,
            "totalAngleScale": totalAngleScale,
        };
    }
    var angleScales = makeAngleScales();
    var internalAngleScale = angleScales.internalAngleScale;
    var totalAngleScale = angleScales.totalAngleScale;
    var makeCoverages = function() {
        var nonDummyNodes = nodes
            .filter(function(node) {
                return !node.dummy;
            });

        var internalCoverageSvg = svg
            .append("g")
            .attr("transform", "translate(" + (width / 3) + "," + height / 3.5 + ")");
        var internalCoverage = internalCoverageSvg
            .selectAll(".internalCoveragePaths")
            .data(nonDummyNodes)
            .enter()
            .append("svg:path")
            .attr("fill", function(d) { 
                return theCallsColorer.getColor(d.times_called); 
            })
            .on("click", function(d) {
                theLayout.onClicked(d);
            });
        var internalCoverageSelection = internalCoverageSvg
            .selectAll(".internalCoveragePathsSelection")
            .data(nonDummyNodes)
            .enter()
            .append("svg:path") 
            .classed("selection", true);
        var totalCoverageSvg = svg
            .append("g")
            .attr("transform", "translate(" + (width / 3) + "," + 2.5 * height / 3.5 + ")");
        var totalCoverage = totalCoverageSvg
            .selectAll(".totalCoveragePaths")
            .data(nonDummyNodes)
            .enter()
            .append("svg:path")
            .attr("fill", "white")
            .attr("stroke", function(d) { 
                return theCallsColorer.getColor(d.times_called); 
            })
            .on("click", function(d) {
                theLayout.onClicked(d);
            });
        var totalCoverageSelection = totalCoverageSvg
            .selectAll(".totalCoveragePathsSelection")
            .data(nonDummyNodes)
            .enter()
            .append("svg:path")
            .classed("selection", true);

        return {    
            "internalCoverage": internalCoverage,
            "internalCoverageSelection": internalCoverageSelection,
            "totalCoverage": totalCoverage,
            "totalCoverageSelection": totalCoverageSelection,
        }    
    }
    var coverages = makeCoverages();
    var internalCoverage = coverages.internalCoverage;
    var internalCoverageSelection = coverages.internalCoverageSelection;
    var totalCoverage = coverages.totalCoverage;
    var totalCoverageSelection = coverages.totalCoverageSelection;

    totalRect = node
        .filter(function(d) {
            return !d.dummy;
        })
        .append("rect")
        .attr("class", "node")
        .attr("width", function(d) {
            return d.totalWidth;
        })
        .style("fill", "white")
        .style("stroke", function(d) {
            return theCallsColorer.getColor(d.times_called);   
        })
        .style("stroke-width", 1)
        .classed("fixed", true)
        .on("mouseover", function(d) {
            theLayout.onMouseover(d);
            return theTooltipManager.createTooltipIfNeeded(d); 
        })
        .on("mousemove", function() {
            return theTooltipManager.moveTooltip(this);
        })
        .on("mouseout", function(d) {
            theLayout.onMouseout(d);
            theTooltipManager.removeTooltipIfNeeded();
        });

    var internalRect = node
        .filter(function(d) {
            return !d.dummy;
        })
        .append("rect")
        .attr("class", "node")
        .attr("width", function(d) {
            return d.internalWidth;
        })
        .style("stroke", "grey")
        .style("stroke-width", 1)
        .style("fill", function(d) {
            return theCallsColorer.getColor(d.times_called);   
        })
        .classed("fixed", true)
        .on("mouseover", function(d) {
            theLayout.onMouseover(d);
            return theTooltipManager.createTooltipIfNeeded(d); 
        })
        .on("mousemove", function() {
            return theTooltipManager.moveTooltip(this);
        })
        .on("mouseout", function(d) {
            theLayout.onMouseout(d);
            theTooltipManager.removeTooltipIfNeeded();
        });

    var label = node
        .filter(function(d) {
            return !d.dummy;
        })
        .append("text")
        .attr("dx", function(d) {
            return - d.textWidth / 2; })
        .attr("dy", 0)
        .style("fill", "black")
        .style("pointer-events", "none")
        .attr("dominant-baseline", "central")
        .text(function(d) {
            return d.label;
        });

    if (fontSize !== undefined)
        label
            .attr("font-size", "0.8em");

    var makeBrush = function() {
        var brushMove = function() {
            var before = brush.extent()[0],
                after = brush.extent()[1];
            var startI = Math.ceil(before / baseItemHeight),
                endI = Math.ceil(after / baseItemHeight);

            theLayout.onSelChanged(startI, endI);
        }

        var brushEnd = function() {
            var before = brush.extent()[0],
                after = brush.extent()[1];
            var startI = Math.ceil(before / baseItemHeight),
                endI = Math.ceil(after / baseItemHeight);

            svg.select(".brush").call(brush.extent(
                [baseItemHeight * startI, baseItemHeight * endI]));
        }

        var brush = d3
            .svg
            .brush()
            .y(theScaler.getYScale())
            .on("brush", brushMove)
            .on("brushend", brushEnd);

        var context = svg
            .append("g")
            .attr("transform", "translate(" + maxWidth / 2 + ", " + baseItemHeight / 2 + ")")
            .attr("class", "context");

        context.append("g")
            .classed("brush", true)
            .call(brush)
            .selectAll("rect")
            .attr("x", 0)
            .attr("width", maxWidth / 2 + 0.1 * radius);

        return brush;
    }
    var theBrush = makeBrush()

    var transitionTime = 250;
    var callsLayout = function() {
        var edgesStraight_ = false;

        var getPath = function(e) {
            if (edgesStraight_) {
                if (!e.back)
                    return "M" + theScaler.getXScale()(nodes[e.source].x) + "," + 
                        theScaler.getYScale()(nodes[e.source].y) + "L" + 
                        theScaler.getXScale()(nodes[e.target].x) + "," + 
                        theScaler.getYScale()(nodes[e.target].y);

                var dx = theScaler.getXScale()(nodes[e.target].x) - theScaler.getXScale()(nodes[e.source].x),
                    dy = theScaler.getYScale()(nodes[e.target].y) - theScaler.getYScale()(nodes[e.source].y),
                    dr = Math.sqrt(dx * dx + dy * dy);
                return "M" + theScaler.getXScale()(nodes[e.source].x) + "," + 
                    theScaler.getYScale()(nodes[e.source].y) + "A" + dr + "," + dr + " 0 0,1 " + 
                    theScaler.getXScale()(nodes[e.target].x) + "," + 
                    theScaler.getYScale()(nodes[e.target].y);
            }
     
            var line = d3
                .svg
                .line()
                .x(function(d) { 
                    return theScaler.getXScale()(d[0]);
                }) 
                .y(function(d) { 
                    return theScaler.getYScale()(d[1]);
                })
                .interpolate("basis");

            var source = [
                nodes[e.source].x,
                nodes[e.source].y
            ];
            var target = [
                nodes[e.target].x,
                nodes[e.target].y
            ];
            var points = 
                [source].concat(e.points).concat([target]);
            return line(points);
        }

        var update = function(transition) {
            if (transition) {
                link
                    .transition()   
                    .delay(transitionTime) 
                    .duration(transitionTime)
                    .style("opacity", "1")
                    .attr("d", function(e) {
                        return getPath(e);
                    });
            }
            else
                link
                    .attr("d", function(e) {
                        return getPath(e);
                    });

            totalRect
                .transition()   
                .duration(transition? transitionTime: 0)
                .attr("x", function(d) { 
                    return theScaler.getXScale()(d.x) - d.totalWidth / 2; 
                })
                .attr("y", function(d) { 
                    return theScaler.getYScale()(d.y - baseItemHeight / 2); 
                })
                .attr("height", function(d) {
                    var yStart = d.y - baseItemHeight / 2;
                    var yEnd = yStart + baseItemHeight;
                    return theScaler.getYScale()(yEnd) - theScaler.getYScale()(yStart);
                });

            internalRect
                .transition()   
                .duration(transition? transitionTime: 0)
                .attr("x", function(d) { 
                    return theScaler.getXScale()(d.x) - d.internalWidth / 2; 
                })
                .attr("y", function(d) { 
                    return theScaler.getYScale()(d.y - baseItemHeight / 2); 
                })
                .attr("height", function(d) {
                    var yStart = d.y - baseItemHeight / 2;
                    var yEnd = yStart + baseItemHeight;
                    return theScaler.getYScale()(yEnd) - theScaler.getYScale()(yStart);
                });

            label
                .transition()   
                .duration(transition? transitionTime: 0)
                .attr("x", function(d) { 
                    return theScaler.getXScale()(d.x); 
                })
                .attr("y", function(d) { 
                    return theScaler.getYScale()(d.y); 
                });

            var arc = d3
                .svg
                .arc()
                .innerRadius(0)
                .outerRadius(0)
                .startAngle(function(d) {
                    return 0;
                })
                .endAngle(function(d) {
                    return 0;
                });
            internalCoverage
                .attr("d", arc);
            internalCoverageSelection
                .attr("d", arc);
            totalCoverage
                .attr("d", arc);
            totalCoverageSelection
                .attr("d", arc);

            d3
                .selectAll(".brush")
                .style("pointer-events", "none")
                .style("opacity", 0);
        } 

        var onMouseover = function(d) {
            var nonOpaques = {};
            nonOpaques[d.name] = true;

            link
                .transition()
                .duration(transitionTime)
                .attr("stroke-opacity", function(e) {
                    if (e.source != d.name && e.target != d.name)
                        return e.nonselectedOpacity;
                    nonOpaques[e.source] = nonOpaques[e.target] = true;
                    return e.normalOpacity;
                });

            node
                .transition()
                .duration(transitionTime)
                .attr("opacity", function(d) {
                    return nonOpaques[d.name] === undefined? 0.1: 1;
                });
        }

        var onMouseout = function(d) {
            link
                .transition()
                .duration(transitionTime)
                .attr("stroke-opacity", function(e) {
                    return e.normalOpacity;
                });

            node
                .transition()
                .duration(transitionTime)
                .attr("opacity", 1);
        }

        var edgesStraight = function(on) {
            if (arguments.length == 0)
                return edgesStraight_;
            edgesStraight_ = on;
            update(true);
            return this;
        }

        return {
            "update": update,
            "onMouseover": onMouseover,
            "onMouseout": onMouseout,
            "edgesStraight": edgesStraight,
        };
    }
    var timesLayout = function(total) {
        var nonDummyNodes = nodes
            .filter(function(node) {
                return !node.dummy;
            });
        var startI = 0,
            endI = Math.min(5, nonDummyNodes.length);

        var update = function(transition) {
            if (!transition)
                return;

            link
                .transition()   
                .duration(transitionTime)
                .style("opacity", "0");
            totalRect
                .transition()   
                .delay(transitionTime)    
                .duration(transitionTime)
                .attr("x", theScaler.getXScale()(0)) 
                .attr("y", function(d) {
                    return theScaler.getYScale()(
                        baseItemHeight / 2 + baseItemHeight * (total? d.byTotalInd: d.byInternalInd));
                })
                .attr("height", function(d) {
                    var yStart = baseItemHeight / 2 + 
                        baseItemHeight * (total? d.byTotalInd: d.byInternalInd);
                    var yEnd = yStart + baseItemHeight;
                    return theScaler.getYScale()(yEnd) - theScaler.getYScale()(yStart);
                });
            internalRect
                .transition()   
                .delay(transitionTime)    
                .duration(transitionTime)
                .attr("x", theScaler.getXScale()(0)) 
                .attr("y", function(d) {
                    return theScaler.getYScale()(
                        baseItemHeight / 2 + baseItemHeight * (total? d.byTotalInd: d.byInternalInd));
                })
                .attr("height", function(d) {
                    var yStart = baseItemHeight / 2 + 
                        baseItemHeight * (total? d.byTotalInd: d.byInternalInd);
                    var yEnd = yStart + baseItemHeight;
                    return theScaler.getYScale()(yEnd) - theScaler.getYScale()(yStart);
                });
            label
                .transition()   
                .delay(transitionTime)    
                .duration(transitionTime)
                .attr("x", function(d) {
                    return d.textWidth / 2;
                })
                .attr("y", function(d) {
                    return theScaler.getYScale()(
                        baseItemHeight + baseItemHeight * (total? d.byTotalInd: d.byInternalInd));
                })
                .attr("dominant-baseline", "central");
            var internalArc = d3
                .svg
                .arc()
                .innerRadius(0)
                .outerRadius(radius)
                .startAngle(function(d) {
                    return internalAngleScale(total? d.internalStartByTotalInd: d.internalStartByInternalInd);
                })
                .endAngle(function(d) {
                    return internalAngleScale(d.internal + 
                        (total? d.internalStartByTotalInd: d.internalStartByInternalInd));
                });
            internalCoverage
                .transition()   
                .delay(2 * transitionTime)    
                .duration(transitionTime)
                .attr("d", internalArc);
            var internalArcSelection = d3
                .svg
                .arc()
                .innerRadius(radius)
                .outerRadius(1.1 * radius)
                .startAngle(function(d) {
                    return internalAngleScale(total? d.internalStartByTotalInd: d.internalStartByInternalInd);
                })
                .endAngle(function(d) {
                    return internalAngleScale(d.internal + 
                        (total? d.internalStartByTotalInd: d.internalStartByInternalInd));
                });
            internalCoverageSelection
                .transition()   
                .delay(2 * transitionTime)    
                .duration(transitionTime)
                .attr("d", internalArcSelection);
            var totalArc = d3
                .svg
                .arc()
                .innerRadius(0)
                .outerRadius(radius)
                .startAngle(function(d) {
                    return totalAngleScale(total? d.totalStartByTotalInd: d.totalStartByInternalInd);
                })
                .endAngle(function(d) {
                    return totalAngleScale(d.total +
                        (total? d.totalStartByTotalInd: d.totalStartByInternalInd));
                });
            totalCoverage
                .transition()   
                .delay(2 * transitionTime)    
                .duration(transitionTime)
                .attr("d", totalArc);
            var totalArcSelection = d3
                .svg
                .arc()
                .innerRadius(radius)
                .outerRadius(1.1 * radius)
                .startAngle(function(d) {
                    return totalAngleScale(total? d.totalStartByTotalInd: d.totalStartByInternalInd);
                })
                .endAngle(function(d) {
                    return totalAngleScale(d.total +
                        (total? d.totalStartByTotalInd: d.totalStartByInternalInd));
                });
            totalCoverageSelection
                .transition()   
                .delay(2 * transitionTime)    
                .duration(transitionTime)
                .attr("d", totalArcSelection);
            var brush = d3
                .selectAll(".brush");
            brush
                .transition()   
                .delay(2 * transitionTime)    
                .duration(transitionTime)
                .style("pointer-events", "all")
                .style("opacity", 0.4);

            svg
                .transition()   
                .delay(2 * transitionTime)
                .each("end", function() {
                    theLayout.onSelChanged(startI, endI);
                });
        }   

        var onClicked = function(node) {
            var i = total? node.byTotalInd: node.byInternalInd;
            onSelChanged(i, i +  1);
        }

        var onSelChanged = function(startI_, endI_) {
            startI = startI_;
            endI = endI_;

            svg.select(".brush").call(theBrush.extent(
                [baseItemHeight * startI, baseItemHeight * endI]));

            internalCoverageSelection
                .classed("disabledSelection", function(node) {
                    if (total)  
                        return startI > node.byTotalInd || endI <= node.byTotalInd;
                    return startI > node.byInternalInd || endI <= node.byInternalInd;
                })
                .classed("selection", function(node) {
                    if (total)  
                        return !(startI > node.byTotalInd || endI <= node.byTotalInd);
                    return !(startI > node.byInternalInd || endI <= node.byInternalInd);
                });

            totalCoverageSelection
                .classed("disabledSelection", function(node) {
                    if (total)  
                        return startI > node.byTotalInd || endI <= node.byTotalInd;
                    return startI > node.byInternalInd || endI <= node.byInternalInd;
                })
                .classed("selection", function(node) {
                    if (total)  
                        return !(startI > node.byTotalInd || endI <= node.byTotalInd);
                    return !(startI > node.byInternalInd || endI <= node.byInternalInd);
                });
        }

        var onMouseover = function(d) {
            // Do nothing. 
        }

        var onMouseout = function(d) {
            // Do nothing. 
        }

        return {
            "update": update,
            "onMouseover": onMouseover,
            "onMouseout": onMouseout,
            "onClicked": onClicked,
            "onSelChanged": onSelChanged,
        };
    }
    var theCallsLayout = callsLayout();
    var theTotalTimesSLayout = timesLayout(true);
    var theInternalTimesSLayout = timesLayout(false);
    theLayout = theCallsLayout;
    theLayout.update(true);

    svg.on("mousemove", function() {
        var mouse = d3.mouse(this);    
        theScaler.updateMouse(mouse[0], mouse[1])
        theLayout.update(false);
    });

    d3
        .select("#layoutTypeCalls")
        .property("checked", true)
        .on("change", function() {
            d3
                .select("#callsStuff")
                .style("visibility", "visible");
            theScaler.on(d3.select("#fisheye").property("checked"));

            theLayout = theCallsLayout;
            theLayout.update(true);
        });
    d3
        .select("#layoutTypeInternal")
        .on("change", function() {
            d3
                .select("#callsStuff")
                .style("visibility", "hidden");
            theScaler.on(false);

            theLayout = theInternalTimesSLayout;
            theLayout.update(true);
        });
    d3
        .select("#layoutTypeTotal")
        .on("change", function() {
            d3
                .select("#callsStuff")
                .style("visibility", "hidden");
            theScaler.on(false);

            theLayout = theTotalTimesSLayout;
            theLayout.update(true);
        });

    d3
        .select("#fisheye")
        .property("checked", theScaler.on())
        .on("change", function() {
            theScaler.on(!theScaler.on());
            theLayout.update(true);
        });

    d3
        .select("#edgesSplines")
        .property("checked", !theCallsLayout.edgesStraight())
        .on("change", function() {
            theLayout.edgesStraight(false);
        });
    d3
        .select("#edgesStraight")
        .property("checked", theCallsLayout.edgesStraight())
        .on("change", function() {
            theLayout.edgesStraight(true);
        });
}
