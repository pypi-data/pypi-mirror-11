function Gauge(placeholderName, configuration){
  /**class:Gauge(placeholderName, configuration)
    Creates a Gauge object
    
    :param str placeHolderName: The identifier of the placeholder to which the gauge will be attached
    :param object configuration: A configuration object
  */
  this.placeholderName = placeholderName;
  
  var self = this; // for internal d3 functions
  
  this.configure = function(configuration){
    /**function:configure(configuration)
      Applies the configuration passed in the constructor
       to the internal parameters

       :param object configuration: The configuration object passed in the constructor
    */
    this.config = configuration;
    
    this.config.size = this.config.size;// * 0.9;
    
    this.config.raduis = this.config.size * 0.97 / 2;
    this.config.cx = this.config.size / 2;
    this.config.cy = this.config.size / 2;
    
    
    this.config.min = undefined != configuration.min ? configuration.min : 0; 
    this.config.max = undefined != configuration.max ? configuration.max : 100; 
    this.config.range = this.config.max - this.config.min;
    
    this.config.majorTicks = configuration.majorTicks || 5;
    this.config.minorTicks = configuration.minorTicks || 2;
    
    this.config.greenColor  = configuration.greenColor || "#109618";
    this.config.yellowColor = configuration.yellowColor || "#FF9900";
    this.config.redColor  = configuration.redColor || "#DC3912";
    
    this.config.transitionDuration = configuration.transitionDuration || 500;
  }

  this.render = function(){
    /**function:render()
      Renders the gauge.
    */
    this.body = d3.select("#" + this.placeholderName)
              .append("svg:svg")
              .attr("class", "gauge")
              .attr("width", this.config.size)
              .attr("height", this.config.size);
    this.body.append("svg:circle")
          .attr("cx", this.config.cx)
          .attr("cy", this.config.cy)
          .attr("r", this.config.raduis)
          .style("fill", "#ccc")
          .style("stroke", "#000")
          .style("stroke-width", "0.5px");
          
    this.body.append("svg:circle")
          .attr("cx", this.config.cx)
          .attr("cy", this.config.cy)
          .attr("r", 0.9 * this.config.raduis)
          .style("fill", "#fff")
          .style("stroke", "#e0e0e0")
          .style("stroke-width", "2px");
          
    for (var index in this.config.greenZones)
    {
      this.drawBand(this.config.greenZones[index].from, this.config.greenZones[index].to, self.config.greenColor);
    }
    
    for (var index in this.config.yellowZones)
    {
      this.drawBand(this.config.yellowZones[index].from, this.config.yellowZones[index].to, self.config.yellowColor);
    }
    
    for (var index in this.config.redZones)
    {
      this.drawBand(this.config.redZones[index].from, this.config.redZones[index].to, self.config.redColor);
    }
    
    if (undefined != this.config.label)
    {
      var fontSize = Math.round(this.config.size / 9);
      this.body.append("svg:text")
            .attr("x", this.config.cx)
            .attr("y", this.config.cy / 2 + fontSize / 2)
            .attr("dy", fontSize / 2)
            .attr("text-anchor", "middle")
            .text(this.config.label)
            .style("font-size", fontSize + "px")
            .style("fill", "#333")
            .style("stroke-width", "0px");
    }
    
    var fontSize = Math.round(this.config.size / 16);
    var majorDelta = this.config.range / (this.config.majorTicks - 1);
    for (var major = this.config.min; major <= this.config.max; major += majorDelta)
    {
      var minorDelta = majorDelta / this.config.minorTicks;
      for (var minor = major + minorDelta; minor < Math.min(major + majorDelta, this.config.max); minor += minorDelta)
      {
        var point1 = this.valueToPoint(minor, 0.75);
        var point2 = this.valueToPoint(minor, 0.85);
        
        this.body.append("svg:line")
              .attr("x1", point1.x)
              .attr("y1", point1.y)
              .attr("x2", point2.x)
              .attr("y2", point2.y)
              .style("stroke", "#666")
              .style("stroke-width", "1px");
      }
      
      var point1 = this.valueToPoint(major, 0.7);
      var point2 = this.valueToPoint(major, 0.85);  
      
      this.body.append("svg:line")
            .attr("x1", point1.x)
            .attr("y1", point1.y)
            .attr("x2", point2.x)
            .attr("y2", point2.y)
            .style("stroke", "#333")
            .style("stroke-width", "2px");
      
      if (major == this.config.min || major == this.config.max)
      {
        var point = this.valueToPoint(major, 0.63);
        
        this.body.append("svg:text")
              .attr("x", point.x)
              .attr("y", point.y)
              .attr("dy", fontSize / 3)
              .attr("text-anchor", major == this.config.min ? "start" : "end")
              .text(major)
              .style("font-size", fontSize + "px")
              .style("fill", "#333")
              .style("stroke-width", "0px");
      }
    }
    
    var pointerContainer = this.body.append("svg:g").attr("class", "pointerContainer");
    
    var midValue = (this.config.min + this.config.max) / 2;
    
    var pointerPath = this.buildPointerPath(midValue);
    
    var pointerLine = d3.svg.line()
                  .x(function(d) { return d.x })
                  .y(function(d) { return d.y })
                  .interpolate("basis");
    
    pointerContainer.selectAll("path")
              .data([pointerPath])
              .enter()
                .append("svg:path")
                  .attr("d", pointerLine)
                  .style("fill", "#dc3912")
                  .style("stroke", "#c63310")
                  .style("fill-opacity", 0.7)
          
    pointerContainer.append("svg:circle")
              .attr("cx", this.config.cx)
              .attr("cy", this.config.cy)
              .attr("r", 0.12 * this.config.raduis)
              .style("fill", "#4684EE")
              .style("stroke", "#666")
              .style("opacity", 1);
    
    var fontSize = Math.round(this.config.size / 10);
    pointerContainer.selectAll("text")
              .data([midValue])
              .enter()
                .append("svg:text")
                  .attr("x", this.config.cx)
                  .attr("y", this.config.size - this.config.cy / 4 - fontSize)
                  .attr("dy", fontSize / 2)
                  .attr("text-anchor", "middle")
                  .style("font-size", fontSize + "px")
                  .style("fill", "#000")
                  .style("stroke-width", "0px");
    
    this.redraw(this.config.min, 0);
  }
  
  this.buildPointerPath = function(value){
    /**function:buildPointerPath(value)
      Builds the pointer path of the gauge

      :param numbers.Number value: The start point
    */
    var delta = this.config.range / 13;
    
    var head = valueToPoint(value, 0.85);
    var head1 = valueToPoint(value - delta, 0.12);
    var head2 = valueToPoint(value + delta, 0.12);
    
    var tailValue = value - (this.config.range * (1/(270/360)) / 2);
    var tail = valueToPoint(tailValue, 0.28);
    var tail1 = valueToPoint(tailValue - delta, 0.12);
    var tail2 = valueToPoint(tailValue + delta, 0.12);
    
    return [head, head1, tail2, tail, tail1, head2, head];
    
    function valueToPoint(value, factor)
    {
      var point = self.valueToPoint(value, factor);
      point.x -= self.config.cx;
      point.y -= self.config.cy;
      return point;
    }
  }
  
  this.drawBand = function(start, end, color){
    /**function:drawBand(start, end, color)
      Draws the coloured bands in the circumference

      :param int start: The start of the band, measured in degrees
      :param int end: The end of the band, measured in degrees
      :param str color: The colour of the band
    */
    if (0 >= end - start) return;
    
    this.body.append("svg:path")
          .style("fill", color)
          .attr("d", d3.svg.arc()
            .startAngle(this.valueToRadians(start))
            .endAngle(this.valueToRadians(end))
            .innerRadius(0.65 * this.config.raduis)
            .outerRadius(0.85 * this.config.raduis))
          .attr("transform", function() { return "translate(" + self.config.cx + ", " + self.config.cy + ") rotate(270)" });
  }
  
  this.redraw = function(value, transitionDuration){
    /**function:redraw(value, transitionDuration)
      Redraws the gauge
      
      :param float value: The new value
      :param float transitionDuration: The duration of the state transition
    */
      var pointerContainer = this.body.select(".pointerContainer");
    
    pointerContainer.selectAll("text").text(Math.round(value));
    
    var pointer = pointerContainer.selectAll("path");
    pointer.transition()
          .duration(undefined != transitionDuration ? transitionDuration : this.config.transitionDuration)
          //.delay(0)
          //.ease("linear")
          //.attr("transform", function(d) 
          .attrTween("transform", function()
          {
            var pointerValue = value;
            if (value > self.config.max) pointerValue = self.config.max + 0.02*self.config.range;
            else if (value < self.config.min) pointerValue = self.config.min - 0.02*self.config.range;
            var targetRotation = (self.valueToDegrees(pointerValue) - 90);
            var currentRotation = self._currentRotation || targetRotation;
            self._currentRotation = targetRotation;
            
            return function(step) 
            {
              var rotation = currentRotation + (targetRotation-currentRotation)*step;
              return "translate(" + self.config.cx + ", " + self.config.cy + ") rotate(" + rotation + ")"; 
            }
          });
  }
  
  this.valueToDegrees = function(value)
  {
    // thanks @closealert
    //return value / this.config.range * 270 - 45;
    return value / this.config.range * 270 - (this.config.min / this.config.range * 270 + 45);
  }
  
  this.valueToRadians = function(value)
  {
    return this.valueToDegrees(value) * Math.PI / 180;
  }
  
  this.valueToPoint = function(value, factor)
  {
    return {  x: this.config.cx - this.config.raduis * factor * Math.cos(this.valueToRadians(value)),
          y: this.config.cy - this.config.raduis * factor * Math.sin(this.valueToRadians(value))    };
  }
  
  // initialization
  this.configure(configuration);  
}

var gauges = [];
      
function createGauge(name, label, min, max){
  /**function:CreateGauge(name, label, min, max)
    Creates a new gauge and appends it to an array of gauges
    
    :param str name: The name of the gauge and the key of the array
    :param str label: An identificatory label
    :param int min: The minimal value
    :param int max: The maximum value
  */
  var config = 
  {
    size: 120,
    label: label,
    min: undefined != min ? min : 0,
    max: undefined != max ? max : 100,
    minorTicks: 5
  }
  
  var range = config.max - config.min;
  config.yellowZones = [{ from: config.min + range*0.75, to: config.min + range*0.9 }];
  config.redZones = [{ from: config.min + range*0.9, to: config.max }];
  
  gauges[name] = new Gauge(name + "GaugeContainer", config);
  gauges[name].render();
}

function createGauges()
{
  createGauge("memory", "Memory");
  //createGauge("cpu", "CPU");
  //createGauge("network", "Network");
  //createGauge("test", "Test", -50, 50 );
}

function updateGauges(){
  /**function:updateGauges()
    Updates all the gauges calling its ``redraw`` method
  */
  for (var key in gauges)
  {
    var value = getRandomValue(gauges[key])
    gauges[key].redraw(value);
  }
}

function getRandomValue(gauge){
  var overflow = 0; //10;
  return gauge.config.min - overflow + (gauge.config.max - gauge.config.min + overflow*2) *  Math.random();
}

function initialize(){
  createGauges();
  setInterval(updateGauges, 5000);
}