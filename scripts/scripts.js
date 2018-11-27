function FillTheTable(response) {
    var Retval;
    retval = 
    `<br>
     <hr>
    <table id='results' border=1>    
    <tr>
        <th rowspan=2>Διάρκεια</th>
        <th colspan=2>Αναχώρηση</th>
        <th colspan=2>Άφιξη</th>
        <th colspan=3>Πτήση</th>
        <th colspan=2 rowspan=2 >Θέση</th>
        <th rowspan=2>Διαθέσιμες<br>θέσεις</th>
        <th colspan=3>Συν. Κόστος</th>
    </tr>
    <tr>
        <th>Αεροδρόμιο</th>
        <th>Ώρα</th>
        <th>Αεροδρόμιο</th>
        <th>Ώρα</th>
        <th>Airline</th>
        <th>Αριθμός</th>
        <th>Αεροσκάφος</th>
        <th>Total Price</th>
        <th>Total Fare</th>
        <th>Tax</th>
    </tr>`

    return retval;
}
