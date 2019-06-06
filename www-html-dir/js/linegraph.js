$(document).ready(function(){
	//alert(limitSQLvar);
	$.ajax({
		//alert("inside ajax");
		//url : "http://myac.dx.am/followersdata.php", data: {limitSQLvar: limitSQLvar}, dataType: 'json', type: 'POST', type : 'GET',
		//url : "http://myac.dx.am/followersdata.php", data: {limitSQLvar: limitSQLvar}, dataType: 'json', type: 'GET',
		url : "http://myac.dx.am/followersdata.php",
		type : "GET",
		success : function(data){
			console.log(data);

			var userid = [];
			var facebook_follower = [];
			var twitter_follower = [];
			var googleplus_follower = [];
			var temp_hall = [];

			for(var i in data) {
				//recordID, temp, highCutOff, lowCutOff
				//recordID, temp, highCutOff, lowCutOff, temp_hall
				//userid.push("recordID " + data[i].recordID);
				userid.push(data[i].recordID);
				facebook_follower.push(data[i].temp);
				twitter_follower.push(data[i].highCutOff);
				googleplus_follower.push(data[i].lowCutOff);
				temp_hall.push(data[i].temp_hall);
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
					},
					{
						label: "temp_hall",
						fill: false,
						lineTension: 0.1,
						backgroundColor: "rgba(211, 72, 54, 0.75)",
						borderColor: "rgba(211, 72, 54, 1)",
						pointHoverBackgroundColor: "rgba(211, 72, 54, 1)",
						pointHoverBorderColor: "rgba(211, 72, 54, 1)",
						data: temp_hall
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