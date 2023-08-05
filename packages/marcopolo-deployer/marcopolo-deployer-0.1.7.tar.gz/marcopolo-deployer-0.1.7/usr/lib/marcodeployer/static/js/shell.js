var shellTabs = {};

function processCommand(input){
	/**function:processCommand(input)
		Creates a new command output

		:param str input: The command to execute
	*/
	var hosts = [];
	$(".doexecute").each(function(index, element){
		hosts[hosts.length] = $(element).text();
	});
	sendInput(input, hosts);
}


function sendInput(input, hosts){
	/**function:sendInput(input, hosts)
		Sends the command to each of the nodes in the network

		:param str input: The command
		:param list hosts: The list of nodes
	*/
	for(host in hosts){
		opensockets[hosts[host]].send(JSON.stringify({user_id:$.cookie("user"),command:input}));
	}
}

function scrollToBottom(placeholder){
	/**function:scrollToBottom(placeholder)
		Automatically scrolls the placeholder to the bottom

		:param object placeholder: The jQuery object with the tab
	*/
	var panel_body = placeholder.find(".panel-body");
	panel_body.scrollTop(panel_body.prop('scrollHeight'));
}

function appendShellOutput(input, ip, stream_name, stop, command, identifier){
	/**function:appendShellOutput(input, ip, stream_name, stop, command, identifier)
		Appends a new output or ends the command execution

		:param str input: The input command
		:param str ip: The ip of the node
		:param str stream_name: The name of the stream (stdout, stderr)
		:param bool stop: Indicates if the message is the "EOF" of the stream
		:param str command: The name of the command
		:param str identifier: An unique identifier for the command
	*/
	var panel_body = shellTabs[ip].find(".panel-body");
	var doScroll = ((panel_body.scrollTop()+200) == panel_body.prop('scrollHeight'));

	if(stop == false){
		shellTabs[ip].find(".panel-body").append("<p class='"+stream_name+"'>"+escapeHtml(input)+"</p>");
		//if(!shellTabs[ip].find(".panel-body").hasClass(identifier)){
		shellTabs[ip].find(".panel-heading").addClass(identifier);
		
	}else{
		shellTabs[ip].find(".panel-body").append("<p class='"+stream_name+"'>"+"End of "+stream_name+" for "+command+"</p>");
		shellTabs[ip].find(".panel-heading").removeClass(identifier)
	}
	if(doScroll) scrollToBottom(shellTabs[ip]);
}


function createShellTab(ip){
	/**function:createShellTab(ip)
		Creates the HTML of a new tab and appends it
	*/
    var identifier = "tab"+(Object.keys(shellTabs).length);

    $("#shellwindow").append("<div id='"+identifier+"' class='col-xs-6'><div class='panel panel-primary'><div class='panel-heading' style='display:block;overflow:auto'><span class='ipaddr doexecute'>"+ip+"</span><button style='width:10%;margin-left:10px;' class='btn btn-danger stopexecution pull-right'><div class='glyphicon glyphicon-remove'></button><input class='pull-right executecheckbox' type='checkbox' name='execute' checked></input></div><div class='panel-body output'></div></div></div>");
    
    shellTabs[ip] = $("#"+identifier);

}

function createShell(ip){
	createShellTab(ip);
}

$(document).ready(function(){
	/**function:ready()
		Binds the initial events
	*/
	$("#command input").attr("placeholder", "$"+$("span.username").text()+">");

	$("#command input").on('keyup', function(e){
		
		if(e.which == 13){
			e.preventDefault();
			var command = $(this).val();
			$(this).val("");
			processCommand(command);
			
		}
	});

	$("#shellwindow").on('click', ".executecheckbox", function(){
		$panel = $(this).closest(".panel");
		$node = $(this).siblings(".ipaddr").first();
		
		if($(this).is(":checked")){
			$panel.removeClass("panel-default").addClass("panel-primary");
			$node.addClass("doexecute");
		}else{
			$panel.removeClass("panel-primary").addClass("panel-default");
			$node.removeClass("doexecute");
		}
	});

	$("#shellwindow").on("click", ".stopexecution", function(){
		//console.log($(this).parent());
		//console.log($(this).parent().attr('class').split(" "));
		var classes=$(this).parent().attr('class').split(" ");
		var ip = $(this).siblings(".ipaddr").text();

		var m = classes.indexOf("panel-heading");
		if(m != -1){
			classes.splice(m, 1);
		}
		console.log(classes);

		for (var i = classes.length - 1; i >= 0; i--) {
			//if(classes[i] != "panel-heading"){
			var ws = opensockets[ip];
        	ws.send(JSON.stringify({"removeshell":classes, "user_id":$.cookie("user")}));
			//}
		};
	})
});