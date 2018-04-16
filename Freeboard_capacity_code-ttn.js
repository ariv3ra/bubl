pdu = datasources["microshare datapunks"]["objs"][0]["data"]["payload_fields"]["payload"];

var TOTAL_CONTAINER_CAPACITY = 8;  // Defines the total cpacity of a container in Centimeters

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

// Calculate the Current Capacity of the container
function container_status(current_capacity, total_capacity){
    // Check if the value is a number or string
    if (isNaN(current_capacity)){
        current_capacity = Number(current_capacity);
    }

    // Calculate the current capacity of the container
    var percentile = 100 - ((current_capacity / total_capacity) * 100);  // Calculate the percentage of the container

    return percentile;
}

strPDU = String(container_status(pdu, TOTAL_CONTAINER_CAPACITY));
strPDU = strPDU.fontcolor(valid_color(strPDU));
pdu_percentage = strPDU+'%';
return "<div style='font-size:6em;'><center>"+pdu_percentage+"</center></div>";