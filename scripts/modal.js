function MyModal(title="Flight scanner",maincontext="") {
    if ($("#MyModal")) {
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
        str +=    '                <button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>'; 
        str +=    '            </div>'; 
        str +=    '        </div>'; 
        str +=    '    </div>'; 
        str +=    '</div>'; 
    }
    $("body").prepend(str);
    $( "#MyModal").modal('show')    
}

function credits() {
    if ($("#Credits")) {
        var str = '<div class="modal fade" id="Credits" tabindex="-1" role="dialog">';
        str    +=    '<div class="modal-dialog" role="document">';
        str    +=    '    <div class="modal-content">';
        str    +=    '            <div class="modal-header">';
        str    +=    '                <h5 class="modal-title text-primary">Flight Scanner<br><p class="text-secondary">An innovative low-fare flight searching engine</p></h5>';             
        str    +=    '                <button type="button" class="close" data-dismiss="modal" aria-label="Close">';
        str    +=    '                    <span aria-hidden="true">&times;</span>';
        str    +=    '                </button>';
        str    +=    '           </div>';
        str    +=    '           <div class="modal-body">';
        str    +=    '               <h5 class="modal-title text-primary">Developers</h5>';
        str    +=    '               <p>Nariris Dimitris<br>Malliaridis Konstantinos<br>Sklavou Nasia</p>';
        str    +=    '            </div>';
        str    +=    '            <div class="modal-footer">';
        str    +=    '               <p class="text-center" >MSc in Web Intelligence &copy; 2018-2019</p>';
        str    +=    '           </div>';
        str    +=    '        </div>';
        str    +=    '    </div>';
        str    +=    '</div>';
    }
    $("body").prepend(str);
    $( "#Credits").modal('show')   
}