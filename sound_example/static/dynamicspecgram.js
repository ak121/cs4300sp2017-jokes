function closest (num, arr) {
  var curr = arr[0];
  var diff = Math.abs (num - curr);
  for (var val = 0; val < arr.length; val++) {
      var newdiff = Math.abs (num - arr[val]);
      if (newdiff < diff) {
          diff = newdiff;
          curr = arr[val];
      }
  }
  return curr;
}
var recalculateSpectrum;
var updateSpectrum;
var paused = true;

$(document).ready(function() {

  createViz = function () {
    var title = $('#selectedsong').val();
    var filename = title + '.wav';
    $('#filename').html(filename);
    //$.get( `http://127.0.0.1:5000/spectrogram/${title}`, updateSong );
    $.get( `${window.location.href}spectrogram/${title}`, updateSong );
  };

  function updateSong( data ) {
    var width = 800;
    var height = 500;
    var padding = 50;

    var audiourl = data.filename;
    var specmat = data.specmat;
    var freqs = data.freqs;
    var times = data.times;
    var maxamplitude = data.maxamplitude;
    var maxtime = data.maxtime;
    var maxfreq = data.maxfreq;
    $('#audioplayer').removeAttr('src');
    $('#audioplayer').attr('src', audiourl);
    $('#totalsecs').html((maxtime).toPrecision(3));
    $('#timeslider').attr('max', maxtime);
    $('#timeslider').attr('step', 0.01);
    $('#timeslider').attr('value', 0);
    $('#timevalue').html(0)

    d3.select("#specgram svg").remove();
    var svg = d3.select("#specgram").append("svg")
    .attr("width",width).attr("height",height);

    var xScale = d3.scale.linear().domain([0,maxfreq]).range([padding,width-padding]);
    var yScale = d3.scale.linear().domain([0,maxamplitude]).range([height-padding,padding]);

    var lineFunc = d3.svg.line()
    .x((d)=>xScale(d.frequency))
    .y((d)=>yScale(d.amplitude))
    .interpolate("linear");

    prepareAxes(svg, xScale, yScale);

    var freqseries = [];
    for ( i in times ){
      var time = times[i];
      var values = [];
      for ( j in freqs ){
        values.push({
          'frequency': freqs[j],
          'amplitude': specmat[j][i]
        });
      }
      freqseries.push({
        'key': time,
        'values': values
      });
    }

    var specplot = svg.append("path").attr('class','specgram');
    specplot.attr("d",lineFunc(freqseries[0].values));

    recalculateSpectrum = function (){
      var currTime = $("#timeslider").val();
      $("#timevalue").html(currTime);
      var newIndex = times.indexOf(closest(currTime,times));
      specplot.attr("d",lineFunc(freqseries[newIndex].values));
    };

    updateSpectrum = function(msecs) {
      return function () {
        if ((!paused)&&(document.getElementById('timeslider').value <= maxtime)){
          recalculateSpectrum();
          var currTime = Number(document.getElementById('timeslider').value);
          currTime += msecs/1000;
          document.getElementById('timeslider').value = currTime.toPrecision(3);
        }
      };
    }

    var audio = document.getElementById('audioplayer');

    play = function() {
      paused = false;
      audio.play();
      playing = setInterval(updateSpectrum(50), 50);
    }

    pause = function() {
      paused = true;
      audio.pause();
      clearInterval(playing);
    }

    $('#play').attr('onclick','play()');
    $('#pause').attr('onclick','pause()');
  }

  function prepareAxes(svg, xScale, yScale) {
    var xAxis = d3.svg.axis().scale(xScale).orient("bottom");
    var yAxis = d3.svg.axis().scale(yScale).orient("left").tickFormat(d3.format("e"));

    svg.append("g").attr("class","axis")
    .attr("transform","translate(0,450)")
    .call(xAxis);

    svg.append("g").attr("class","axis")
    .attr("transform","translate(50,0)")
    .call(yAxis);

    svg.append("text").style("font-size",14).attr("x",20).attr("y",40)
    .text("Amplitude").style("fill","#dddddd");

    svg.append("text").style("font-size",14).attr("x",700).attr("y",485)
    .text("Frequency [Hz]").style("fill","#dddddd");
  }

});
