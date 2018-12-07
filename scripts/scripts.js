var airports = [];
//Json Object shape
//airports = [
//  {code:'ATH', city:'Athens', country:'Greece'}
//];

var airlines = [];
//Json Object shape
//airlines = [
//  {}
//];

function find_airport(A_Code) {

    var res = airports.find(x => x.code === A_Code);
    if (res===undefined) {
        if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST","phpfunctions/getairport.php", false);
            xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
            xmlhttp.send("code=" +A_Code);

            res=JSON.parse(xmlhttp.responseText);
            airports.push(res); 
            return res.city + ",<br>" + res.country;
        }
        else return A_Code;
    } else {
        return res.city + ",<br>" + res.country;
    }

}

function FillTheTable(response) {
    var Retval;
    retval = 
    `<br>
     <hr>
    <table id='results' border=1>    
    <tr>
        <th rowspan=2>Duration</th>
        <th colspan=2>Departure</th>
        <th colspan=2>Arrival</th>
        <th colspan=3>Flight</th>
        <th colspan=2 rowspan=2 >Seat</th>
        <th rowspan=2>Seats<br>Available</th>
        <th colspan=3>Total Cost</th>
    </tr>
    <tr>
        <th>Airport</th>
        <th>Time</th>
        <th>Airport</th>
        <th>Time</th>
        <th>Airline</th>
        <th>Flight No</th>
        <th>Aircraft</th>
        <th>Total Price</th>
        <th>Total Fare</th>
        <th>Tax</th>
    </tr>`

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

                //TODO Read airlines From Database...
                retval+=`<td align=center>` + flights.operating_airline + `<br>` +  `</td>`;

                retval+=`<td align=center>` + flights.flight_number + `</td>`;
                retval+=`<td align=center>` + flights.aircraft + `</td>`;
                retval+=`<td align=center>` + flights.booking_info.travel_class + `</td>`;
                retval+=`<td align=center>` + flights.booking_info.booking_code + `</td>`;
                var seats=flights.booking_info.seats_remaining;
                if(flights.booking_info.seats_remaining==9) {seats=">=9"};
                retval+=`<td align=center>` + seats + `</td>`;

                if(index == 0) {retval+=`<td align=center rowspan=` + totallines + `>` + results.fare.total_price + `</td>`};
                if(index == 0) {retval+=`<td align=center rowspan=` + totallines + `>` + results.fare.price_per_adult.total_fare + `</td>`};
                if(index == 0) {retval+=`<td align=center rowspan=` + totallines + `>` + results.fare.price_per_adult.tax + `</td>`};
     
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

                    //TODO Read airlines From Database...
                    retval+=`<td align=center>` + flights.operating_airline + `<br>` +  `</td>`;

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

            retval+=`<tr><td colspan=14 style="background: lightblue; line-height:0.01;">&nbsp;</td></tr>`;	

        });
    });

    retval += `</table>`

    retval += `<br><br><br>`

    return retval;

};                
                        
                    


