// Example: Convert temp from C to F and truncate to 2 decimal places.
// return (datasources["MyDatasource"].sensor.tempInF * 1.8 + 32).toFixed(2);
function valid_color(value){
    color = "";
    if (value >= 0 && value <= 50){
        color = "green";
    }else if (value >= 51 && value <= 74){
        color = "yellow";
    }else if (value >= 75){
        color = "red";
    }
    return color;
}

pdu = datasources["microshare datapunks"]["objs"][0]["data"]["pdu"];
pdu = pdu.fontcolor(valid_color(pdu));
pdu_percentage = pdu+'%';
return "<div style='font-size:120px;'><center>"+pdu_percentage+"</center></div>";
