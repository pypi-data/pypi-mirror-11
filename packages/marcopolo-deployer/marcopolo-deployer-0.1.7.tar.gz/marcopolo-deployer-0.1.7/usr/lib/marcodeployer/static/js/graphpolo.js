'use strict'

var PORT=1370

var opensockets = {};

$(document).ready(function(){
  /**function:getNodes()
  Gets all the nodes and initializes the panels
  */
  $.ajax({
    url:"/nodes/",
    type: 'GET',
    success: function(data, textStatus, x){
      $("#count").text(data.nodes.length)
      $("#listanodos").html("");
      $("#statusmonitor").html("");
      if(data.nodes.length == 0){
        var htmlstring = '<div class="container"><div class="row"><p>No nodes were found</p></div></div>';
        $("#statusmonitor").html(htmlstring);
        $("#listanodos").html("<p>No nodes were found</p>")
      }
      for(var ip in data.nodes){
        createPanel(nodes++, data.nodes[ip]);

        nodo(data.nodes[ip], function(data){
          $("#listanodos").append(data);
        });

        createShell(data.nodes[ip]);
        opensockets[data.nodes[ip]] = createSocket(data.nodes[ip]);
      }
    },
    error: function(x, status, error){

      var htmlstring = '<div class="container"><div class="row"><p>Error in node detection</p></div></div>';
        $("#statusmonitor").html(htmlstring);
    },
    dataType: 'json'
  });


});

//Suponemos una temperatura máxima de 100º para el valor máximo del termómetro
var MAXTEMP = 100;
var nodes=0;
//Grupos de memoria
var groups = [
  "Free",
  "InUse",
  "Cached"
];

var gauges = [];

function createPanel(number, ip){
  /**function:CreatePanel(number, ip)
    Creates a panel that displays the information about a node

    :param int number: An identificatory number
    :param str ip: The ip of the node, necessary to create the WebSocket connection
  */
  gauges[number] = [];

  //initialize();
  var htmlstring = '<div class="container"><div class="panel panel-primary"><div class="panel-heading"><h3 id="hostname-'+number+'" class="panel-title">Host</h3><p id="time-'+number+'" class="pull-right"></p><p id="uptime-'+number+'"></p><p id="network-'+number+'"></p></div><br>';

  htmlstring += '<div class="row"><div id="memdiv-'+number+'" class="col-sm-6"><div class="panel panel-primary"><div class="panel-heading"><h3 class="panel-title">Memory and swap</h3></div></div><div class="panel-body"><div class="col-sm-6"><div id="memgraph-'+number+'"></div></div><div class="col-sm-6"><div id="swapgraph-'+number+'"></div></div><div class="col-sm-12"><div class="col-sm-4 memorylegend free">Free</div><div class="col-sm-4 memorylegend used">Used</div><div class="col-sm-4 memorylegend cached">Cached</div></div></div></div><div class="col-sm-6"><div class="panel panel-primary"><div class="panel-heading"><h3 class="panel-title">Top (name, %CPU, %MEM)</h3></div></div><div class="panel-body"><div id="top-processes-'+number+'"></div></div></div></div>'

  htmlstring += '<div class="row"><div class="col-sm-6"><div class="panel panel-primary"><div class="panel-heading"><h3 class="panel-title">Temperature</h3></div></div><div class="panel-body"><div class="col-sm-6" id="temperature-div-'+number+'"><p id="temperature-'+number+'"></p></div></div></div><div class="col-sm-6"><div class="panel panel-primary"><div class="panel-heading"><h3 class="panel-title">CPU</h3></div></div><div class="panel-body"><div class="col-sm-6" id="cpus-'+number+'"></div></div><div class="panel-body"><div class="col-sm-12" id="cpu-'+number+'"></div></div></div></div></div><p id="top-'+number+'"></p><p id="kernel-name-'+number+'"></p></div></div>'

  $("#statusmonitor").append(htmlstring);



  //D3 incluye un sistema de eventos. Solicitamos utilizar los eventos de carga y cambio de estado
  var dispatch = d3.dispatch("load", "statechange");
  var dispatchtemperature = d3.dispatch("load", "statechange");
  var dispatchswap = d3.dispatch("load", "statechange", "stop");


  var stateById = d3.map(); //Mapa asociativo
  
  

  //Construcción de la URI y conexión al WebSocket
  var loc = ip;
  var uri = "wss:";
  uri += "//" + loc + ":"+PORT+"/ws/status/";



    // //Registro de callbacks para los eventos
  dispatchtemperature.on("load", function(maxtemperature){
  /*Evento de carga del gráfico de temperatura*/
    //Márgenes
    var margin = {top: 20, right: 20, bottom: 30, left: 40};
    var width = 80 - margin.left - margin.right,
      height = 260 - margin.top - margin.bottom;

    var color = d3.scale.ordinal()
      .domain([0, maxtemperature])
      .range(["#da2724", "#db2724", "#dc2724", "#dd2724", "#de2724", "#d0743c", "#ff8c00"]);

    var y = d3.scale.linear()
      .domain([0, maxtemperature])
      .rangeRound([height, 0])
      .nice();

    var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickFormat(d3.format(".2s"));

    var svg = d3.select("#temperature-div-"+number).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    var rect = svg.append("rect")
      .attr("x", 4)
      .attr("width", width - 4)
      .attr("y", height)
      .attr("height", 0)
      .style("fill", color);

    dispatchtemperature.on("statechange.bar", function(d) {
    /*Evento de cambio*/
        rect.transition()
            .attr("y", y(d))
            .attr("height", y(0) - y(d))
            .style("fill", "rgba(255,0,0,"+d/maxtemperature+")");
    });
  });

  dispatch.on("load.pie", function(stateById) {
/*Evento de carga del gráfico de quesos para la memoria en uso*/

  var width = $("#memdiv-"+number).width() / 2.5,
      height = $("#memdiv-"+number).width() / 2.5,
      radius = Math.min(width, height) / 2;
      
    if(width < 100){
      width = 200;
      height = width;
      radius = Math.min(width, height) / 2;
    }

  /*Colores de cada tipo de memoria. Se eligen según un rango de colores dados*/
  var color = d3.scale.ordinal()
      .domain(groups)
      .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

  /*Creación del arco con los radios interno y externo*/
  var arc = d3.svg.arc()
      .outerRadius(radius - 10)
      .innerRadius(radius - 70);

  /*Creación del gráfico*/
  var pie = d3.layout.pie()
      .sort(null);

  /*Creación de un svg con el gráfico */
  var svg = d3.select("#memgraph-"+number).append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")


  /*Creación de cada uno de los "quesos" como path*/
  var path = svg.selectAll("path")
      .data(groups)
      .enter()
      .append("path")
      .style("fill", color)
      .each(function() { this._current = {startAngle: 0, endAngle: 0}; });

  var texto = svg.append("text")
    .attr("witdh", width)
    .attr("height", height)
    .text("Memoria")
    .style("text-anchor", "middle")
    .attr("transform", "translate(" + 0 + "," + 0 + ")");

  var bottomText = svg.append("text")
    .text("Memoria")
    .style("text-anchor", "middle")
    .attr("transform", "translate("+0+","+height/2+")");


  dispatch.on("statechange.pie", function(d) {
    /*Evento de cambio*/

    path.data(pie.value(function(g) { return d[g]; })(groups)).transition()
        .attrTween("d", function(d) {
          var interpolate = d3.interpolate(this._current, d);
          this._current = interpolate(0);
          return function(t) {
            return arc(interpolate(t));
          };
    });
    
    if(d["InUse"] > 0)
        texto.text((100 - ((d["Free"]/(d["Free"]+d["InUse"])) * 100)).toFixed(2) + "%");
    else
        texto.text("0%");
  });

});

  dispatchswap.on("load.pie", function(stateById) {
  /*Evento de carga del gráfico de quesos para la memoria en uso*/
    
    var width = $("#memdiv-"+number).width()/2.5,
        height = $("#memdiv-"+number).width()/2.5,
        radius = Math.min(width, height) / 2;
    if(width < 100){
      width = 200;
      height = width;
      radius = Math.min(width, height) / 2;
    }
    /*Colores de cada tipo de memoria. Se eligen según un rango de colores dados*/
    var color = d3.scale.ordinal()
        .domain(groups)
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    /*Creación del arco con los radios interno y externo*/
    var arc = d3.svg.arc()
        .outerRadius(radius - 10)
        .innerRadius(radius - 70);

    /*Creación del gráfico*/
    var pie = d3.layout.pie()
        .sort(null);

    /*Creación de un svg con el gráfico */
    var svg = d3.select("#swapgraph-"+number).append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");


    /*Creación de cada uno de los "quesos" como path*/
    var path = svg.selectAll("path")
        .data(groups)
        .enter()
        .append("path")
        .style("fill", color)
        .each(function() { this._current = {startAngle: 0, endAngle: 0}; });
    
    
    var texto = svg.append("text")
        .attr("witdh", width)
        .attr("height", height)
        .text("Swap")
        .style("text-anchor", "middle")
        .attr("transform", "translate(" + 0 + "," + 0 + ")");

    var bottomText = svg.append("text")
      .text("Swap")
      .style("text-anchor", "middle")
      .attr("transform", "translate("+0+","+height/2+")");

  dispatchswap.on("stop.pie", function(d){
    bottomText.text("No hay swap");
  });

  dispatchswap.on("statechange.pie", function(d) {

    
    if(d.Free == 0 && d.InUse == 0 && d.Cached == 0){
      dispatchswap.stop();
    }
    /*Evento de cambio*/
    path.data(pie.value(function(g) { return d[g]; })(groups)).transition()
        .attrTween("d", function(d) {
          var interpolate = d3.interpolate(this._current, d);
          this._current = interpolate(0);
          return function(t) {
            return arc(interpolate(t));
          };


    });
    
    if(d["InUse"] > 0)
        texto.text((100-d["Free"]/(d["Free"]+d["InUse"]) * 100).toFixed(2) + "%");
    else
        texto.text("0%");
    
    });

    
  });


  //Carga de los gráficos
  dispatch.load([{"Free":0,"Cached":0}]);
  dispatchswap.load([{"Free":0,"Cached":0}]);
  dispatchtemperature.load(MAXTEMP);

  dispatchswap.statechange({"Free":1, "InUse":0,"Cached":0});
  dispatch.statechange({"Free":1, "InUse":0,"Cached":0});

  try{
    var ws = new WebSocket(uri);
  }catch(e){
    console.log("Cannot create the WebSocket");
  }

    ws.onerror = function(evt){
      var probe = "https://"+loc+":"+PORT+"/probe/";
      
      $("#hostname-"+number)
      .closest(".panel-heading")
      .append("<p>The websocket connection could not be created. Check your network connectivity and make sure that you can establish a connection clicking <a style='color:#fff' href='"+probe+"'>here</a></p>");
  
    }
    ws.onmessage = function(evt){

      var data = JSON.parse(evt.data);
      
      $("#hostname-"+number).html(data["hostname"] + "@" + data["ip"]);

      $("#temperature-"+number).html("Temperature: "+data["temperature"]);

      dispatch.statechange({"Free":+data["memfree"], "InUse":data["memtotal"]-data["memfree"],"Cached":+data["memcached"]});
      dispatchswap.statechange({"Free":+data["swapfree"], "InUse":data["swaptotal"]-data["swapfree"],"Cached":0});
      dispatchtemperature.statechange(+data["temperature"]);
      

      
      $("#time-"+number).text("Node time: "+new Date(data["time"]));
      
      var uptime_data = data["load_average"].split("-");
      $("#uptime-"+number).text("Uptime: "+uptime_data[0]+". Load average: "+uptime_data[1].replace(/,$/, "")+" "+uptime_data[2].replace(/,$/, "")+" "+uptime_data[3].replace(/,$/, ""));

      $("#network-"+number).text("Megabytes received: "+(data["rx"]/(1024*1024)).toFixed(2));
      $("#network-"+number).text($("#network-"+number).text()+". Megabytes sent:"+(data["tx"]/(1024*1024)).toFixed(2));
      //$("#time-"+number).append("Desfase de " + (new Date() - new Date(data["time"]) + "ms"));
      //clock(number, new Date(data["time"]));
      var procesos = "";
      
      $.each(data["top_list"].split("\n"), function(index, value, array){
        if (value != ""){
          //procesos += value != "" ? "<li class='list-group-item'>"+value+"</li>" : "";
          var values = value.split("-");
          if(values.length > 0)
            procesos += "<li class='list-group-item'>"+values[2]+" <span class='top-percentage'>("+values[1]+"%) </span><span class='top-percentage'>("+values[0]+"%)</span></li>";
        }else{
          procesos += "";
        }


      });
      
      $("#top-processes-"+number).html("<ul class='scrollable-top list-group'>"+procesos+"</ul>");

      var cpus = "";
      for(var cpu in data["cpus"]){
        cpus += "<div class='col-sm-6'><p>"+data["cpus"][cpu].toFixed(2)+"</p></div>";

      }

      var config = 
      {
        size: 100,
        label: "CPU",
        min: 0,
        max: 100,
        minorTicks: 5
      }
      var range = config.max - config.min;
        config.yellowZones = [{ from: config.min + range*0.75, to: config.min + range*0.9 }];
        config.redZones = [{ from: config.min + range*0.9, to: config.max }];

      //$("#cpus-"+number).html(cpus);
      var j = 0;
      if(gauges[number].length == 0){
        for (var cpu in data["cpus"]){
          $("#cpus-"+number).append("<div class='col-sm-6' id='cpus-"+number+""+j+"'></div>");
          config.label="CPU "+j;
          gauges[number][j] = new Gauge("cpus-"+number+""+j, config);
          gauges[number][j++].render();
        }
      }else{
        for (var cpu in data["cpus"]){
          gauges[number][j++].redraw(data["cpus"][cpu].toFixed(2));
        }
      }

    }

    ws.onclose=function(evt){
        //console.log("Connection closed");
    }
}



function clock(number, time){
  //Credit to: http://bl.ocks.org/mbostock/1096355

    var width = 260,
        height = 200,
        radius = Math.min(width, height) / 1.9,
        spacing = .09;

    var formatSecond = d3.time.format("%S s"),
        formatMinute = d3.time.format("%M m"),
        formatHour = d3.time.format("%H h"),
        formatDay = d3.time.format("%a"),
        formatDate = d3.time.format("%d d"),
        formatMonth = d3.time.format("%b");

    var color = d3.scale.linear()
        .range(["hsl(-180,50%,50%)", "hsl(180,50%,50%)"])
        .interpolate(interpolateHsl);

    var arc = d3.svg.arc()
        .startAngle(0)
        .endAngle(function(d) {
            return d.value * 2 * Math.PI;
        })
        .innerRadius(function(d) {
            return d.index * radius;
        })
        .outerRadius(function(d) {
            return (d.index + spacing) * radius;
        });

    var svg = d3.select("#clock-"+number).append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var field = svg.selectAll("g")
        .data(fields)
        .enter().append("g");

    field.append("path");

    field.append("text");

    d3.transition().duration(0).each(tick);

    d3.select(self.frameElement).style("height", height + "px");

    function tick() {
        field = field
            .each(function(d) {
                this._value = d.value;
            })
            .data(fields)
            .each(function(d) {
                d.previousValue = this._value;
            });

        field.select("path")
            .transition()
            .ease("elastic")
            .attrTween("d", arcTween)
            .style("fill", function(d) {
                return color(d.value);
            });

        field.select("text")
            .attr("dy", function(d) {
                return d.value < .5 ? "-.5em" : "1em";
            })
            .text(function(d) {
                return d.text;
            })
            .transition()
            .ease("elastic")
            .attr("transform", function(d) {
                return "rotate(" + 360 * d.value + ")" + "translate(0," + -(d.index + spacing / 2) * radius + ")" + "rotate(" + (d.value < .5 ? -90 : 90) + ")"
            });

        setTimeout(tick, 1000 - Date.now() % 1000);
    }

    function arcTween(d) {
        var i = d3.interpolateNumber(d.previousValue, d.value);
        return function(t) {
            d.value = i(t);
            return arc(d);
        };
    }

    function fields() {
        var now = new Date;
        return [{
            index: .7,
            text: formatSecond(now),
            value: now.getSeconds() / 60
        }, {
            index: .6,
            text: formatMinute(now),
            value: now.getMinutes() / 60
        }, {
            index: .5,
            text: formatHour(now),
            value: now.getHours() / 24
        }, {
            index: .3,
            text: formatDay(now),
            value: now.getDay() / 7
        }, {
            index: .2,
            text: formatDate(now),
            value: (now.getDate() - 1) / (32 - new Date(now.getYear(), now.getMonth(), 32).getDate())
        }, {
            index: .1,
            text: formatMonth(now),
            value: now.getMonth() / 12
        }];
    }

    // Avoid shortest-path interpolation.
    function interpolateHsl(a, b) {
        var i = d3.interpolateString(a, b);
        return function(t) {
            return d3.hsl(i(t));
        };
    }

}






