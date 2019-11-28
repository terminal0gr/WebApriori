function guestlogin() {

    $.ajax({
        type: 'POST',
        url: 'phpfunctions/guestlogin.php'
    })
    .done(function(response) {

        res=JSON.parse(response);

        if (res.http_response_code==200) {
            sessionStorage.setItem('token', res.token);
            sessionStorage.setItem('apikey', res.apikey);
            sessionStorage.setItem('username', res.name);
        } else {
            MyModal("An error occured",res.http_response_code + ' ' + res.message);
        }

    })
    .fail(function(data) {

        if (data.responseText) {
            MyModal("Association rules mining",data.responseText);
        } else {
            MyModal("Association rules mining",'Unknown error occured!');
        }
    });
};
       
function executeFunctionByName(functionName, context /*, args */) {
    var args = Array.prototype.slice.call(arguments, 2);
    var namespaces = functionName.split(".");
    var func = namespaces.pop();
    for(var i = 0; i < namespaces.length; i++) {
      context = context[namespaces[i]];
    }
    return context[func].apply(context, args);
  }

var callingRoutine = "";
function MyModal(title="association rules mining",maincontext="", ConfirmFunc=false) {
    if ($("#MyModal")) {
        MyModalAnsw=false;
        var str = '<div class="modal fade" id="MyModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">';
        str +=    '    <div class="modal-dialog" role="document">';
        str +=    '        <div class="modal-content">';
        str +=    '            <div class="modal-header">';
        str +=    '                <h5 class="modal-title" id="exampleModalLabel">' + title + '</h5>';    
        str +=    '                <button type="button" class="close" data-dismiss="modal" aria-label="Close">';   
        str +=    '                   <span aria-hidden="true">&times;</span>';
        str +=    '                </button>';
        str +=    '            </div>';
        str +=    '            <div class="modal-body">';
        str +=    '               ' + maincontext; 
        str +=    '            </div>';
        str +=    '            <div class="modal-footer">'; 
        if (ConfirmFunc) {
            str +=    '                <button type="button" class="btn btn-primary" >Yes</button>'; 
            str +=    '                <button type="button" class="btn btn-primary" data-dismiss="modal">No</button>'; 
        }
        else {
            str +=    '                <button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>'; 
        }
        str +=    '            </div>'; 
        str +=    '        </div>'; 
        str +=    '    </div>'; 
        str +=    '</div>'; 
    }
    $("body").prepend(str);
    $( "#MyModal").modal('show');
}

function credits() {
    if ($("#Credits")) {
        str     = '<div class="modal fade" id="Credits" tabindex="-1" role="dialog">';
        str    +=    '<div class="modal-dialog" role="document">';
        str    +=    '    <div class="modal-content">';
        str    +=    '            <div class="modal-header">';
        str    +=    '                <h5 class="modal-title text-primary">Association rules<br><p class="text-secondary">An innovative association rules mining engine</p></h5>';             
        str    +=    '                <button type="button" class="close" data-dismiss="modal" aria-label="Close">';
        str    +=    '                    <span aria-hidden="true">&times;</span>';
        str    +=    '                </button>';
        str    +=    '           </div>';
        str    +=    '           <div class="modal-body">';
        str    +=    '               <h5 class="modal-title text-primary">Developer</h5>';
        str    +=    '               <p>Malliaridis Konstantinos</p>';
        str    +=    '            </div>';
        str    +=    '            <div class="modal-footer">';
        str    +=    '               <p class="text-center" >MSc in Web Intelligence &copy; 2019-2020</p>';
        str    +=    '           </div>';
        str    +=    '        </div>';
        str    +=    '    </div>';
        str    +=    '</div>';
    }
    $("body").prepend(str);
    $( "#Credits").modal('show')   
}

function ProfileSettings() {
    if (!sessionStorage.getItem('token')) {
        MyModal("Information","Please Sing In!!!");
        return;
    }

    if (!window.XMLHttpRequest) {
        MyModal("Error","Connection error!!!");
        return;
    }

    xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","phpfunctions/profile.php", false);
    xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlhttp.send("token="+sessionStorage.getItem('token'));

    if(xmlhttp.status=200) {
        if (xmlhttp.responseText.startsWith("{")) { //Είναι Json και κατ' επέκτασιν σωστή η κλήση
            res=JSON.parse(xmlhttp.responseText);
            sessionStorage.setItem('ProfileJSON',JSON.stringify(res));
            window.location.href='profile.html';
        } else {
            MyModal("Error", xmlhttp.responseText);
            return;
        }
    } else {
        MyModal("Error", xmlhttp.responseText);
        return;
    }
};

function isJSON(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

function toggleDisplay(element="") {
    if (element) {
        if ($(element).is(":visible")) {
            $(element).hide( "slow" );
        }
        else {
            $(element).show( "slow" );
        }
    }
};

function dateObjToString(date){
    var dd = date.getDate();
    var mm = date.getMonth() + 1; //January is 0!
    var yyyy = date.getFullYear();
    if (dd < 10) {
        dd = '0' + dd;
    } 
    if (mm < 10) {
        mm = '0' + mm;
    } 
    return dd + '/' + mm + '/' + yyyy;
}
