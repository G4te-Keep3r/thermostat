$(document).ready(function(){
	//alert(limitSQLvar);
	$.ajax({
		//alert("inside ajax");
		//url : "http://192.168.2.236/followersdata.php", data: {limitSQLvar: limitSQLvar}, dataType: 'json', type: 'POST', type : 'GET',
		//url : "http://192.168.2.236/followersdata.php", data: {limitSQLvar: limitSQLvar}, dataType: 'json', type: 'GET',
		url : "http://192.168.2.236/2hour.php",
		type : "GET",
		success : function(data){
			console.log(data);

			var userid = [];
			var temp = [];
			var highCutOff = [];
			var lowCutOff = [];
			var temp_hall = [];
			var outside = [];
			var attic = [];

			for(var i in data) {
				//recordID, temp, highCutOff, lowCutOff
				//recordID, temp, highCutOff, lowCutOff, temp_hall
				//userid.push("recordID " + data[i].recordID);
				userid.push(data[i].recordID);
				temp.push(data[i].temp);
				highCutOff.push(data[i].highCutOff);
				lowCutOff.push(data[i].lowCutOff);
				temp_hall.push(data[i].temp_hall);
				outside.push(data[i].outside);
				attic.push(data[i].attic);
			}

			var chartdata = {
				labels: userid,
				datasets: [
					{
						label: "temp",
						fill: false,
						lineTension: 0.1,
						borderWidth: 2, //0 seems to be the same as 3
						pointRadius: 2,
						backgroundColor: "rgba(75, 0, 130, 0.75)",
						borderColor: "rgba(75, 0, 130, 1)",
						pointHoverBackgroundColor: "rgba(75, 0, 130, 1)",
						pointHoverBorderColor: "rgba(75, 0, 130, 1)",
						data: temp
					},
					{
						label: "highCutOff",
						fill: false,
						lineTension: 0.1,
						borderWidth: 2,
						pointRadius: 2,
						backgroundColor: "rgba(211, 72, 54, 0.75)",
						borderColor: "rgba(211, 72, 54, 1)",
						pointHoverBackgroundColor: "rgba(211, 72, 54, 1)",
						pointHoverBorderColor: "rgba(211, 72, 54, 1)",
						data: highCutOff
					},
					{
						label: "lowCutOff",
						fill: false,
						lineTension: 0.1,
						borderWidth: 2,
						pointRadius: 2,
						backgroundColor: "rgba(29, 202, 255, 0.75)",
						borderColor: "rgba(29, 202, 255, 1)",
						pointHoverBackgroundColor: "rgba(29, 202, 255, 1)",
						pointHoverBorderColor: "rgba(29, 202, 255, 1)",
						data: lowCutOff
					},
					{
						label: "temp_hall",
						fill: false,
						lineTension: 0.1,
						borderWidth: 2,
						pointRadius: 2,
						backgroundColor: "rgba(150, 100, 50, 0.75)",
						borderColor: "rgba(150, 100, 50, 1)",
						pointHoverBackgroundColor: "rgba(150, 100, 50, 1)",
						pointHoverBorderColor: "rgba(150, 100, 50, 1)",
						data: temp_hall
					},
					{
						label: "outside",
						fill: false,
						lineTension: 0.1,
						borderWidth: 2,
						pointRadius: 2,
						backgroundColor: "rgba(0, 100, 0, 0.75)",
						borderColor: "rgba(0, 100, 0, 1)",
						pointHoverBackgroundColor: "rgba(0, 100, 0, 1)",
						pointHoverBorderColor: "rgba(0, 100, 0, 1)",
						data: outside
					},
					{
						label: "attic",
						fill: false,
						lineTension: 0.1,
						borderWidth: 2,
						pointRadius: 2,
						backgroundColor: "rgba(0, 0, 100, 0.75)",
						borderColor: "rgba(0, 0, 100, 1)",
						pointHoverBackgroundColor: "rgba(0, 0, 100, 1)",
						pointHoverBorderColor: "rgba(0, 0, 100, 1)",
						data: attic
					}
				]
			};

			var ctx = $("#mycanvas-2hour");

			var LineGraph = new Chart(ctx, {
				type: 'line',
				data: chartdata
			});
		},
		error : function(data) {
			alert(data);
		}
	});
});