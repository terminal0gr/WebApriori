function guestlogin() {

    $.ajax({
        type: 'POST',
        url: 'phpfunctions/guestlogin.php'
    })
    .done(function(response, textStatus, jqXHR) {

        res=JSON.parse(response);

        if (jqXHR.status==200) {
            sessionStorage.setItem('token', res.token);
            sessionStorage.setItem('apikey', res.apikey);
            sessionStorage.setItem('username', res.name);
        } else {
            MyModal("An error occured",res.message);
        }

    })
    .fail(function(data) {

        if (data.responseText) {
            MyModal("WebApriori",data.responseText);
        } else {
            MyModal("WebApriori",'Unknown error occured!');
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
function MyModal(title="WebApriori",maincontext="", ConfirmFunc=false) {
    if ($("#MyModal")) {
        MyModalAnsw=false;
        var str = '<div class="modal fade" id="MyModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">';
        str +=    '    <div class="modal-dialog modal-dialog-centered">';
        str +=    '        <div class="modal-content">';
        str +=    '            <div class="modal-header">';
        str +=    '                <h5 class="modal-title" id="exampleModalLabel">' + title + '</h5>';    
        str +=    '                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>';
        str +=    '            </div>';
        str +=    '            <div class="modal-body">';
        str +=    '               ' + maincontext; 
        str +=    '            </div>';
        str +=    '            <div class="modal-footer">'; 
        if (ConfirmFunc) {
            str +=    '                <button type="button" class="btn btn-primary" >Yes</button>'; 
            str +=    '                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">No</button>'; 
        }
        else {
            str +=    '                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>'; 
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
        str     = '<div class="modal fade" id="Credits" tabindex="-1">';
        str    +=    '<div class="modal-dialog modal-dialog-centered">';
        str    +=    '    <div class="modal-content">';
        str    +=    '        <div class="modal-header"><div>';
        str    +=    '                <h1 class="modal-title text-primary fs-3">webApriori</h1>';
        str    +=    '                <p class="text-secondary">An innovative AutoML association rules mining engine</p></div>';             
        str    +=    '                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>';
        str    +=    '        </div>';
        str    +=    '           <div class="modal-body">';
        str    +=    '               <h5 class="modal-title text-primary">Developer</h5>';
        str    +=    '               <p>Malliaridis Konstantinos</p><hr>';
        str    +=    '               <h5 class="modal-title text-primary">Application Version</h5>';
        str    +=    '               <p>V01.07.00 beta 24/03/2024</p>';
        str    +=    '            </div>';
        str    +=    '            <div class="modal-footer">';
        str    +=    '               <p class="text-center" >MSc and PHd in Web Intelligence &copy; 2019-2024</p>';
        str    +=    '           </div>';
        str    +=    '        </div>';
        str    +=    '    </div>';
        str    +=    '</div>';
    }
    $("body").prepend(str);
    $( "#Credits").modal('show')   
}

function footerActions() {
    // Select the span element with id "erty"
    var spanElement = document.getElementById("c-footer-span");

    // Check if the span element exists
    if (spanElement) {
        // Update the inner text of the span element
        spanElement.innerHTML = "WebApriori - An innovative autoML association rules mining engine. &copy;2019-2024";
    } 
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

const copyToClipboard = str => {
    const el = document.createElement('textarea');  // Create a <textarea> element
    el.value = str;                                 // Set its value to the string that you want copied
    el.setAttribute('readonly', '');                // Make it readonly to be tamper-proof
    el.style.position = 'absolute';                 
    el.style.left = '-9999px';                      // Move outside the screen to make it invisible
    document.body.appendChild(el);                  // Append the <textarea> element to the HTML document
    const selected =            
      document.getSelection().rangeCount > 0        // Check if there is any content selected previously
        ? document.getSelection().getRangeAt(0)     // Store selection if found
        : false;                                    // Mark as false to know no selection existed before
    el.select();                                    // Select the <textarea> content
    document.execCommand('copy');                   // Copy - only works as a result of a user action (e.g. click events)
    document.body.removeChild(el);                  // Remove the <textarea> element
    if (selected) {                                 // If a selection existed before copying
      document.getSelection().removeAllRanges();    // Unselect everything on the HTML document
      document.getSelection().addRange(selected);   // Restore the original selection
    }
  };