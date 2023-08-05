'use strict'

function probeSocket(uri, callback, errcallback){
    /**function:probeSocket(uri, callback, errcallback)
        Determines if a WebSocket connection can be established

        :param str uri: The uri where to connect to
        :param function callback: A success callback
        :param function errcallback: An error callback
    */
    var probews;
    probews = new WebSocket(uri);
    
    probews.onmessage= function(evt){
        callback(evt);
        probews.close();
    }
    
    probews.onerror = function(evt){
        errcallback(evt);
        probews.close();
    }
    
}

function nodo(info, callback){
    /**function:nodo(info, callback)
        Creates a new node element

        :param str info: The ip of the node
        :param function callback: The callback with either the information of the node or an error message
    */
    var uri = "wss://"+info+":1370/ws/probe/";
    probeSocket(uri, function(evt){
        var i = info;
        var cadena = "<div class='node not-chosen'>";
        cadena += "<p class='ip'>"+i+"</p>";
        cadena += "<input class='deploy' type='checkbox'></input>"
        cadena += "</div>";
        callback(cadena);
    }, function(evt){
        var i = info;
        var probeuri = "https://"+i+":1370/";
        var cadena = "<div class='node not-chosen'>";
        cadena += "<p class='ip'>"+i+"</p>";
        cadena += "<p>Error en la creación del socket. Click <a href='"+probeuri+"'>aquí para resolver</a></p>"
        cadena += "<input class='deploy' type='checkbox'></input>"
        cadena += "</div>";
        callback(cadena);
    });
}

$(document).ready(function() {
    /**function:ready()
        Binds the DOM elements
    */

    $("#listanodos").on('click', "input[type=checkbox]", function(){
        $(this).closest(".node").toggleClass("chosen").toggleClass("not-chosen");
    });
    
    $("#list").delegate('.delete-buton', 'click', function(){
        var index = $(this).parent().index();
        
        $(this).parent().fadeOut(400, function(){
            $(this).remove();
            files_to_upload.splice(index, 1);
        });
    });

    $('#list').delegate('input[name=polo]', 'click', function(){
        if($(this).is(':checked')){
            $(this).siblings('input[name=idpolo]').prop('disabled', false);
            $(this).siblings('.polo.alert-warning').show(400);
        }else{
            $(this).siblings('input[name=idpolo]').prop('disabled', true);
            $(this).siblings('.polo.alert-warning').hide(400);
        }
    });

    $('#list').delegate('input[name=tomcat]', 'click', function(){
        if($(this).is(':checked')){
            $(this).siblings('.warning.alert-warning').show(400);
            $(this).siblings('input[name=folder]').prop('disabled', true);
            $(this).siblings('input[name=folder]').prop('placeholder', 'Default Tomcat directory');
        }else{
            $(this).siblings('.warning.alert-warning').hide(400);
            $(this).siblings('input[name=folder]').prop('disabled', false);
            $(this).siblings('input[name=folder]').prop('placeholder', 'Deployment folder');
        }
    });
});



//http://hayageek.com/drag-and-drop-file-upload-jquery/

function sendFileToServer(formData, status) {
    /**function:sendFileToServer(formData, status)
        Sends the deployment information

        :param object formData: The data to send
        :param int status: A jQuery object that controls a progress bar which represents the upload process
    */

    var uploadURL = "/upload/"; //Upload URL
    var extraData = {}; //Extra Data.
    var jqXHR = $.ajax({
        xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                xhrobj.upload.addEventListener('progress', function(event) {
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total = event.total;
                    if (event.lengthComputable) {
                        percent = Math.ceil(position / total * 100);
                    }

                    status.setProgress(percent);
                }, false);
            }
            return xhrobj;
        },
        url: uploadURL,
        type: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: formData,
        beforeSend:function(data){
            $(".alert.alert-success").hide();
        },
        success: function(data) {
            status.setProgress(100);
            $(".alert.alert-success").show();
            $(".alert.alert-success").text("File upload done");
        }
    });
}

function createStatusbar(obj){
    /**function:createStatusbar(obj)
        Creates the status bar object
    */
    this.obj = $(obj);
    this.setProgress = function(progress){
        obj.attr("aria-valuenow", progress);
        obj.css("width",progress + "%");
        obj.html(progress + "%");
    }
}

function handleFileUpload(files, obj) {
    /**function:handleFileUpload(files, obj)
        Parses the HTML form and creates a form with all the information to upload

        :param list files: An array with each of the deployment objects
        :param object obj: (**deprecated**) The deployment area
    */
    for (var i = 0; i < files.length; i++) {

        files[i].command = $(".upload-item").eq(i).find("input[name=command]").val();
        //files[i].folder = $(".upload-item").eq(i).find("input[name=folder]").val();
        files[i].polo = $(".upload-item").eq(i).find("input[name=polo]").is(':checked');
        if(files[i].polo){
            files[i].identifier = $(".upload-item").eq(i).find("input[name=idpolo").val();
        }
        
        if($(".upload-item").eq(i).find("input[name=tomcat]").is(':checked')){
            files[i].tomcat = true
            
        }else{
            files[i].tomcat = false      
            files[i].folder = $(".upload-item").eq(i).find("input[name=folder]").val();
        }

        
        files[i].overwrite = $(".upload-item").eq(i).find("input[name=overwrite]").is(':checked');
        
        
        var fd = new FormData();
        fd.append('file', files[i].file);
        fd.append('command', files[i].command);
        fd.append('folder', files[i].folder);
        if(files[i].tomcat === true)
            fd.append('tomcat', files[i].tomcat);
        fd.append('overwrite', files[i].overwrite);
        var cadena = "";
        var ips = $(".chosen").children(".ip")
        var j = i;

        if(ips.length > 0){
            ips.each(function(index){
                
                cadena += $(this).html() + ",";
                var ip = $(this).html();

                /*createSocket(ip,*/

                (function(){

                    if(index >= ips.length - 1){

                        fd.append('nodes', cadena);
                        
                        var status = new createStatusbar($(".progress-bar").eq(j));
                        createTabs(ip);
                        sendFileToServer(fd, status);
                    }
                })();
            });
            
        }
    }
}

var fileCount = 0;

function addToList(file){
    /**function:addToList(file)
        Creates a panel control to the file
    
        :param str file: The name of the new file
    */
    var filename = file.name;

    var other= '<li class="list-group-item upload-item"><button style="width:10%;" class="btn btn-danger delete-buton pull-right"><div class="glyphicon glyphicon-remove"></div></button>'
    var header_filename = '<p class="list-group-item-header">'+filename+'</p><div style="width:85%;" class="progress"><div role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" class="progress-bar"></div></div>'
    var buttons = '<input type="text" name="command" placeholder="Command" maxlength="300"/><br/><input type="text" placeholder="Deployment folder" name="folder" maxlength="300"/><br/><label list-group-item-text="list-group-item-text" for="polo">Deploy in Polo?</label><input type="checkbox" value="polo" name="polo"/><input type="text" name="idpolo" placeholder="Identifier" maxlength="40" disabled="true"/><p class="alert alert-warning polo" style="display:none;">The service will be registered permanently. Use the language-specific binding to perform a temporary registry on execution time.</p>'
    var labels = '<br></br><label list-group-item-text="list-group-item-text" for="tomcat">Deploy in Tomcat?</label><input type="checkbox" value="tomcat" name="tomcat"/><p class="alert alert-warning warning" style="display:none;">The service will be installed on the Tomcat deployment directory after validating the format of the archive. If no instance of Tomcat is installed on the server, it won\'t be installed.</p>'
    labels += '<br></br><label list-group-item-text="list-group-item-text" for="overwrite">Overwrite file if it exists?</label><input type="checkbox" value="overwrite" name="overwrite" checked/></li>'

    var str = other + header_filename + buttons + labels;
    $("#list").append(str);
}

var files_to_upload;

$(document).ready(function() {
    /**function:ready
        Binds the initial event handlers and data structures
    */
    files_to_upload = new Array();

    var obj = $("#dragandrophandler");
    obj.on('dragenter', function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).css('border', '2px solid #0B85A1');
    });
    obj.on('dragover', function(e) {
        e.stopPropagation();
        e.preventDefault();
    });
    obj.on('drop', function(e) {

        $(this).css('border', '2px dotted #0B85A1');
        e.preventDefault();
        var files = e.originalEvent.dataTransfer.files;
        for (var i = 0; i < files.length; i++) {
            files_to_upload.push({file: files[i]});
            fileCount++;
            addToList(files[i]);
        }
    });

    $(document).on('dragenter', function(e) {
        e.stopPropagation();
        e.preventDefault();
    });
    $(document).on('dragover', function(e) {
        e.stopPropagation();
        e.preventDefault();
        obj.css('border', '2px dotted #0B85A1');
    });
    $(document).on('drop', function(e) {
        e.stopPropagation();
        e.preventDefault();
    });

    $("#uploadbutton").on('click', function(e){
        handleFileUpload(files_to_upload, obj);
    });

    //from http://www.jacklmoore.com/notes/jquery-tabs/
    $("ul.tabs").each(function() {
        var $active, $content, $links = $(this).find('a');

        // If the location.hash matches one of the links, use that as the active tab.
        // If no match is found, use the first link as the initial active tab.
        $active = $($links.filter('[href="' + location.hash + '"]')[0] || $links[0]);
        $active.addClass('active');

        $content = $($active[0].hash);

        // Hide the remaining content
        $links.not($active).each(function() {
            $(this.hash).hide();
        });

        // Bind the click event handler
        $(this).on('click', 'a', function(e) {
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
            //e.preventDefault();
        });
    });
});

