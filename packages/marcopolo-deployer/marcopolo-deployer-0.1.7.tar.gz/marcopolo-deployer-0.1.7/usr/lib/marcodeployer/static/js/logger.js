var connectedSockets = []
var newConnections=0;

function newConnection(){
    /**function:newConnection()
        Notifies the income of a new output stream
    */
    newConnections++;
    $badge = $("span.badge.logger-badge");
    $badge.text(newConnections);
    if(!$badge.hasClass("active")){
        $badge.show();
    }
}

function resetConnectionsCounter(){
    /**function:resetConnectionsCounter()
        Resets the connections counter
    */
    newConnections=0;
    $("span.badge.logger-badge").hide();
}

$(document).ready(function(){
    /**function:bindEvents()
        Binds all the required DOM events
    */
    $(".logger-link").on('click', function(){
        resetConnectionsCounter();
    });
});


function createSocket(url, callback){
    /**function:createSocket(url, callback)
        Creates the socket connection and performs some testing of it

        :param str url: The websocket ip or url
        :param function callback: A callback that is invoked if the connection is opened successfully
    */
    //The socket is only created once
    if(connectedSockets.indexOf(url) > -1){
        callback();
        return;
    }
    
    connectedSockets.push(url);

    var loc = window.location;
    var uri = loc.protocol == "https:" ? "wss:" : "ws:"; //HTTPS detection
    uri += "//" +url+":1370" + "/ws/logger/";
    var ws;
    
    ws = new WebSocket(uri);

    ws.onmessage = function(evt) {
        /**function:onmessage(evt)
            Determines whether the message is a new output stream, creating a new frame or an already
            existing one, appending the message to the existing frame.

            :param object evt: The event object, containing the message
        */
        var msg = JSON.parse(evt.data);
        //If it is the first output received, the output frame is created
        if(msg.shell == true){
            appendShellOutput(msg.message, msg.ip, msg.stream_name, msg.stop, msg.command, msg.identifier);
        }else{
            if($("#"+msg.identifier).length < 1){
                createOutput(msg.ip, msg.identifier, msg.command);
                newConnection();
            }
                
            addOutput(msg.ip, msg.identifier, msg.message, msg.stream_name, msg.stop);
        }
    };
    
    ws.onopen=function(evt){
        /**function:onopen(evt)
            Sends the secure cookie to the server in order to register for events 
            and invokes the callback function. The authentication is based on the HMAC message stored in the cookie
        
            :param object evt: An object with the opening event information.
        */
        ws.send(JSON.stringify({register:$.cookie("user")}));
        if(callback != undefined)
            callback();
    };

    ws.onerror= function(evt){
        //
    };

    return ws;
}

var tabs = [];

function createTabs(host){
    /**function:CreateTabs(host)
        Creates a tab for the output of a host. If the tab already existed no action is taken
    */
    if(!(host in tabs)){
        var identifier = "tab"+(Object.keys(tabs).length);
        $("ul.nav-tabs").append("<li><a href='#"+identifier+"'>"+host+"</a></li>");

        $("#window").append("<div class='tab' id='"+identifier+"' style='display:none'></div>");
        tabs[host] = $(identifier);
        parseTabs("ul.nav-tabs");
    }
}


function createOutput(host, identifier, command){
    /**function:createOutput(host, identifier, command)
        Appends a frame to display the output of a node

        :param str host: The name of the host (IP or URL)
        :param str identifier: A random identifier
        :param str command: The name of the command.
    */
    $tab = tabs[host];
    
    $("#"+$tab.selector).append("<div id='"+identifier+"' class='col-xs-6'><div class='panel panel-primary'><div class='panel-heading' style='display:block;overflow:auto'><p height='80%'>"+command+"</p><button style='width:10%;' class='btn btn-danger stop-button pull-right'><div class='glyphicon glyphicon-remove'></button></div><div class='panel-body output'></div></div></div></div>");

}

function escapeHtml(string) {
    /**function:escapeHTML(string)
        Escapes potentially malicious HTML strings, based on
        the mustache.js escaping function. See http://stackoverflow.com/a/12034334/2628463
    */
    var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
    };
    return String(string).replace(/[&<>"'\/]/g, function (s) {
      return entityMap[s];
    });
}
function addOutput(host, identifier, message, stream, stop){
    /**function:addOutput(host, identifier, message, stream, stop)
        Appends the output of a command to the panel.

        :param str host: The name of the host that created the output
        :param str identifier: An identifier of this output stream
        :param str message: The message
        :param str stream: The name of the stream (stdout or stderr)
        :param bool stop: A boolean that indicates if the message indicates the EOF of the stream
    */
    $tab = tabs[host];
    if (stop == true)
        //If the stop flag is true, no more input is appended and the style of the panel is modified
        $("#"+$tab.selector).find("#"+identifier).find(".panel").removeClass("panel-primary").addClass("panel-default");
    else{
        $("#"+$tab.selector).find("#"+identifier).find(".panel-body").append("<p class='"+stream+"'>"+escapeHtml(message)+"</p>");
    }
    
}


function parseTabs(selector) {
    /**function:parseTabs(selector)
        Creates or updates the event bindings of the tabs under 
        the element specified by ``selector``

        :param str selector: The DOM element that the tabs are children of   
    */
    $(selector).each(function() {

        var $active, $content, $links = $(this).find('a');

        // If the location.hash matches one of the links, use that as the active tab.
        // If no match is found, use the first link as the initial active tab.
        $active = $($links.filter('[href="' + location.hash + '"]')[0] || $links[0]);
        
        //$active.addClass('active');
        if ($active[0] === undefined)
            return
       
        $content = $($active[0].hash);

        // Hide the remaining content
        $links.not($active).each(function() {
            $(this.hash).hide();
        });

        $(this).unbind('click');
        // Bind the click event handler
        $(this).on('click', 'a', function(e) {
            
            $(selector+" li.active").removeClass('active');
            $(this).closest('li').addClass('active');
            // Make the old tab inactive.
            $active.removeClass('active');
            $content.hide();

            // Update the variables with the new link and content
            $active = $(this);
            $content = $(this.hash);
            
            // Make the tab active.
            $active.addClass('active');
            $content.show();

            // Prevent the anchor's default click action
            e.preventDefault();
        });
    });
};

$(document).ready(function(){
    /**function:ready()
        Initializes the components of the view
    */
    parseTabs("ul.nav-tabs");

    $("#window").on('click', '.stop-button', function(){
        var identifier = $(this).closest(".col-xs-6").attr('id');
        var id = $(this).closest(".tab").attr('id');
        var link = $("ul.nav-tabs").find("li").find('a[href="#'+id+'"]');
        /*console.log(link.text());
        console.log(identifier)*/
        var ws = opensockets[link.text()];
        ws.send(JSON.stringify({"remove":identifier, "user_id":$.cookie("user")}));
    })
});