var airports = [];
//Json Object shape
//airports = [
//  {code:'ATH', city:'Athens', country:'Greece'}
//];

var airlines = [];
//Json Object shape
//airlines = [
//  {iata:'OA', name:'Olympic Airways'}
//];


function find_airline(A_iata) {
    var res = airlines.find(x => x.iata === A_iata);
    var token = "0";
    if (sessionStorage.getItem('token')) {
        token=sessionStorage.getItem('token');
    }
    if (res===undefined) {
        if (window.XMLHttpRequest && sessionStorage.getItem('token')) {
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST","phpfunctions/getairline.php", false);
            xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
            xmlhttp.send("token="+token+"&iata=" +A_iata);

            if(xmlhttp.status=200) {
                if (xmlhttp.responseText.startsWith("{")) { //Είναι Json και κατ' επέκτασιν σωστή η κλήση
                    res=JSON.parse(xmlhttp.responseText);
                    airlines.push(res); 
                    return res.iata + ",<br>" + res.name;
                } else {
                    MyModal("Error", xmlhttp.responseText);
                    return A_iata;
                }
            } else {
                MyModal("Error", xmlhttp.responseText);
                return A_iata;
            }
        }
        else return A_iata;
    } else {
        return res.iata + ",<br>" + res.name;
    }
}

function find_airport(A_Code) {
    var res = airports.find(x => x.code === A_Code);
    var token = "0";
    if (sessionStorage.getItem('token')) {
        token=sessionStorage.getItem('token');
    }
    if (res===undefined) {
        if (window.XMLHttpRequest && sessionStorage.getItem('token')) {
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST","phpfunctions/getairport.php", false);
            xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
            xmlhttp.send("token="+token+"&code=" +A_Code);

            if(xmlhttp.status=200) {
                if (xmlhttp.responseText.startsWith("{")) { //Είναι Json και κατ' επέκτασιν σωστή η κλήση
                    res=JSON.parse(xmlhttp.responseText);
                    airports.push(res); 
                    return res.city + ",<br>" + res.country;
                } else {
                    MyModal("Error", xmlhttp.responseText);
                    return A_Code;
                }
            } else {
                MyModal("Error", xmlhttp.responseText);
                return A_Code;
            }                
        }
        else return A_Code;
    } else {
        return res.city + ",<br>" + res.country;
    }
}

function FillTheTable(response) {
    var retval=``;

    // if (response.results[0].itineraries.length) {
    //     retval+=`<p class=text-center>` + response.results.itineraries.length + ` low fare flights retrieved</p>`;
    // }

    retval += 
    `
    <table id='results' class="table table-bordered">  
        <thead>
            <tr>
                <th class="text-center" rowspan=2>#</th>
                <th class="text-center" rowspan=2>Duration</th>
                <th class="text-center" colspan=2>Departure</th>
                <th class="text-center" colspan=2>Arrival</th>
                <th class="text-center" colspan=3>Flight</th>
                <th class="text-center" colspan=2 rowspan=2 >Seat</th>
                <th class="text-center" rowspan=2>Seats<br>Available</th>
                <th class="text-center" colspan=3>Total Cost</th>
            </tr>
            <tr>
                <th class="text-center" >Airport</th>
                <th class="text-center" >Time</th>
                <th class="text-center" >Airport</th>
                <th class="text-center" >Time</th>
                <th class="text-center" >Airline</th>
                <th class="text-center" >Flight No</th>
                <th class="text-center" >Aircraft</th>
                <th class="text-center" >Fare</th>
                <th class="text-center" >Tax</th>
                <th class="text-center" >Total Price</th>
            </tr>
        </thead>
        <tbody>`;

    flights_sum=0;

    $.each(response.results, function(key, results) {

        retval += ` <tr> `;
  
        $.each(results.itineraries, function(key1, itineraries) {

            dromologia=itineraries.outbound.flights.length;

            duration = itineraries.outbound.duration.split(":");

            totallines=dromologia;

            if (itineraries.inbound !== undefined) {
                totallines+=itineraries.inbound.flights.length;
            }

            flights_sum++;

            retval+=`<td align=right rowspan=` + totallines + `>` + flights_sum + `</td>`

            retval+=`<td align=center rowspan=` + dromologia + `><b>Transition</b><br>` + (duration[0]==0 ? `` : duration[0]  + `h `) + duration[1] + `m<br>`;

            if (dromologia == 1) {
                retval+=`<b>Non stop</b></td>`;
            }
            else {
                retval+=`<b>` + (dromologia - 1) + ((dromologia - 1)>1?` stops` : ` stop`) + `</b></td>`;
            }

            index=0;

            $.each(itineraries.outbound.flights, function(key1, flights) {

                if (index > 0) retval+=`<tr>`;

                retval+=`<td align=center>` + flights.origin.airport + `<br>` + find_airport(flights.origin.airport) + `</td>`;

                var departure = flights.departs_at.split("T");
                var tmp_departure_date =departure[0].split("-");
                var departure_date = tmp_departure_date[2] + "/" + tmp_departure_date[1] + "/" + tmp_departure_date[0];
                var departure_time = departure[1];
                retval+=`<td align=center>` + departure_date + `<br>` + departure_time + `</td>`;

                retval+=`<td align=center>` + flights.destination.airport + `<br>` + find_airport(flights.destination.airport) + `</td>`;

                var arrival = flights.arrives_at.split("T");
                var tmp_arrival_date =arrival[0].split("-");
                var arrival_date = tmp_arrival_date[2] + "/" + tmp_arrival_date[1] + "/" + tmp_arrival_date[0];
                var arrival_time = arrival[1];
                retval+=`<td align=center>` + arrival_date + `<br>` + arrival_time + `</td>`;

                retval+=`<td align=center>` + find_airline(flights.operating_airline) + `<br>` +  `</td>`;

                retval+=`<td align=center>` + flights.flight_number + `</td>`;
                retval+=`<td align=center>` + flights.aircraft + `</td>`;
                retval+=`<td align=center>` + flights.booking_info.travel_class + `</td>`;
                retval+=`<td align=center>` + flights.booking_info.booking_code + `</td>`;
                var seats=flights.booking_info.seats_remaining;
                if(flights.booking_info.seats_remaining==9) {seats=">=9"};
                retval+=`<td align=center>` + seats + `</td>`;

                fare=parseFloat(parseFloat(results.fare.price_per_adult.total_fare).toFixed(2)-parseFloat(results.fare.price_per_adult.tax).toFixed(2)).toFixed(2);
                if(index == 0) {retval+=`<td align=center rowspan=` + totallines + `>` + fare + `</td>`};
                if(index == 0) {retval+=`<td align=center rowspan=` + totallines + `>` + results.fare.price_per_adult.tax + `</td>`};
                if(index == 0) {retval+=`<td align=center rowspan=` + totallines + `>` + results.fare.total_price + `</td>`};
     
                retval+=`</tr>`;
                    
                index++;

            });

            if(itineraries.inbound!==undefined) {

                dromologia=itineraries.inbound.flights.length;

                duration = itineraries.inbound.duration.split(":");
                retval+=`<td align=center rowspan=` + dromologia + `><b>return</b><br>` + (duration[0]==0 ? `` : duration[0]  + `h `) + duration[1] + `m<br>`;
                if (dromologia == 1) {
                    retval+=`<b>Non stop</b></td>`;
                }
                else {
                    retval+=`<b>` + (dromologia - 1) + ((dromologia - 1)>1?` stops` : ` stop`) + `</b></td>`;
                }

                index==0;

                $.each(itineraries.inbound.flights, function(key1, flights) {

                    retval+=`<td align=center>` + flights.origin.airport + `<br>` + find_airport(flights.origin.airport) + `</td>`;

                    var departure = flights.departs_at.split("T");
                    var tmp_departure_date =departure[0].split("-");
                    var departure_date = tmp_departure_date[2] + "/" + tmp_departure_date[1] + "/" + tmp_departure_date[0];
                    var departure_time = departure[1];
                    retval+=`<td align=center>` + departure_date + `<br>` + departure_time + `</td>`;
    
                    retval+=`<td align=center>` + flights.destination.airport + `<br>` + find_airport(flights.destination.airport) + `</td>`;

                    var arrival = flights.arrives_at.split("T");
                    var tmp_arrival_date =arrival[0].split("-");
                    var arrival_date = tmp_arrival_date[2] + "/" + tmp_arrival_date[1] + "/" + tmp_arrival_date[0];
                    var arrival_time = arrival[1];
                    retval+=`<td align=center>` + arrival_date + `<br>` + arrival_time + `</td>`;

                    retval+=`<td align=center>` + find_airline(flights.operating_airline) + `<br>` +  `</td>`;

                    retval+=`<td align=center>` + flights.flight_number + `</td>`;
                    retval+=`<td align=center>` + flights.aircraft + `</td>`;
                    retval+=`<td align=center>` + flights.booking_info.travel_class + `</td>`;
                    retval+=`<td align=center>` + flights.booking_info.booking_code + `</td>`;
                    var seats=flights.booking_info.seats_remaining;
                    if(flights.booking_info.seats_remaining==9) {seats=">=9"};
                    retval+=`<td align=center>` + seats + `</td>`;

                    retval+=`</tr>`;

                    index++;

                });
            }

            retval+=`<tr><td colspan=15 style="background:#007BFF; line-height:0.01;">&nbsp;</td></tr>`;	

        });
    });

    retval += `</tbody>
    </table>`

    retval += `<br><br><br>`

    if (flights_sum>0) {
        $('#result-dialog').html('<p class="text-center text-primary">' + flights_sum + ' low fare flights retrieved</p>');
    }

    return retval;

};                

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
            MyModal("Flight Scanner",data.responseText);
        } else {
            MyModal("Flight Scanner",'Unknown error occured!');
        }
    });
};
                        
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
        str     = '<div class="modal fade" id="Credits" tabindex="-1" role="dialog">';
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
        str    +=    '               <p>Naziris Dimitris<br>Malliaridis Konstantinos<br>Sklavou Nasia</p>';
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
