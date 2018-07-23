function search(){
// call the server
  var x = document.getElementById('summoner').value;
  var y = document.getElementById('regionselect').value;
  $.ajax({
    url: "http://localhost:8080/info",
    data: {name: x, region: y}, // pass in summoner name and region for api call
    dataType: "json",
    crossDomain: true,
    success: function(data){
      alert(data);
  },
  error: function(textStatus, errorThrow){
    alert("Summoner not found."); // on failiure
    window.location.reload();
      }
    });
   
}
function handle(e){
        if(e.keyCode === 13){
            e.preventDefault(); // when enter is presssed, run search()
            search();
        }
    }