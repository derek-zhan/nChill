'use strict';

angular.module('nchill', [])
  .factory('cal',function() {

var genres = {"Romance": 6, "Comedy": 4, "Fantasy":4, "Drama": 3, "Action": 3,"Sci-Fi":3, "Horror":0, "Thriller": 1, "Animation":2,"Family":1,"Adventure":4};
var MPAA = {"NC-17":20, 'TV-MA':20,"R":15,"PG-13":10,"PG":5,"G":1,"N/A":1,"TV-14":10,"NOT RATED":20};

  function calScore(details){
    var total,avg,score,i,len;
    total = avg = score = 0;
    var list = details.genre.split(",");

    if("Horror" in list){
      avg = 0;
    }else if("Romance" in list){
      avg = 6;
    }else{
      len = list.length;
      for(i = 0; i < list.length;i++){
        if(!(list[i] in genres)){
          length--;
        }else{
          total +=genres[list[i]];
        }
        avg = total/length;
      }
    }

    if(details.RTR == "N/A"){
      score = (avg*(MPAA[details.MPAAR]-1))*0.7 + 0.3* (100/details.IMDBR);
    }else{
      score = (avg*(MPAA[details.MPAAR]-1))*0.7 + 0.3* (0.5 *(100/details.IMDBR + 100/details.RTR));
    }
    return score*2;
    }

  })
  .controller('searchlist', function($scope, $http){
    $scope.$watch('search', function() {
      fetch();
    });

    $scope.search = "Sherlock Holmes";

    function fetch(){
      $http.get("http://www.omdbapi.com/?t=" + $scope.search + "&tomatoes=true&plot=full")
      .then(function(response){ $scope.details = response.data; });

    }

    $scope.update = function(movie){
      $scope.search = movie.Title;
    };

    $scope.select = function(){
      this.setSelectionRange(0, this.value.length);
    }
  });

