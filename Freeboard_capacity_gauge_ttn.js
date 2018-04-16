pdu = datasources["microshare datapunks"]["objs"][0]["data"]["payload_fields"]["payload"];

var TOTAL_CONTAINER_CAPACITY = 20;  // Defines the total cpacity of a container in Centimeters

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

percentage_full = container_status(pdu, TOTAL_CONTAINER_CAPACITY);
return percentage_full;
