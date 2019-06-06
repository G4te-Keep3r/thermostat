$(document).ready(function(){
	$.ajax({
		url : "http://myac.dx.am/experimenting/chartjs-master/php-mysql-chartjs/tempchart.php",
		type : "GET",
		success : function(data){
			console.log(data);

			var userid = [];
			var facebook_follower = [];
			var twitter_follower = [];
			var googleplus_follower = [];

			for(var i in data) {
				//recordID, temp, highCutOff, lowCutOff
				userid.push("recordID " + data[i].recordID);
				facebook_follower.push(data[i].temp);
				twitter_follower.push(data[i].highCutOff);
				googleplus_follower.push(data[i].lowCutOff);
			}

			var chartdata = {
				labels: userid,
				datasets: [
					{
						label: "temp",
						fill: false,
						lineTension: 0.1,
						backgroundColor: "rgba(59, 89, 152, 0.75)",
						borderColor: "rgba(59, 89, 152, 1)",
						pointHoverBackgroundColor: "rgba(59, 89, 152, 1)",
						pointHoverBorderColor: "rgba(59, 89, 152, 1)",
						data: facebook_follower
					},
					{
						label: "highCutOff",
						fill: false,
						lineTension: 0.1,
						backgroundColor: "rgba(29, 202, 255, 0.75)",
						borderColor: "rgba(29, 202, 255, 1)",
						pointHoverBackgroundColor: "rgba(29, 202, 255, 1)",
						pointHoverBorderColor: "rgba(29, 202, 255, 1)",
						data: twitter_follower
					},
					{
						label: "lowCutOff",
						fill: false,
						lineTension: 0.1,
						backgroundColor: "rgba(211, 72, 54, 0.75)",
						borderColor: "rgba(211, 72, 54, 1)",
						pointHoverBackgroundColor: "rgba(211, 72, 54, 1)",
						pointHoverBorderColor: "rgba(211, 72, 54, 1)",
						data: googleplus_follower
					}
				]
			};

			var ctx = $("#mycanvas");

			var LineGraph = new Chart(ctx, {
				type: 'line',
				data: chartdata
			});
		},
		error : function(data) {

		}
	});
});