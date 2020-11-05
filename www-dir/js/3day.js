$(document).ready(function(){
	$.ajax({
		url : "http://192.168.2.236/3day.php",
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
			var state = [];

			for(var i in data) {
				//userid.push("recordID " + data[i].recordID);
				userid.push(data[i].recordID);
				temp.push(data[i].temp);
				highCutOff.push(data[i].highCutOff);
				lowCutOff.push(data[i].lowCutOff);
				temp_hall.push(data[i].temp_hall);
				outside.push(data[i].outside);
				attic.push(data[i].attic);
				state.push(data[i].state);
			}

			var chartdata = {
				labels: userid,
				datasets: [
					{
						label: "temp",
						fill: false,
						lineTension: 0.1,
						pointRadius: 0,
						borderWidth: 0.7,
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
						pointRadius: 0,
						borderWidth: 0.7,
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
						pointRadius: 0,
						borderWidth: 0.7,
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
						pointRadius: 0,
						borderWidth: 0.7,
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
						pointRadius: 0,
						borderWidth: 0.7,
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
						borderWidth: 0,
						pointRadius: 0.7,
						backgroundColor: "rgba(0, 0, 100, 0.75)",
						borderColor: "rgba(0, 0, 100, 1)",
						pointHoverBackgroundColor: "rgba(0, 0, 100, 1)",
						pointHoverBorderColor: "rgba(0, 0, 100, 1)",
						data: attic
					},
					{
						label: "state",
						fill: false,
						lineTension: 0.1,
						borderWidth: 2,
						pointRadius: 2,
						backgroundColor: "rgba(100, 100, 100, 0.75)",
						borderColor: "transparent",
						pointHoverBackgroundColor: "rgba(100, 100, 100, 1)",
						pointHoverBorderColor: "rgba(100, 100, 100, 1)",
						data: state
					}
				]
			};

			var ctx = $("#mycanvas-3day");

			var LineGraph = new Chart(ctx, {
				type: 'line',
				data: chartdata
			});
		},
		error : function(data) {

		}
	});
});