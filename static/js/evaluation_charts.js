document.addEventListener("DOMContentLoaded", function () {
    console.log("evaluation_charts.js is loaded");
  
    var chartDataString = document.getElementById("chart-data").textContent.replace(/&quot;/g, '"');
    console.log(chartDataString);
    var rawData;
    var chart;
  
    try {
      rawData = JSON.parse(chartDataString);
      console.log(rawData)
    } catch (error) {
      console.error("Error: failed to parse chart data: ", error);
    }
  
    function buildChartData(rawData, startDate, endDate) {
        if (!rawData || typeof rawData !== "object") {
          console.error("Error: chart data is not an object");
          return;
        }
      
        var labels = rawData.labels;
        var usefulRatings = rawData.useful_ratings;
        var notUsefulRatings = rawData.not_useful_ratings;
        var notEvaluatedRatings = rawData.not_evaluated_ratings;
      
        for (var prop in rawData) {
          if (rawData.hasOwnProperty(prop) && Array.isArray(rawData[prop])) {
            rawData[prop].forEach(function (entry, index) {
              var timestamp = new Date(entry.timestamp);
              if (timestamp >= startDate && timestamp <= endDate) {
                var labelIndex = labels.indexOf(entry.question);
      
                if (labelIndex === -1) {
                  labels.push(entry.question);
                  usefulRatings.push(0);
                  notUsefulRatings.push(0);
                  notEvaluatedRatings.push(0);
                  labelIndex = labels.length - 1;
                }
      
                if (entry.user_rating_choice === "U") {
                  usefulRatings[labelIndex]++;
                } else if (entry.user_rating_choice === "N") {
                  notUsefulRatings[labelIndex]++;
                } else {
                  notEvaluatedRatings[labelIndex]++;
                }
              }
            });
          }
        }
      
        return {
          labels: labels,
          useful_ratings: usefulRatings,
          not_useful_ratings: notUsefulRatings,
          not_evaluated_ratings: notEvaluatedRatings,
        };
      }
    
      window.updateChartData = function () {
        console.log("Button clicked");
        var startDateElem = document.getElementById("start-date");
        var endDateElem = document.getElementById("end-date");
      
        if (!startDateElem || !endDateElem) {
          console.error("Error: One or more elements not found.");
          return;
        }
      
        function formatDate(date) {
          return date.getFullYear() + "-" + (date.getMonth() + 1).toString().padStart(2, '0') + "-" + date.getDate().toString().padStart(2, '0');
        }
      
        var startDate = formatDate(new Date(startDateElem.value));
        var endDate = formatDate(new Date(endDateElem.value));
      
        console.log("Start Date:", startDate);
        console.log("End Date:", endDate);
      
        var chartData = buildChartData(rawData, startDate, endDate);
        console.log(chartData);
      
        if (chartData) {
          if (chart) {
            chart.destroy();
          }
          var ctx = document.getElementById("evaluationChart").getContext("2d");
          chart = new Chart(ctx, {
            type: "bar",
            data: {
              labels: chartData.labels,
              datasets: [
                {
                  label: "Útil",
                  data: chartData.useful_ratings,
                  backgroundColor: "#3cba9f",
                },
                {
                  label: "No útil",
                  data: chartData.not_useful_ratings,
                  backgroundColor: "#ff4040",
                },
                {
                  label: "No evaluado",
                  data: chartData.not_evaluated_ratings,
                  backgroundColor: "#666666",
                },
              ],
            },
            options: {
              scales: {
                y: {
                  ticks: {
                    beginAtZero: true,
                  },
                },
              },
            },
          });
        } else {
          console.error("Error: Failed to update chart data");
        }
      };
      
    updateChartData();
  });
  
  