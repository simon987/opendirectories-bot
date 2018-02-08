var xhttp = new XMLHttpRequest();

xhttp.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {

        console.log("Received: " + this.responseText);

        var rData = this.responseText;

        drawChart(JSON.parse(rData));
        fillTable(JSON.parse(rData));
    }
};
xhttp.open("GET", "./json_chart", true);
xhttp.send();

function drawChart(rData) {

    var dataSetSize = [];
    var dataSetCount = [];
    var labels = [];
    var colors = [];

    var otherSize = 0;
    var otherCount = 0;

    for(var ext in rData["ext_sizes"]) {
        //Ignore file sizes below 0.5%
        if (!isRelevant(rData, ext)) {

            otherSize += rData["ext_sizes"][ext];
            otherCount += rData["ext_count"][ext];

        } else {
            dataSetSize.push(rData["ext_sizes"][ext]);
            dataSetCount.push(rData["ext_count"][ext]);
            labels.push(ext + " x" + rData["ext_count"][ext] + " (" + humanFileSize(rData["ext_sizes"][ext]) + ")");
            colors.push(getRandomColor())
        }
    }

    if(otherCount !== 0) {
        colors.push(getRandomColor());
        labels.push("other x" + otherCount + " (" + humanFileSize(otherSize) + ")");
        dataSetSize.push(otherSize);
        dataSetCount.push(otherCount);
    }

    var ctx = document.getElementById('typesChart').getContext('2d');

    var fileTypePieChart = new Chart(ctx,{
        type: 'pie',
        data: {
            datasets: [{
                data: rData["total_size"] < 100000 ? dataSetCount : dataSetSize,
                backgroundColor: colors
            }],

            labels: labels

        },
        options: {
            title: {
                display: true,
                text: "File types for " + rData["base_url"] + " - " + humanFileSize(rData["total_size"])
            }
        }
    });
}

function fillTable(rData) {

    document.getElementById("baseUrl").innerHTML = rData["base_url"];
    document.getElementById("fileCount").innerHTML = rData["total_count"];
    document.getElementById("totalSize").innerHTML = humanFileSize(rData["total_size"]);
    document.getElementById("reportTime").innerHTML = rData["report_time"];

}


function isRelevant(rData, ext) {

    console.log("Checking + " + ext);
    console.log("total + " + rData["total_size"]);
    console.log("size + " + rData["ext_count"][ext]);
    console.log("min + " + 0.03 * rData["total_count"]);

    if(rData["total_size"] < 100000) {
        return rData["ext_count"][ext] > 0.03 * rData["total_count"]
    } else {
        return rData["ext_sizes"][ext] > 0.005 * rData["total_size"]
    }


}

/**
 * https://stackoverflow.com/questions/1484506
 */
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

/**
 * https://stackoverflow.com/questions/10420352
 */
function humanFileSize(bytes) {

    if(bytes === 0) {
        return "? B"
    }

    var thresh = 1000;
    if(Math.abs(bytes) < thresh) {
        return bytes + ' B';
    }
    var units = ['kB','MB','GB','TB','PB','EB','ZB','YB'];
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while(Math.abs(bytes) >= thresh && u < units.length - 1);

    return bytes.toFixed(1) + ' ' + units[u];
}